#!/usr/bin/env python3
"""Mide el metal del nodo soberano y lo deja en JSON. Solo lectura, stdlib pura.

POR QUE EXISTE ESTE FICHERO
---------------------------
El recolector anterior (`volcar_estado.sh`) fabricaba rojos que no existian, y
cada sesion los heredaba como si fueran problemas del rack:

  * preguntaba `systemctl --user` por `api-guia`, que es unidad de SISTEMA;
  * medía `is-active` en unidades `Type=oneshot`, donde «inactive» es el estado
    SANO entre disparos;
  * comparaba un timer semanal (curador, domingos) contra dos diarios y
    concluia que llevaba cinco dias caido;
  * llamaba a `ollama` sin `OLLAMA_HOST`, que vivia en `.bashrc` -- fichero que
    ningun proceso desatendido lee.

Ninguno de esos cuatro rojos era del rack. Los cuatro eran del termometro. Por
eso la primera responsabilidad de este modulo no es medir mucho: es **medir la
propiedad correcta** y no poder mentir en silencio.

LA ESCALA DE ESTADOS, DEFINIDA UNA VEZ
--------------------------------------
Tres valores y ninguno mas. Un componente tiene exactamente uno:

  OK       lo medido responde y es lo esperado.
  RED      lo medido responde y NO es lo esperado. `causa` OBLIGATORIA.
  NO_DATA  no se pudo medir. `causa` Y `remedio` OBLIGATORIOS.

La diferencia entre RED y NO_DATA no es de matiz: RED es un hecho del rack,
NO_DATA es un limite del observador. Confundirlos es como se acaba
persiguiendo fantasmas -- y `_declarar()` lo hace cumplir por construccion.

DOS VELOCIDADES, Y POR QUE
---------------------------
Los gates cuestan ~10 s de CPU. Correrlos cada 15 minutos son 96 `pytest` al
dia quemando la CPU que necesita el entrenamiento, y el canon del nodo ya dice
que el enjambre y el entrenamiento no se tocan a la vez. Asi que:

  --rapido    (por defecto) puertos, ollama, servicios, doogee, memoria. ~2 s.
              Los gates se ARRASTRAN de la ultima corrida completa, y viajan
              con su edad al lado: un dato viejo declarado como viejo sigue
              siendo un dato; un dato viejo disfrazado de fresco es una mentira.
  --completo  ademas corre los dos gates. Es el modo del cierre de sesion.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

CASA = Path.home()
RAIZ = CASA / "p0x" / "Alejandria"
SALIDA = RAIZ / "estado.json"
HISTORIAL = RAIZ / "historial"

REPO_MVP = CASA / "p0x" / "preceptor"
REPO_WEB = CASA / "preceptoros-web"
def _casa_del_producto():
    """Donde vive la memoria, PREGUNTANDOSELO al producto.

    Escrito a mano decia `~/.aurelius`, que tras la mudanza del 2026-08-30 es un
    symlink de compatibilidad. Habria seguido funcionando -- y ese es justo el
    problema: el informe habria enseñado durante meses la ruta vieja como si
    fuera la verdad, y nadie se habria enterado hasta que alguien borrase el
    symlink. `casa.raiz()` es el unico sitio del proyecto que decide esto.
    """
    try:
        sys.path.insert(0, str(CASA / "p0x" / "preceptor"))
        import casa as _casa
        return _casa.raiz() / "memory.db"
    except Exception:                              # noqa: BLE001
        # Si el producto no se puede importar, se declara y se sigue: el resto
        # del rack no depende de esto.
        return None


MEMORIA = _casa_del_producto()
LATIDOS = (MEMORIA.parent / "loops.db") if MEMORIA else None

ENV_P0X = CASA / ".config" / "environment.d" / "50-p0x.conf"


def _host_ollama():
    """De donde sale OLLAMA_HOST, en orden, y por que hay mas de un sitio.

    1. El entorno del proceso. Es lo normal bajo systemd, que lee environment.d.
    2. El propio `50-p0x.conf`, LEIDO A MANO.
    3. NO_DATA.

    El paso 2 no es redundancia por si acaso: es la leccion de esta misma
    sesion. Una shell NO interactiva no carga `.bashrc` y tampoco hereda
    environment.d si no la lanzo el manager de usuario, asi que el recolector
    se quedaba ciego segun QUIEN lo invocase -- el mismo comando daba OK desde
    un timer y NO_DATA desde un script. Un termometro cuya lectura depende de
    quien lo sostiene no es un termometro.

    Lo que NO se hace nunca es caer a localhost: el canon del nodo lo prohibe
    explicitamente, y fingir una medicion es peor que declarar el hueco.
    """
    del_entorno = os.environ.get("OLLAMA_HOST", "").strip()
    if del_entorno:
        return del_entorno.rstrip("/"), "entorno"
    try:
        for linea in ENV_P0X.read_text(encoding="utf-8").splitlines():
            linea = linea.strip()
            if linea.startswith("OLLAMA_HOST="):
                valor = linea.partition("=")[2].strip().strip('"').strip("'")
                if valor:
                    return valor.rstrip("/"), f"leido de {ENV_P0X.name}"
    except OSError:
        pass
    return "", "ninguna"


OLLAMA, OLLAMA_ORIGEN = _host_ollama()

ENJAMBRE = ("guardian", "curador", "afinador")

# Los cuatro arboles de trabajo. La rama NO se escribe: se pregunta. El volcado
# viejo comparaba contra `origin/main` a mano y p0x esta en `master`, asi que
# para ese repo la cuenta de commits sin empujar era literalmente incomparable
# -- y salia como si estuviera todo al dia.
REPOS = (CASA / "p0x", CASA / "p0x" / "preceptor", CASA / "preceptoros-web",
         CASA / "p0x" / "preceptor-internal")

# Loopback y nada mas. Todo lo que no este aqui esta expuesto a la LAN y a la
# tailnet, y merece decirse en voz alta.
LOCALES = ("127.", "::1", "[::1]")

# Puertos que SE ESPERA que esten expuestos, con su motivo. Sin esta lista, el
# recolector marcaba en rojo los nueve puertos expuestos del nodo -- incluidos
# sshd, el demonio de la red superpuesta y el propio Ollama, que estan
# expuestos a proposito y por canon. Nueve rojos permanentes son cero rojos:
# a la tercera sesion nadie los
# mira, y el dia que aparezca uno de verdad se pierde entre ellos.
#
# Lo que esta lista permite es que el rojo signifique SORPRESA.
EXPUESTOS_ESPERADOS = {
    22: "sshd",
    53: "systemd-resolved",
    443: "demonio de la red superpuesta (DERP/HTTPS)",
    631: "cups",
    9001: "API Guia",
    11434: "Ollama (canon: escucha en la IP de tailnet, nunca en localhost)",
}

# El rango efimero no cuenta como sorpresa. Un puerto >= 32768 no es un
# servicio que alguien dejo encendido: es una asignacion dinamica del kernel --
# aqui, el demonio de la red superpuesta abriendo sus escuchas. Meterlos en la
# lista de sorpresas
# haria que el numero cambiase solo entre corridas y volveria el rojo inutil.
# Se siguen listando; simplemente no disparan la alarma.
EFIMERO_DESDE = 32768


# --------------------------------------------------------------------------
# Utilidades: nunca lanzan, siempre devuelven algo que se puede declarar.
# --------------------------------------------------------------------------

def _corre(cmd, timeout=10, cwd=None):
    """Ejecuta y devuelve (ok, salida). Un fallo es un dato, no una excepcion."""
    try:
        p = subprocess.run(cmd, capture_output=True, text=True,
                           timeout=timeout, cwd=cwd)
        return p.returncode == 0, (p.stdout or "") + (p.stderr or "")
    except FileNotFoundError:
        return False, "binario no encontrado"
    except subprocess.TimeoutExpired:
        return False, f"timeout tras {timeout}s"
    except OSError as e:
        return False, f"{type(e).__name__}: {e}"


def _declarar(estado, **campos):
    """Construye un bloque de componente e impone la escala.

    Un RED sin causa o un NO_DATA sin remedio no se dejan pasar en silencio: se
    marcan como defecto DEL RECOLECTOR. Preferimos un informe que se acuse a si
    mismo antes que uno que presente un hueco como si fuera una medicion.
    """
    bloque = {"estado": estado}
    bloque.update({k: v for k, v in campos.items() if v is not None})
    if estado == "RED" and not bloque.get("causa"):
        bloque["causa"] = "SIN CAUSA DECLARADA (defecto del recolector)"
    if estado == "NO_DATA":
        bloque.setdefault("causa", "SIN CAUSA DECLARADA (defecto del recolector)")
        bloque.setdefault("remedio", "SIN REMEDIO DECLARADO (defecto del recolector)")
    return bloque


def _prop(unidad, propiedades, usuario=True):
    """Lee propiedades de una unidad systemd como diccionario."""
    base = ["systemctl"] + (["--user"] if usuario else [])
    cmd = base + ["show", unidad, "--no-pager"]
    for p in propiedades:
        cmd += ["-p", p]
    ok, salida = _corre(cmd, timeout=8)
    if not ok:
        return {}
    datos = {}
    for linea in salida.splitlines():
        if "=" in linea:
            k, _, v = linea.partition("=")
            datos[k.strip()] = v.strip()
    return datos


# --------------------------------------------------------------------------
# Sondas
# --------------------------------------------------------------------------

def sonda_ollama():
    if not OLLAMA:
        return _declarar(
            "NO_DATA",
            causa="OLLAMA_HOST no esta ni en el entorno ni en "
                  f"{ENV_P0X}",
            remedio="escribir OLLAMA_HOST en ese fichero y "
                    "'systemctl --user daemon-reexec'")
    url = f"{OLLAMA}/api/tags"
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(url, timeout=8) as r:
            datos = json.loads(r.read().decode("utf-8"))
    except (urllib.error.URLError, OSError, ValueError) as e:
        return _declarar("RED", causa=f"{type(e).__name__} contra {url}",
                         host=OLLAMA)
    ms = round((time.perf_counter() - t0) * 1000, 2)

    # El inventario NO se filtra por nombre. El recolector viejo hacia
    # `grep -E "preceptor|qwen|llama"` y por eso escondia justo los modelos con
    # nombre nuevo: la §1 del snapshot decia 8 y la §6 decia 7, en el mismo
    # fichero, sin que nadie lo notara.
    modelos = sorted(m.get("name", "?") for m in datos.get("models", []))

    residentes = []
    ok, salida = _corre(["ollama", "ps"], timeout=8)
    if ok:
        for linea in salida.splitlines()[1:]:
            if linea.strip():
                residentes.append(linea.split()[0])

    return _declarar("OK", host=OLLAMA, origen_host=OLLAMA_ORIGEN, latencia_ms=ms,
                     modelos=len(modelos), nombres=modelos,
                     residentes=residentes, backend=_backend_ollama())


def _backend_ollama():
    """Vulkan o CPU. El canon obliga a anotarlo al arrancar sesion.

    No se deduce del hardware: se lee el drop-in de la unidad, que es lo que
    decide de verdad y lo que puede cambiar entre sesiones.
    """
    ok, salida = _corre(["systemctl", "show", "ollama", "--no-pager",
                         "-p", "Environment"], timeout=8)
    if ok and "OLLAMA_IGPU_ENABLE=1" in salida:
        return "vulkan (OLLAMA_IGPU_ENABLE=1 en la unidad)"
    ok2, drop = _corre(["bash", "-lc",
                        "cat /etc/systemd/system/ollama.service.d/*.conf 2>/dev/null"],
                       timeout=8)
    if ok2 and "OLLAMA_IGPU_ENABLE=1" in drop:
        return "vulkan (OLLAMA_IGPU_ENABLE=1 en drop-in)"
    return "NO_DATA (sin OLLAMA_IGPU_ENABLE visible)"


def sonda_api_guia():
    """Reconciliada: es unidad de SISTEMA, no de usuario.

    El recolector viejo preguntaba `systemctl --user api-guia` y el manager de
    usuario respondia que no la conoce -- que es cierto y no significa nada. Se
    consultan los dos managers y se dice cual la tiene.
    """
    gestor, activo = None, None
    for usuario in (False, True):
        d = _prop("api-guia", ["ActiveState", "SubState", "FragmentPath"], usuario)
        if d.get("FragmentPath"):
            gestor = "user" if usuario else "system"
            activo = d.get("ActiveState")
            break

    # Dos candidatos, y ninguno escrito a mano: loopback, y el MISMO host que ya
    # usa Ollama con el puerto cambiado. La direccion del rack vive en
    # environment.d, no en el codigo -- asi solo hay un sitio que tocar el dia
    # que cambie, y el guardia de higiene no encuentra IPs que filtrar.
    candidatos = ["http://127.0.0.1:9001"]
    if OLLAMA:
        candidatos.append(re.sub(r":\d+$", ":9001", OLLAMA))
    puerto_vivo, url_viva = False, None
    for base in candidatos:
        try:
            with urllib.request.urlopen(f"{base}/docs", timeout=5) as r:
                if r.status == 200:
                    puerto_vivo, url_viva = True, base
                    break
        except Exception:
            continue

    if puerto_vivo:
        return _declarar("OK", puerto=9001, gestor=gestor or "NO_DATA",
                         alcanzado_en="loopback" if "127." in (url_viva or "") else "tailnet",
                         unidad=activo or "sin unidad (proceso suelto)")
    if activo == "active":
        return _declarar("RED", causa="la unidad dice active pero :9001 no responde",
                         gestor=gestor)
    return _declarar("RED", causa=f"unidad {activo or 'ausente'} y :9001 sin respuesta",
                     gestor=gestor or "ninguno",
                     remedio="systemctl status api-guia")


def sonda_enjambre():
    """Salud real de unidades oneshot: Result, no is-active.

    `is-active` sobre un oneshot devuelve «inactive» SIEMPRE que no este
    corriendo en ese instante, que es el 99,99% del tiempo. Es la propiedad que
    no informa. Lo que informa es si la ultima corrida salio bien y cuando toca
    la siguiente.

    Y `cadencia` viaja como campo de primera clase porque el rojo falso del
    curador nacio de comparar un timer SEMANAL contra dos diarios. Con la
    cadencia delante, esa comparacion no se puede volver a hacer mal.
    """
    fuera = {}
    for nombre in ENJAMBRE:
        svc = _prop(f"{nombre}.service",
                    ["Result", "ExecMainStatus", "ExecMainStartTimestamp",
                     "ActiveState"])
        tim = _prop(f"{nombre}.timer",
                    ["NextElapseUSecRealtime", "LastTriggerUSec", "UnitFileState"])
        ok, cal = _corre(["systemctl", "--user", "cat", f"{nombre}.timer"], timeout=8)
        cadencia = "NO_DATA"
        if ok:
            m = re.search(r"^OnCalendar=(.+)$", cal, re.M)
            if m:
                crudo = m.group(1).strip()
                dia = re.match(r"^(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\b", crudo)
                cadencia = f"semanal ({dia.group(1)}) · {crudo}" if dia else f"diaria · {crudo}"

        resultado = svc.get("Result", "")
        arranque = svc.get("ExecMainStartTimestamp", "") or None

        # EL LATIDO MANDA SOBRE systemd.
        #
        # `Result=success` solo dice que el proceso salio con codigo 0. No dice
        # si HIZO algo. Medido el 2026-08-30: el guardian llevaba dos corridas
        # devolviendo `success` con «0 ficheros mirados» porque su arbol
        # vigilado habia dejado de existir -- y este recolector lo pintaba
        # SANO en el Ojo, sesion tras sesion.
        #
        # Es el tercer agujero del mismo tipo en esta capa, y siempre el mismo:
        # medir la propiedad que no informa. El bucle deja su propio latido con
        # su resultado y su nota; eso es lo que hay que leer.
        latido = _ultimo_latido(nombre)
        if latido:
            if latido.get("resultado") and latido["resultado"] != "ok":
                fuera[nombre] = _declarar(
                    "RED", causa=f"su ultimo latido dice '{latido['resultado']}': "
                                 f"{latido.get('nota') or 'sin nota'}",
                    cadencia=cadencia, ultima=latido.get("cuando"),
                    nota_latido=latido.get("nota"),
                    proxima=tim.get("NextElapseUSecRealtime") or "NO_DATA")
                continue

        if not svc:
            fuera[nombre] = _declarar("NO_DATA",
                                      causa="la unidad no existe en el manager de usuario",
                                      remedio=f"systemctl --user status {nombre}")
        elif resultado and resultado != "success":
            fuera[nombre] = _declarar("RED", causa=f"Result={resultado}",
                                      cadencia=cadencia, ultima=arranque)
        else:
            fuera[nombre] = _declarar(
                "OK", resultado=resultado or "success", cadencia=cadencia,
                ultima=arranque or "sin corridas en este arranque",
                proxima=tim.get("NextElapseUSecRealtime") or "NO_DATA",
                timer=tim.get("UnitFileState", "NO_DATA"),
                nota_latido=(latido or {}).get("nota"),
                # Un oneshot sano esta inactive entre disparos. Se dice aqui
                # para que nadie vuelva a leerlo como una caida.
                nota="oneshot: 'inactive' entre disparos es el estado sano")
    return fuera


def _ultimo_latido(nombre):
    """El ultimo latido de salida de un bucle, en solo lectura.

    Devuelve {resultado, nota, cuando} o None. `mode=ro` no es cortesia: los
    latidos son append-only por cuatro disparadores de SQLite, y abrir en
    escritura para leer es pedirle al motor que nos deje romper su promesa.
    """
    if not LATIDOS or not LATIDOS.exists():
        return None
    try:
        import sqlite3
        con = sqlite3.connect(f"file:{LATIDOS}?mode=ro", uri=True, timeout=5)
        fila = con.execute(
            "select resultado, nota, datetime(momento,'unixepoch','localtime') "
            "from latidos where bucle=? and evento='sale' "
            "order by momento desc limit 1", (nombre,)).fetchone()
        con.close()
    except Exception:                              # noqa: BLE001
        return None
    if not fila:
        return None
    return {"resultado": fila[0], "nota": fila[1], "cuando": fila[2]}


def sonda_puertos():
    """Puertos a la escucha, distinguiendo loopback de expuesto.

    El numero de puerto solo no dice nada. Un `http.server` en 0.0.0.0:8080 sin
    auth, sin logs y sin supervision estuvo seis horas invisible porque todo el
    mundo miraba el numero y nadie la interfaz.
    """
    ok, salida = _corre(["ss", "-tlnp"], timeout=8)
    if not ok:
        return _declarar("NO_DATA", causa="ss no disponible o sin permisos",
                         remedio="ss -tlnp")
    filas, expuestos, sorpresas = [], 0, []
    for linea in salida.splitlines()[1:]:
        partes = linea.split()
        if len(partes) < 4:
            continue
        addr = partes[3]
        proc = partes[-1] if "users:" in partes[-1] else ""
        proc = re.sub(r'users:\(\("([^"]+)",pid=(\d+).*', r"\1 pid=\2", proc) or "NO_DATA"
        local = any(addr.startswith(p) for p in LOCALES)
        try:
            puerto = int(addr.rsplit(":", 1)[1])
        except (IndexError, ValueError):
            puerto = 0
        esperado = puerto in EXPUESTOS_ESPERADOS or puerto >= EFIMERO_DESDE
        if not local:
            expuestos += 1
            if not esperado:
                sorpresas.append({"addr": addr, "proceso": proc, "puerto": puerto})
        filas.append({"addr": addr, "expuesto": not local, "proceso": proc,
                      "puerto": puerto,
                      "motivo": (EXPUESTOS_ESPERADOS.get(puerto) or
                                 ("rango efimero del kernel" if puerto >= EFIMERO_DESDE else None))
                                if not local else None})

    huerfanos = _servidores_huerfanos()

    causa = None
    if sorpresas:
        causa = ("puerto expuesto fuera de la lista esperada: " +
                 ", ".join(f"{x['addr']} ({x['proceso']})" for x in sorpresas))
    elif huerfanos:
        causa = (f"{len(huerfanos)} servidor(es) http.server huerfanos: su shell "
                 "murio y quedaron reparentados")

    return _declarar("RED" if causa else "OK", causa=causa,
                     total=len(filas), expuestos=expuestos,
                     sorpresas=sorpresas or None,
                     huerfanos=huerfanos or None, lista=filas)


def _servidores_huerfanos():
    """`http.server` cuyo shell murio y quedaron reparentados a systemd/init.

    Existe esta sonda porque la primera corrida del Ojo destapo CATORCE, en
    puertos 8792-8808, sirviendo `preceptoros-web/public`, algunos con siete
    horas de vida. Uno por sesion: cada una levantaba su previsualizacion de la
    web y ninguna la apagaba. Nadie lo sabia porque estaban en loopback y
    porque nadie mira `ss` entero.

    Es el «servicio fantasma» del canon, pero por la puerta de atras: sin
    unidad, sin firma y sin registro. Un proceso que sobrevive al shell que lo
    lanzo es exactamente lo que nadie recuerda haber arrancado.
    """
    ok, salida = _corre(["bash", "-lc",
                         "ps -eo pid,ppid,etimes,args --no-headers 2>/dev/null "
                         "| grep -F 'http.server' | grep -v grep"], timeout=8)
    if not ok:
        return []

    # Un proceso DESACOPLADO no es lo mismo que un proceso ABANDONADO.
    # `bin/preview-web` se desacopla a proposito -- asi sobrevive a la terminal
    # que lo lanzo -- pero deja fichero de pid y tiene `--stop`. Si el
    # recolector lo contase como huerfano, la herramienta que se escribio para
    # curar esta plaga apareceria cada dia como uno de sus casos, y a la tercera
    # vez nadie mira la linea. Lo que define al huerfano es que NADIE responda
    # por el, no que su padre sea init.
    gestionados = set()
    for base in (os.environ.get("XDG_RUNTIME_DIR", "/tmp"), "/tmp"):
        try:
            crudo = Path(base, "p0x-preview-web.pid").read_text(encoding="utf-8")
            gestionados.add(int(crudo.strip()))
        except (OSError, ValueError):
            pass

    fuera = []
    for linea in salida.splitlines():
        campos = linea.split(None, 3)
        if len(campos) < 4:
            continue
        pid, ppid, etimes, args = campos
        # ppid 1 (init) o el manager de usuario: su padre real ya no existe.
        try:
            padre_vivo = int(ppid) > 1 and "systemd" not in Path(
                f"/proc/{ppid}/comm").read_text(encoding="utf-8", errors="replace")
        except OSError:
            padre_vivo = False
        if not padre_vivo and int(pid) not in gestionados:
            fuera.append({"pid": int(pid), "edad_s": int(etimes),
                          "cmd": args.strip()})
    return fuera


def sonda_memoria():
    """Cuenta engramas SIN tocar la base. `mode=ro` no es cortesia: es la regla."""
    if MEMORIA is None:
        return _declarar("NO_DATA",
                         causa="no se pudo importar casa.py del producto",
                         remedio="comprobar ~/p0x/preceptor/casa.py")
    if not MEMORIA.exists():
        return _declarar("NO_DATA", causa=f"{MEMORIA} no existe",
                         remedio="python3 ~/p0x/preceptor/preceptoros.py --view")
    try:
        import sqlite3
        con = sqlite3.connect(f"file:{MEMORIA}?mode=ro", uri=True, timeout=5)
        tablas = {r[0] for r in con.execute(
            "select name from sqlite_master where type='table'")}
        cuenta = {}
        for t in ("engrams", "turnos", "salidas", "profile", "proyectos"):
            if t in tablas:
                cuenta[t] = con.execute(f"select count(*) from {t}").fetchone()[0]
        con.close()
    except Exception as e:
        return _declarar("NO_DATA", causa=f"{type(e).__name__}: {e}",
                         remedio="comprobar que memory.db no esta bloqueada")
    return _declarar("OK", ruta=str(MEMORIA), engramas=cuenta.get("engrams", 0),
                     fts="engrams_fts" in tablas, tablas=sorted(cuenta.items()),
                     tamano_b=MEMORIA.stat().st_size)


def sonda_doogee():
    ok, salida = _corre(["adb", "devices"], timeout=12)
    if not ok:
        return _declarar("NO_DATA", causa="adb no responde",
                         remedio="adb devices")
    for linea in salida.splitlines()[1:]:
        if "\t" in linea:
            serial, estado = linea.split("\t")[:2]
            estado = estado.strip()
            if estado == "device":
                return _declarar("OK", serial=serial.strip(), conexion="device")
            return _declarar("RED", causa=f"adb dice '{estado}'",
                             serial=serial.strip())
    return _declarar("NO_DATA", causa="ningun dispositivo en 'adb devices'",
                     remedio="conectar el Doogee y autorizar la depuracion USB")


def sonda_tailscale():
    ok, salida = _corre(["tailscale", "status", "--json"], timeout=10)
    if not ok:
        return _declarar("NO_DATA", causa="tailscale no responde",
                         remedio="tailscale status")
    try:
        d = json.loads(salida)
    except ValueError as e:
        return _declarar("NO_DATA", causa=f"json ilegible: {e}",
                         remedio="tailscale status --json")
    pares = d.get("Peer") or {}
    online = sorted(p.get("HostName", "?") for p in pares.values() if p.get("Online"))
    offline = sorted(p.get("HostName", "?") for p in pares.values() if not p.get("Online"))
    return _declarar("OK", total=len(pares), online=len(online),
                     nodos_online=online, nodos_offline=offline)


def sonda_disco():
    u = shutil.disk_usage(str(CASA))
    libre_gb = round(u.free / 2**30, 1)
    estado = "OK" if libre_gb > 20 else "RED"
    return _declarar(estado, libre_gb=libre_gb,
                     total_gb=round(u.total / 2**30, 1),
                     causa=None if estado == "OK" else f"solo {libre_gb} GB libres")


def sonda_lora():
    """Que adaptadores estan servidos. Depende de la sonda de Ollama."""
    o = sonda_ollama() if OLLAMA else None
    if not o or o["estado"] != "OK":
        return _declarar("NO_DATA", causa="Ollama no responde, no hay que inventariar",
                         remedio="arreglar Ollama primero")
    adaptadores = [n for n in o.get("nombres", []) if "preceptor" in n]
    if not adaptadores:
        return _declarar("RED", causa="ningun modelo con 'preceptor' en el nombre",
                         servidos=o.get("nombres", []))
    return _declarar("OK", adaptadores=adaptadores)


def sonda_repos():
    """Commits sin empujar y suciedad, por arbol.

    Se resuelve la rama de seguimiento con `@{upstream}` en vez de suponer
    `origin/main`. Suponerla es como el volcado viejo daba p0x por limpio: esta
    en `master`, la comparacion no existia, y el cero significaba «no lo se»
    disfrazado de «no hay nada pendiente».

    Y `rev-list` mide contra la copia LOCAL de la rama remota. Si nadie ha
    hecho fetch, un cero sigue significando «que yo sepa». Por eso viaja
    `fetch_edad_s`: un cero con una referencia de hace tres dias no es la misma
    afirmacion que un cero recien comprobado.
    """
    fuera, pendientes = {}, 0
    for ruta in REPOS:
        if not (ruta / ".git").exists():
            fuera[ruta.name] = {"estado": "NO_DATA", "causa": "no es repo git"}
            continue
        ok_r, rama = _corre(["git", "-C", str(ruta), "rev-parse",
                             "--abbrev-ref", "HEAD"], timeout=8)
        ok_u, arriba = _corre(["git", "-C", str(ruta), "rev-parse",
                               "--abbrev-ref", "@{upstream}"], timeout=8)
        rama, arriba = rama.strip(), arriba.strip()
        if not ok_u:
            fuera[ruta.name] = {"rama": rama, "estado": "NO_DATA",
                                "causa": "la rama no tiene upstream"}
            continue
        ok_n, n = _corre(["git", "-C", str(ruta), "rev-list", "--count",
                          f"{arriba}..HEAD"], timeout=10)
        ok_s, sucio = _corre(["git", "-C", str(ruta), "status", "--porcelain"],
                             timeout=15)
        # Cuando se refresco por ultima vez la referencia remota.
        edad = None
        cabeza = ruta / ".git" / "FETCH_HEAD"
        try:
            edad = int(time.time() - cabeza.stat().st_mtime)
        except OSError:
            pass
        cuenta = int(n.strip()) if ok_n and n.strip().isdigit() else None
        pendientes += cuenta or 0
        fuera[ruta.name] = {
            "rama": rama, "upstream": arriba, "sin_push": cuenta,
            "sucios": len([l for l in sucio.splitlines() if l.strip()]) if ok_s else None,
            "fetch_edad_s": edad}
    return _declarar("OK", pendientes_total=pendientes, arboles=fuera)


def _gate(cwd, cmd, patron):
    ok, salida = _corre(cmd, timeout=300, cwd=str(cwd))
    cola = "\n".join(salida.strip().splitlines()[-3:])
    m = re.search(patron, salida)
    if not m:
        return _declarar("NO_DATA", causa="no se pudo leer el resumen del gate",
                         remedio=" ".join(cmd), cola=cola)
    datos = {k: int(v) for k, v in m.groupdict(default="0").items() if v}
    if not ok:
        return _declarar("RED", causa="el gate termino en rojo", cola=cola, **datos)
    return _declarar("OK", cola=cola, **datos)


def sonda_gate_mvp():
    return _gate(REPO_MVP, ["python3", "-m", "pytest", "--tb=no", "-q"],
                 r"(?P<pasa>\d+) passed(?:, (?P<salta>\d+) skipped)?"
                 r"(?:, (?P<subtests>\d+) subtests passed)?")


def sonda_gate_web():
    return _gate(REPO_WEB, ["python3", "test_web.py"],
                 r"Ran (?P<pasa>\d+) tests?")


# --------------------------------------------------------------------------
# Orquestacion
# --------------------------------------------------------------------------

def _arrastrar_gates(previo, ahora_epoch):
    """Trae los gates de la ultima corrida completa, CON su edad.

    Un dato viejo declarado como viejo sigue siendo un dato. Un dato viejo
    disfrazado de fresco es una mentira, y el pais entero de este proyecto se
    apoya en no decir ninguna.
    """
    fuera = {}
    for clave in ("mvp_gate", "web_gate"):
        bloque = ((previo or {}).get("componentes") or {}).get(clave)
        if not bloque:
            fuera[clave] = _declarar(
                "NO_DATA", causa="nunca se ha corrido el gate en modo --completo",
                remedio="python3 recolector.py --completo")
            continue
        copia = dict(bloque)
        medido = (previo or {}).get("epoch")
        copia["edad_s"] = int(ahora_epoch - medido) if medido else None
        copia["arrastrado"] = True
        fuera[clave] = copia
    return fuera


def recolectar(completo=False):
    ahora = datetime.now(timezone.utc).astimezone()
    epoch = time.time()
    previo = None
    if SALIDA.exists():
        try:
            previo = json.loads(SALIDA.read_text(encoding="utf-8"))
        except ValueError:
            previo = None

    componentes = {
        "ollama": sonda_ollama(),
        "api_guia": sonda_api_guia(),
        "lora_v7": sonda_lora(),
        "enjambre": sonda_enjambre(),
        "memoria": sonda_memoria(),
        "puertos": sonda_puertos(),
        "doogee": sonda_doogee(),
        "tailscale": sonda_tailscale(),
        "disco": sonda_disco(),
        "repos": sonda_repos(),
    }
    if completo:
        componentes["mvp_gate"] = sonda_gate_mvp()
        componentes["web_gate"] = sonda_gate_web()
    else:
        componentes.update(_arrastrar_gates(previo, epoch))

    return {
        "generado": ahora.isoformat(timespec="seconds"),
        "epoch": epoch,
        "nodo": "soberano",
        "modo": "completo" if completo else "rapido",
        "escala": {"OK": "responde y es lo esperado",
                   "RED": "responde y no es lo esperado · causa obligatoria",
                   "NO_DATA": "no se pudo medir · causa y remedio obligatorios"},
        "componentes": componentes,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--completo", action="store_true",
                    help="incluye los dos gates (~10 s de CPU). Modo de cierre de sesion")
    ap.add_argument("--rapido", action="store_true",
                    help="sin gates, ~2 s. Es el modo por defecto")
    ap.add_argument("--salida", default=str(SALIDA))
    ap.add_argument("--historial", action="store_true",
                    help="ademas deja una copia fechada en historial/")
    ap.add_argument("--stdout", action="store_true",
                    help="imprime el JSON y no escribe nada")
    a = ap.parse_args(argv)

    datos = recolectar(completo=a.completo)
    texto = json.dumps(datos, indent=2, ensure_ascii=False) + "\n"

    if a.stdout:
        sys.stdout.write(texto)
        return 0

    destino = Path(a.salida)
    destino.parent.mkdir(parents=True, exist_ok=True)
    # Escritura atomica: un corte a mitad no puede dejar un estado.json a
    # medias que la proxima sesion lea como si fuera verdad.
    parcial = destino.with_suffix(".json.partial")
    parcial.write_text(texto, encoding="utf-8")
    os.replace(parcial, destino)

    if a.historial:
        HISTORIAL.mkdir(parents=True, exist_ok=True)
        sello = datetime.now().strftime("%Y%m%d-%H%M%S")
        (HISTORIAL / f"estado-{sello}.json").write_text(texto, encoding="utf-8")

    rojos = [k for k, v in datos["componentes"].items()
             if isinstance(v, dict) and v.get("estado") == "RED"]
    print(f"estado.json escrito · modo={datos['modo']} · "
          f"rojos={len(rojos)}{': ' + ', '.join(rojos) if rojos else ''}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
