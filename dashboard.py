#!/usr/bin/env python3
"""Aurelius · dashboard local (PyWebView · GTK3/WebKit2).

La cara ya existe y no se toca: se carga `~/aurelius/interface/aurelius_face.html`
por `file://`, así los diez assets relativos (4 CSS + 6 JS) resuelven solos.

D75 · ni una capa abre un socket. El modelo y la voz son procesos HIJOS del
gerente (`aurelius-m1/aurelius` → llama-cli + piper, por tubería). Este proceso
no escucha en ningún puerto, no habla por HTTP y no usa ollama.

D77 · la página puede preguntar si es un proceso. Lo es: PyWebView. Por eso
`file://` deja de estar vetado aquí.

La cara fue escrita contra el servidor estático :8050 y contra un endpoint
ollama: hace `fetch()` a `/api/estado`, `/api/inventario`, `/api/preferencia`,
`/api/modulo/completar`, `/api/totem` y `<EP>/api/chat`. NO se edita el fichero.
En su lugar se inyecta SHIM_JS como *user script* de WebKit en `document-start`
—antes de que corra un solo script de la página— que redirige esas rutas al
puente `pywebview.api`. Es inyección, no edición: `aurelius_face.html` queda
intacto en el disco (además su repo es público y este dashboard es privado).
"""

from __future__ import annotations

import json
import os
import shutil
import sqlite3
import subprocess
import threading
from pathlib import Path

import psutil  # noqa: F401  (declarado en el contrato; se usa para la medición)
import webview

# ─────────────────────────────────────────────────────────────────────────────
# Rutas medidas (2026-08-16). Ninguna se adivina, y ninguna se escribe absoluta:
# la guardia de higiene trata la ruta absoluta como suelo duro (D8/D34).
# ─────────────────────────────────────────────────────────────────────────────
RAIZ = Path(__file__).resolve().parent          # el propio repo privado
HOGAR = Path.home()

CARA = HOGAR / "aurelius" / "interface" / "aurelius_face.html"
GERENTE = HOGAR / "aurelius-m1" / "aurelius"
AUDIO = GERENTE.parent / "ultima-respuesta.wav"
MEMORIA = HOGAR / ".aurelius" / "memory.db"

# El gerente resuelve llama-cli, el modelo y ARQUETIPO.md contra $HOME, pero los
# tres se mudaron bajo este repo y su literal se quedó viejo. Reapuntar HOME SOLO
# para el proceso hijo alinea las tres rutas sin editar el gerente (que está
# fuera de alcance). `AQUI` del wrapper es dirname($0), así que voces/ y
# venv/piper siguen resolviendo junto al gerente. Desviación mínima aditiva,
# declarada: si algún día el gerente se corrige, esto sobra y no estorba.
HOME_GERENTE = str(RAIZ)

TIMEOUT_GERENTE = 30  # s · la guarda de la propia cara aborta a los 45 s

# Reproductor del wav que deja piper. Se resuelve por `which`, nunca por PATH
# implícito (footgun conocido: el PATH de un servicio no es el interactivo).
# Otro proceso hijo más: ninguno de ellos abre un socket.
REPRODUCTORES = ("pw-play", "paplay", "aplay", "ffplay")


# ─────────────────────────────────────────────────────────────────────────────
# El shim. Se inyecta en document-start, así que instala su `fetch` antes de
# que la cara dispare los suyos de arranque.
# ─────────────────────────────────────────────────────────────────────────────
SHIM_JS = r"""
(function () {
  "use strict";
  if (window.__AURELIUS_SHIM__) return;
  window.__AURELIUS_SHIM__ = true;

  var originalFetch = window.fetch ? window.fetch.bind(window) : null;

  // El puente tarda un instante en existir. Se espera hasta 10 s; si no llega,
  // se devuelve null y cada ruta degrada a su propio .catch() (la cara ya los
  // tiene: NO_DATA es preferible a un dato inventado).
  function apiLista() {
    return new Promise(function (resolve) {
      (function esperar(intentos) {
        if (window.pywebview && window.pywebview.api) return resolve(window.pywebview.api);
        if (intentos <= 0) return resolve(null);
        setTimeout(function () { esperar(intentos - 1); }, 100);
      })(100);
    });
  }

  function respuestaJson(obj, ok) {
    var cuerpo = JSON.stringify(obj === undefined ? null : obj);
    return {
      ok: ok !== false, status: ok === false ? 503 : 200, headers: new Headers(),
      json: function () { return Promise.resolve(JSON.parse(cuerpo)); },
      text: function () { return Promise.resolve(cuerpo); }
    };
  }

  // /api/chat no devuelve JSON: la cara lo lee como stream NDJSON estilo ollama
  // (r.body.getReader() + j.message.content por línea). El gerente es de UN
  // disparo —carga el modelo, responde y muere—, así que aquí sale un stream
  // sintético de un solo trozo. La cara no nota la diferencia.
  function respuestaNdjson(texto) {
    var linea = JSON.stringify({ message: { role: "assistant", content: texto } }) + "\n";
    var bytes = new TextEncoder().encode(linea);
    var entregado = false;
    return {
      ok: true, status: 200, headers: new Headers(),
      body: {
        getReader: function () {
          return {
            read: function () {
              if (entregado) return Promise.resolve({ done: true, value: undefined });
              entregado = true;
              return Promise.resolve({ done: false, value: bytes });
            },
            cancel: function () { return Promise.resolve(); },
            releaseLock: function () {}
          };
        }
      },
      json: function () { return Promise.resolve(JSON.parse(linea)); },
      text: function () { return Promise.resolve(linea); }
    };
  }

  function cuerpoDe(opciones) {
    if (!opciones || !opciones.body) return {};
    if (typeof opciones.body !== "string") return {};   // /api/totem manda binario
    try { return JSON.parse(opciones.body); } catch (e) { return {}; }
  }

  function idiomaActual() {
    try {
      var sel = document.getElementById("au-lang");
      if (sel && sel.value) return String(sel.value).slice(0, 2);
      if (window.I && window.I.locale) return String(window.I.locale).slice(0, 2);
    } catch (e) {}
    return "es";
  }

  window.fetch = function (entrada, opciones) {
    var url = (typeof entrada === "string") ? entrada : (entrada && entrada.url) || "";
    var ruta;
    try { ruta = new URL(url, location.href).pathname; } catch (e) { ruta = String(url); }

    // Se decide por el FINAL de la ruta, no por el host: así da igual que la
    // cara componga la URL contra localhost:11434, contra el mismo origen o
    // contra lo que diga config.json.
    function esRuta(sufijo) { return ruta.slice(-sufijo.length) === sufijo; }

    if (esRuta("/api/chat")) {
      var cuerpo = cuerpoDe(opciones);
      var msgs = (cuerpo && cuerpo.messages) || [];
      var pregunta = "";
      for (var i = msgs.length - 1; i >= 0; i--) {
        if (msgs[i] && msgs[i].role === "user") { pregunta = msgs[i].content || ""; break; }
      }
      // El system prompt de la cara se descarta a propósito: el carácter lo pone
      // el gerente desde ARQUETIPO.md (texto firmado). Una segunda fuente de
      // carácter es una fuente que se queda vieja.
      return apiLista().then(function (api) {
        if (!api) return respuestaJson({ error: "puente no disponible" }, false);
        // hablar=true: piper genera el wav y el puente lo suelta en el
        // reproductor. En inglés el gerente enmudece solo (la voz es es_ES).
        return api.enviar_pregunta(pregunta, idiomaActual(), true).then(function (r) {
          if (!r || r.error) return respuestaJson({ error: (r && r.error) || "sin respuesta" }, false);
          return respuestaNdjson(r.texto || "");
        });
      });
    }

    if (esRuta("/api/estado")) {
      return apiLista().then(function (api) {
        return api ? api.obtener_estado().then(function (e) { return respuestaJson(e); })
                   : respuestaJson(null, false);
      });
    }

    // El inventario original lo servía ollama. Aquí lo sirve la memoria: es el
    // único inventario real que este nodo puede declarar sin inventarse nada.
    if (esRuta("/api/inventario")) {
      return apiLista().then(function (api) {
        return api ? api.leer_memoria().then(function (v) { return respuestaJson(v); })
                   : respuestaJson(null, false);
      });
    }

    // /api/preferencia tiene las dos mitades: GET lee, POST guarda.
    if (esRuta("/api/preferencia")) {
      var metodo = String((opciones && opciones.method) || "GET").toUpperCase();
      return apiLista().then(function (api) {
        if (!api) return respuestaJson(null, false);
        if (metodo === "GET") {
          return api.obtener_preferencia().then(function (p) { return respuestaJson(p); });
        }
        return api.guardar_preferencia(cuerpoDe(opciones)).then(function (r) {
          return respuestaJson(r);
        });
      });
    }

    // Sin soporte en modo local: se responde NO soportado, nunca un ok falso.
    if (esRuta("/api/modulo/completar") || esRuta("/api/totem")) {
      return Promise.resolve(respuestaJson({ error: "NO_SOPORTADO_EN_LOCAL" }, false));
    }

    // Los .json de configuración los sirve el puente, no WebKit: la Fetch API
    // RECHAZA el esquema file:// por diseño (allow_file_access_from_file_urls
    // solo cubre XHR). Sin esto, cargarConfig() falla en silencio, la cara cae
    // al literal de último recurso y pinta el aviso naranja "point Aurelius at
    // your model" — aunque el modelo esté ahí mismo, respondiendo.
    var m = ruta.match(/\/([a-z0-9_.-]+\.json)$/i);
    if (m) {
      var nombre = m[1];
      return apiLista().then(function (api) {
        if (!api) return respuestaJson(null, false);
        return api.leer_json(nombre).then(function (d) {
          if (!d || d.__falta) return respuestaJson(null, false);
          return respuestaJson(d);
        });
      });
    }

    // El resto (CSS, imágenes, scripts) lo carga WebKit por file:// sin pasar
    // por fetch, así que aquí no llega casi nada.
    if (!originalFetch) return Promise.reject(new Error("sin fetch nativo"));
    return originalFetch(entrada, opciones);
  };
})();
"""


# ─────────────────────────────────────────────────────────────────────────────
# El puente. Todo método público de esta clase es visible como pywebview.api.<x>
# ─────────────────────────────────────────────────────────────────────────────
class Api:
    def __init__(self) -> None:
        self._ultima: dict = {"texto": "", "audio_path": None, "error": None}
        self._candado = threading.Lock()

    # ── contrato del prompt ──────────────────────────────────────────────────
    def enviar_pregunta(self, texto: str, idioma: str = "es", hablar: bool = True) -> dict:
        """Llama al gerente como proceso hijo. Sin sockets, sin red, sin ollama.

        La pregunta va por ARGV: el gerente es un wrapper de un disparo
        (`llama-cli -no-cnv`), no un proceso conversacional con stdin abierto.
        """
        texto = (texto or "").strip()
        if not texto:
            return {"texto": "", "audio_path": None, "error": "pregunta vacía"}

        cmd = [str(GERENTE)]
        if idioma == "en":
            cmd.append("--en")          # --en ya implica sin voz (la voz es es_ES)
        elif not hablar:
            cmd.append("--muda")
        cmd.append(texto)

        entorno = os.environ.copy()
        entorno["HOME"] = HOME_GERENTE

        try:
            r = subprocess.run(
                cmd, capture_output=True, text=True,
                timeout=TIMEOUT_GERENTE, env=entorno, cwd=str(GERENTE.parent),
            )
        except subprocess.TimeoutExpired:
            salida = {"texto": "", "audio_path": None,
                      "error": f"el gerente no respondió en {TIMEOUT_GERENTE}s"}
            with self._candado:
                self._ultima = salida
            return salida
        except OSError as e:
            salida = {"texto": "", "audio_path": None, "error": f"no se pudo lanzar: {e}"}
            with self._candado:
                self._ultima = salida
            return salida

        cuerpo = (r.stdout or "").strip()
        if r.returncode != 0 or not cuerpo:
            salida = {"texto": "", "audio_path": None,
                      "error": (r.stderr or "").strip()[-400:] or f"código {r.returncode}"}
        else:
            con_voz = hablar and idioma != "en" and AUDIO.exists()
            salida = {"texto": cuerpo,
                      "audio_path": str(AUDIO) if con_voz else None,
                      "error": None}
            if con_voz:
                salida["audio_reproducido"] = self._reproducir(AUDIO)

        with self._candado:
            self._ultima = salida
        return salida

    @staticmethod
    def _reproducir(wav: Path) -> bool:
        """Suelta el wav en un reproductor y NO espera: la respuesta de texto ya
        está pintada y el audio no debe retrasarla."""
        for nombre in REPRODUCTORES:
            binario = shutil.which(nombre)
            if not binario:
                continue
            cmd = [binario, "-nodisp", "-autoexit", str(wav)] if nombre == "ffplay" \
                else [binario, str(wav)]
            try:
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return True
            except OSError:
                continue
        return False

    def obtener_respuesta(self) -> dict:
        with self._candado:
            return dict(self._ultima)

    def leer_memoria(self) -> dict:
        """SELECT en solo lectura. Si no hay base, NO_DATA (jamás un dato inventado)."""
        if not MEMORIA.exists():
            return {"estado": "NO_DATA", "motivo": f"no existe {MEMORIA}"}
        try:
            con = sqlite3.connect(f"file:{MEMORIA}?mode=ro", uri=True)
            con.execute("PRAGMA query_only = ON")
            con.row_factory = sqlite3.Row
            filas = con.execute(
                "SELECT id, what, why, where_ref, learned, origin, status, created_at "
                "FROM engrams WHERE status = 'activo' ORDER BY id DESC LIMIT 200"
            ).fetchall()
            perfil = {k: v for (k, v) in con.execute("SELECT key, value FROM profile")}
            con.close()
        except sqlite3.Error as e:
            return {"estado": "NO_DATA", "motivo": f"sqlite: {e}"}

        if not filas:
            return {"estado": "NO_DATA", "motivo": "sin engrams", "perfil": perfil, "engrams": []}
        return {"estado": "OK", "perfil": perfil, "engrams": [dict(f) for f in filas]}

    def escribir_memoria(self, what: str, why: str = "NO_DATA",
                         where_ref: str = "NO_DATA", learned: str = "",
                         status: str = "activo") -> dict:
        """INSERT explícito + checkpoint WAL, para que el dato quede en el .db
        y no colgando en el -wal (la base se lee desde fuera del dashboard)."""
        what = (what or "").strip()
        if not what:
            return {"ok": False, "error": "what vacío (lo prohíbe el CHECK de la tabla)"}
        if status not in ("activo", "archivado"):
            return {"ok": False, "error": f"status inválido: {status}"}
        if not MEMORIA.exists():
            return {"ok": False, "error": f"no existe {MEMORIA}"}
        try:
            con = sqlite3.connect(str(MEMORIA), isolation_level=None)
            con.execute("PRAGMA journal_mode=WAL")
            con.execute("BEGIN")
            cur = con.execute(
                "INSERT INTO engrams (what, why, where_ref, learned, origin, status) "
                "VALUES (?, ?, ?, ?, 'persona', ?)",
                (what, why or "NO_DATA", where_ref or "NO_DATA", learned or "", status),
            )
            nuevo = cur.lastrowid
            con.execute("COMMIT")
            con.execute("PRAGMA wal_checkpoint(TRUNCATE)")
            con.close()
        except sqlite3.Error as e:
            return {"ok": False, "error": f"sqlite: {e}"}
        return {"ok": True, "id": nuevo}

    # ── rutas que la cara espera del servidor :8050 ──────────────────────────
    def obtener_estado(self) -> dict:
        mem = self.leer_memoria()
        perfil = mem.get("perfil", {}) if isinstance(mem, dict) else {}
        estado = {"modo": "local", "transporte": "pywebview", "servidor": None}
        if perfil.get("language"):
            estado["locale"] = perfil["language"]
        if perfil.get("verbosidad"):
            estado["verbosidad"] = perfil["verbosidad"]
        if perfil.get("nombre"):
            estado["nombre"] = perfil["nombre"]
        return estado

    # Lista blanca: la página pide ficheros por nombre, así que sólo estos tres
    # se sirven, y sólo desde el directorio de la cara. Nada de rutas libres.
    JSON_PERMITIDOS = ("models.json", "config.json", "config.example.json")

    def leer_json(self, nombre: str) -> dict:
        """Sirve los .json que la cara pide por fetch (que no puede leer file://)."""
        if nombre not in self.JSON_PERMITIDOS:
            return {"__falta": True, "motivo": f"no permitido: {nombre}"}
        ruta = CARA.parent / nombre
        if not ruta.exists():
            return {"__falta": True, "motivo": f"no existe: {nombre}"}
        try:
            with ruta.open(encoding="utf-8") as f:
                return json.load(f)
        except (OSError, ValueError) as e:
            return {"__falta": True, "motivo": f"{nombre}: {e}"}

    def obtener_preferencia(self) -> dict:
        """Mitad GET de /api/preferencia: lo que haya en profile, o NO_DATA."""
        mem = self.leer_memoria()
        perfil = mem.get("perfil", {}) if isinstance(mem, dict) else {}
        if not perfil:
            return {"estado": "NO_DATA", "motivo": "profile vacío"}
        salida = {"estado": "OK"}
        if perfil.get("language"):
            salida["locale"] = perfil["language"]
        for k in ("verbosidad", "nombre"):
            if perfil.get(k):
                salida[k] = perfil[k]
        return salida

    def guardar_preferencia(self, cuerpo: dict | None = None) -> dict:
        """La cara persiste locale/verbosidad. Van a profile, no a engrams."""
        cuerpo = cuerpo or {}
        pares = [(k, str(v)) for k, v in cuerpo.items()
                 if k in ("locale", "verbosidad", "nombre") and v is not None]
        if not pares:
            return {"ok": False, "error": "nada que guardar"}
        if not MEMORIA.exists():
            return {"ok": False, "error": f"no existe {MEMORIA}"}
        try:
            con = sqlite3.connect(str(MEMORIA), isolation_level=None)
            con.execute("PRAGMA journal_mode=WAL")
            con.execute("BEGIN")
            for k, v in pares:
                clave = "language" if k == "locale" else k
                con.execute(
                    "INSERT INTO profile (key, value, updated_at) VALUES (?, ?, datetime('now')) "
                    "ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=datetime('now')",
                    (clave, v),
                )
            con.execute("COMMIT")
            con.execute("PRAGMA wal_checkpoint(TRUNCATE)")
            con.close()
        except sqlite3.Error as e:
            return {"ok": False, "error": f"sqlite: {e}"}
        return {"ok": True, "guardado": dict(pares)}


# ─────────────────────────────────────────────────────────────────────────────
# Arranque
# ─────────────────────────────────────────────────────────────────────────────
def _registrar_shim(ventana) -> bool:
    """Añade SHIM_JS al UserContentManager de WebKit en document-start.

    `before_show` no sirve: pywebview lo dispara en un hilo aparte y correría
    en carrera con load_uri. Por eso la ventana nace con un HTML mínimo, aquí se
    registra el user script, y sólo después se carga la cara — el shim está
    puesto antes de que exista un solo script de la página.
    """
    from gi.repository import GLib, WebKit2
    from webview.platforms.gtk import BrowserView

    # La instancia del backend se crea en el hilo GUI; este código corre en el
    # hilo de `webview.start(func)` y puede llegar antes. Se espera, no se asume.
    vista = None
    for _ in range(100):
        vista = BrowserView.instances.get(ventana.uid)
        if vista is not None:
            break
        threading.Event().wait(0.1)
    if vista is None:
        return False

    hecho = threading.Event()
    ok = {"v": False}

    def en_hilo_gtk():
        try:
            vista.manager.add_script(WebKit2.UserScript.new(
                SHIM_JS,
                WebKit2.UserContentInjectedFrames.TOP_FRAME,
                WebKit2.UserScriptInjectionTime.START,
                None, None,
            ))
            ok["v"] = True
        except Exception as e:  # noqa: BLE001 — se reporta, no se traga
            print(f"[dashboard] no se pudo registrar el shim: {e}")
        finally:
            hecho.set()
        return False

    GLib.idle_add(en_hilo_gtk)
    hecho.wait(timeout=10)
    return ok["v"]


def _sin_servidor_http() -> bool:
    """Guarda dura de D75: si pywebview levantó su servidor interno, se ve aquí."""
    from webview import http
    return http.global_server is None


def arrancar(ventana) -> None:
    if not _registrar_shim(ventana):
        print("[dashboard] AVISO: shim no registrado — la cara no alcanzará al gerente")
    # file:// NO dispara el servidor interno de pywebview (is_local_url() lo
    # excluye explícitamente), a diferencia de about:blank, que sí lo dispara.
    ventana.load_url(CARA.as_uri())
    if not _sin_servidor_http():
        print("[dashboard] D75 VIOLADO: pywebview levantó su servidor HTTP interno")


def main() -> int:
    for pieza, ruta in (("la cara", CARA), ("el gerente", GERENTE)):
        if not ruta.exists():
            print(f"[dashboard] falta {pieza}: {ruta}")
            return 1

    # La ventana nace con un HTML mínimo, NO con about:blank: `is_local_url()`
    # trata about:blank como url local y eso hace que pywebview levante su
    # servidor HTTP en :42001 (medido). Con `html=` no hay original_url y no hay
    # servidor: ni un socket. Es la diferencia entre cumplir D75 y no cumplirlo.
    ventana = webview.create_window(
        "Aurelius",
        html='<!doctype html><meta charset="utf-8"><title>Aurelius</title>'
             '<body style="margin:0;background:#1a1a1a"></body>',
        js_api=Api(),
        width=1200, height=800,
        resizable=True,
    )
    # private_mode=False para que la cara conserve su localStorage (i18n.js
    # persiste el idioma ahí). http_server=False explícito, por si acaso.
    webview.start(arrancar, ventana, private_mode=False, gui="gtk", http_server=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
