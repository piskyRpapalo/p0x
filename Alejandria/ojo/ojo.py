#!/usr/bin/env python3
"""El Ojo del Soberano · consola de operaciones del rack. Solo loopback.

POR QUE VIVE AQUI Y NO EN EL PRODUCTO
--------------------------------------
El encargo original pedia meter esto en `preceptor/interface/dashboard.html`.
No cabe ahi, por dos razones que no son de estilo:

  * ese dashboard es LA CARA DEL USUARIO -- memoria, frontera, camino, perfil.
    Se sirve a quien instale PreceptorOS. Meterle `OLLAMA :: ONLINE`, el estado
    del Doogee y las latencias de la-fragua es enviar el rack del Soberano a la
    app de cada persona, con IPs de tailnet dentro de un producto cuya promesa
    entera es que el contexto no se escapa.
  * `estado.py` del producto guarda las banderas de INSTALACION, y su propio
    docstring prohibe crear dos verdades sobre el mismo hecho. `/api/estado` ya
    existe sirviendolas.

Asi que el Ojo es suyo: su directorio, su servidor, su puerto. Gana tres cosas
-- cero riesgo para el gate del producto, cero fuga de rack, y puede enseñar
justo lo que el producto nunca debe.

DOS REGLAS DE ESTE SERVIDOR
---------------------------
1. **Solo 127.0.0.1.** No es un detalle de configuracion: la auditoria de hoy
   encontro un `python3 -m http.server` en 0.0.0.0:8080, sin auth y sin logs,
   expuesto a la LAN y a la tailnet entera durante seis horas porque nadie
   miraba la interfaz, solo el numero. Esta consola enseña el rack: si se ata a
   0.0.0.0, lo reparte.
2. **No mide. Pinta.** Sirve lo que `recolector.py` dejo escrito y calcula la
   frescura al vuelo. Un panel que mide al pintar se cuelga justo cuando el
   rack cae -- que es exactamente el momento en que hace falta.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ESTADO = AQUI.parent / "estado.json"

ESTATICOS = {
    "/": ("ojo.html", "text/html; charset=utf-8"),
    # El Ojo-Vivo convive con la consola de texto en vez de sustituirla: la
    # de texto se lee por SSH y en una terminal, el refugio no.
    "/vivo": ("vivo.html", "text/html; charset=utf-8"),
    "/vivo.html": ("vivo.html", "text/html; charset=utf-8"),
    "/vivo.css": ("vivo.css", "text/css; charset=utf-8"),
    "/vivo.js": ("vivo.js", "application/javascript; charset=utf-8"),
    "/ojo.html": ("ojo.html", "text/html; charset=utf-8"),
    "/ojo.css": ("ojo.css", "text/css; charset=utf-8"),
    "/ojo.js": ("ojo.js", "application/javascript; charset=utf-8"),
    "/glosario.js": ("glosario.js", "application/javascript; charset=utf-8"),
    "/acta.js": ("acta.js", "application/javascript; charset=utf-8"),
    "/digesto.js": ("digesto.js", "application/javascript; charset=utf-8"),
}

CAPA = AQUI.parent
GLOSARIO = AQUI / "glosario.json"
FASES = CAPA / "fases.json"
IDENTIDAD = CAPA / "identidad_publica.json"
ACTA = CAPA / "mensajes" / "mensajes.jsonl"
DIGESTOS = CAPA / "digesto"


class Ojo(BaseHTTPRequestHandler):
    server_version = "Ojo/1.0"

    def log_message(self, fmt, *args):
        pass  # sin ruido en la terminal del Soberano

    def _responder(self, codigo, cuerpo, tipo):
        if isinstance(cuerpo, str):
            cuerpo = cuerpo.encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(cuerpo)))
        # Nada de cache: un panel de estado cacheado es un panel que miente.
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(cuerpo)

    def _fichero_json(self, ruta, nombre, causa, remedio=None):
        """Sirve un JSON de disco tal cual, o declara por que no puede."""
        if not ruta.exists():
            return self._json(200, {"estado": "NO_DATA", "causa": causa,
                                    "remedio": remedio or f"crear {nombre}"})
        try:
            return self._responder(200, ruta.read_bytes(),
                                   "application/json; charset=utf-8")
        except OSError as e:
            return self._json(200, {"estado": "NO_DATA",
                                    "causa": f"{type(e).__name__}"})

    def _json(self, codigo, datos):
        self._responder(codigo, json.dumps(datos, ensure_ascii=False),
                        "application/json; charset=utf-8")

    def do_GET(self):
        ruta = self.path.split("?")[0]

        if ruta == "/api/rack":
            if not ESTADO.exists():
                return self._json(200, {
                    "estado": "NO_DATA",
                    "causa": f"no existe {ESTADO.name}",
                    "remedio": "~/p0x/Alejandria/verificar_sesion.sh",
                    "frescura_segundos": None})
            try:
                d = json.loads(ESTADO.read_text(encoding="utf-8"))
            except ValueError as e:
                return self._json(200, {
                    "estado": "NO_DATA",
                    "causa": f"estado.json ilegible: {e}",
                    "remedio": "~/p0x/Alejandria/verificar_sesion.sh",
                    "frescura_segundos": None})
            # La frescura es un CAMPO, no un adorno de la pantalla: asi el
            # script y el panel no pueden discrepar sobre si el dato esta viejo.
            d["frescura_segundos"] = int(time.time() - d.get("epoch", 0))
            return self._json(200, d)

        if ruta == "/api/glosario":
            return self._fichero_json(GLOSARIO, "glosario.json",
                                      "no hay glosario en esta consola")

        if ruta == "/api/acta":
            # La cadena se verifica AL SERVIR, no al escribir solamente. Un
            # acta se rompe editando el fichero por fuera, y eso no pasa por
            # ninguna funcion de escritura: si no se comprueba aqui, no se
            # comprueba nunca en la pantalla de quien la lee.
            sys.path.insert(0, str(CAPA / "mensajes"))
            try:
                import mensajes as M
                problemas = M.verificar(ACTA)
                return self._json(200, {"estado": "OK",
                                        "mensajes": M.leer(ACTA),
                                        "cadena_sana": not problemas,
                                        "problemas": problemas})
            except Exception as e:                 # noqa: BLE001
                return self._json(200, {
                    "estado": "NO_DATA", "causa": f"{type(e).__name__}: {e}",
                    "remedio": "python3 ~/p0x/Alejandria/test_alejandria.py"})

        if ruta == "/api/fases":
            return self._fichero_json(
                FASES, "fases.json",
                "no existe fases.json; es SALIDA de continuidad.db, no un "
                "fichero escrito a mano",
                remedio="python3 ~/p0x/Alejandria/fases.py")

        if ruta == "/api/identidad":
            # Lo unico de esta consola pensado para ser publico. Va envuelto
            # en {"identidad": ...} y no crudo: asi el fichero puede crecer
            # con claves nuevas sin que el render tenga que adivinar si lo
            # que le llega es el dato o el parte de que no lo hay.
            if not IDENTIDAD.exists():
                return self._json(200, {
                    "estado": "NO_DATA",
                    "causa": "no existe identidad_publica.json",
                    "remedio": "crear ~/p0x/Alejandria/identidad_publica.json"})
            try:
                datos = json.loads(IDENTIDAD.read_text(encoding="utf-8"))
            except (OSError, ValueError) as e:
                return self._json(200, {
                    "estado": "NO_DATA",
                    "causa": f"identidad_publica.json ilegible: {e}",
                    "remedio": "revisar el JSON a mano"})
            return self._json(200, {"estado": "OK", "identidad": datos,
                                    "fuente": "identidad_publica.json"})

        if ruta == "/api/companero":
            # El compañero ACTIVO no tiene fuente todavia. Devolver aqui un
            # "Instalador" a secas seria fabricar el dato: el panel diria que
            # el Soberano eligio compañero cuando nadie ha elegido nada.
            # Lo que si es contrato --el compañero POR DEFECTO-- se sirve, y
            # lo elegido se declara NO_DATA con su causa.
            return self._json(200, {
                "estado": "OK",
                "por_defecto": "el Instalador",
                "elegido": None,
                "causa": "ninguna fuente registra el compañero elegido",
                "nota": "El Centro esta dibujado; hablar con el companero es "
                        "V4 («centro vivo») del contrato visual. Hasta "
                        "entonces esto declara el hueco en vez de rellenarlo."})

        if ruta == "/api/digesto":
            ds = sorted(DIGESTOS.glob("digesto-*.md")) if DIGESTOS.exists() else []
            if not ds:
                return self._json(200, {
                    "estado": "NO_DATA", "causa": "todavia no hay ningun digesto",
                    "remedio": "~/p0x/Alejandria/verificar_sesion.sh"})
            ult = ds[-1]
            texto = ult.read_text(encoding="utf-8")
            cuerpo = texto.split("## Los hechos", 1)[0]
            return self._json(200, {
                "estado": "OK", "fichero": ult.name,
                "frescura_segundos": int(time.time() - ult.stat().st_mtime),
                "bronze": "BRONZE · en cuarentena" in texto,
                "cuerpo": cuerpo.split("\n", 4)[-1].strip()})

        pieza = ESTATICOS.get(ruta)
        if not pieza:
            return self._json(404, {"estado": "NO_DATA", "causa": "aqui no vive eso"})
        try:
            crudo = (AQUI / pieza[0]).read_bytes()
        except OSError as e:
            return self._json(500, {"estado": "NO_DATA",
                                    "causa": f"{type(e).__name__}"})
        return self._responder(200, crudo, pieza[1])


def comprobar():
    """Dice si el Ojo puede servir, SIN abrir un puerto. Devuelve 0 o 1.

    Responde UNA pregunta --¿esta entero lo que hay que servir?-- y deja la
    otra --¿arranca el servidor?-- para quien lo arranque. Mezclarlas es lo que
    hacia que un fallo no dijese cual de las dos habia fallado.

    Un fichero que falta NO se convierte en un cero ni en un aviso suave: sale
    NO_DATA con su causa, y el codigo de salida lo repite para que un gate
    pueda leerlo sin parsear texto.
    """
    filas = []
    # Las tres piezas de la topologia V1 del contrato visual. Se nombran una a
    # una a proposito: si manana desaparece `vivo.css`, el Ojo seguiria
    # devolviendo 200 en todas las rutas y sirviendo un esqueleto sin estilo.
    for nombre, _ in sorted({v for v in ESTATICOS.values()}):
        ruta = AQUI / nombre
        filas.append((nombre, ruta.is_file(), ruta.stat().st_size if ruta.is_file() else 0,
                      "fichero estatico"))
    # Las fuentes de datos. Que falten NO impide servir: el Ojo pinta NO_DATA.
    # Por eso se declaran aparte y no cuentan para el codigo de salida.
    fuentes = [("estado.json", ESTADO), ("fases.json", FASES),
               ("glosario.json", GLOSARIO), ("identidad_publica.json", IDENTIDAD),
               ("mensajes.jsonl", ACTA)]

    ancho = max(len(n) for n, *_ in filas)
    print("== lo que el Ojo tiene que servir ==")
    faltan = 0
    for nombre, hay, tam, _ in filas:
        if hay:
            print(f"  MEDIDO   {nombre:<{ancho}}  {tam} B")
        else:
            faltan += 1
            print(f"  NO_DATA  {nombre:<{ancho}}  no existe en {AQUI}")

    print("== las fuentes que lee (su ausencia se pinta, no rompe) ==")
    for nombre, ruta in fuentes:
        existe = Path(str(ruta)).is_file()
        print(f"  {'MEDIDO ' if existe else 'NO_DATA'}  {nombre}"
              + ("" if existe else "  · el Ojo lo declarara en pantalla"))

    if faltan:
        print(f"NO SIRVE · faltan {faltan} pieza(s) de la topologia V1")
        return 1
    print(f"SIRVE · {len(filas)} piezas presentes")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true",
                    help="dice si el Ojo puede servir y sale; no abre puerto")
    ap.add_argument("--puerto", type=int, default=8790)
    a = ap.parse_args(argv)

    # `--check` responde y sale: no abre puerto, asi que puede vivir en un
    # gate sin ocupar un puerto ni dejar un proceso suelto.
    if a.check:
        return comprobar()
    # 127.0.0.1 clavado y sin bandera para cambiarlo. Una consola que enseña el
    # rack no debe poder atarse a 0.0.0.0 "sin querer".
    srv = ThreadingHTTPServer(("127.0.0.1", a.puerto), Ojo)
    print(f"👁  El Ojo del Soberano · http://127.0.0.1:{a.puerto}/  (Ctrl-C para cerrar)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\ncerrado")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
