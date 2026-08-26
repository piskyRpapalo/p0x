"""Los cuatro nodos del rack: quien esta en pie, quien esta a medias y quien no.

**Este es el unico sensor que sale de la maquina**, y por eso es el unico con un
interruptor propio. Arrancar el Nexo con `--sin-red` lo deja mudo: devuelve el
hueco declarado en vez de tocar el tailnet. El resto del panel sigue entero,
porque el resto del panel nunca salio.

Dos fuentes, y se dice cual habla:

1. **`tailscale status --json`**, que se resuelve en ESTA maquina y no pregunta
   a nadie. De ahi sale quien responde.
2. **El gateway de La Fragua**, que ya publica `/api/health/nodes` y
   `/api/antenna/health`. Se usa en vez de abrir sesiones SSH desde un panel:
   una ventana que entra por SSH en cuatro maquinas cada treinta segundos no es
   una ventana, es un agente con llaves.

Y una correccion medida: el registro del gateway trae este nodo apuntando a otra
maquina, apagada, y lo da por caido. Se corrige aqui con lo que se sabe de
primera mano --se esta ejecutando en el, luego esta en pie-- y se DECLARA la
correccion en vez de aplicarla en silencio.
"""

import json
import os
import shutil
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

import sensores
from sensores import registro

# La direccion del gateway NO vive en este fichero, y no es una manía: la
# guardia de higiene del repo bloquea rutas de nodo en lo que entra en la
# historia, y su motivo es el de siempre -- lo que entra no se saca sin
# reescribirla. Asi que la infraestructura vive en la maquina y el codigo solo
# sabe donde preguntar:
#
#   1. la variable de entorno, que es lo que manda,
#   2. `estado/gateway.conf`, una linea, sin versionar,
#   3. y si no hay ninguna de las dos: NO_DATA con la orden para ponerla.
#
# Un panel que no encuentra su gateway no adivina uno.
VARIABLE = "NEXO_GATEWAY"
CONF = Path(__file__).resolve().parents[1] / "estado" / "gateway.conf"
ESPERA = 4


def gateway():
    """Donde preguntar. Cadena vacia si nadie lo ha dicho -- y eso no es un fallo."""
    desde_entorno = (os.environ.get(VARIABLE) or "").strip()
    if desde_entorno:
        return desde_entorno
    try:
        return CONF.read_text(encoding="utf-8").strip().splitlines()[0].strip()
    except (OSError, IndexError):
        return ""

RACK = (
    ("soberano",  "Beelink · Ryzen 7 255 · 64 GB", "nucleo publico · inferencia local"),
    ("la-fragua", "Orange Pi 5 Plus · RK3588 · 16 GB", "gateway · faro · voz · bateria"),
    ("el-vigia",  "Raspberry Pi · SDR · ESP32", "adquisicion RF · ADS-B y AIS"),
    ("la-torre",  "Jetson Orin Nano Super · CUDA 12.6", "inferencia acelerada"),
)

# El nombre que usa el gateway para cada nodo, que no es el del tailnet.
EN_EL_GATEWAY = {"la-fragua": "fragua", "el-vigia": "vigilante", "la-torre": "torre"}

_SIN_RED = False


def sin_red(valor=None):
    """Lee o fija el corte de red de este sensor. Sin argumento, solo lee."""
    global _SIN_RED
    if valor is not None:
        _SIN_RED = bool(valor)
    return _SIN_RED


def _json_remoto(base, ruta):
    peticion = urllib.request.Request(base + ruta, method="GET")
    with urllib.request.urlopen(peticion, timeout=ESPERA) as r:
        return json.loads(r.read().decode("utf-8"))


def _nombre(entrada):
    """El nombre del tailnet, que NO siempre es el de la maquina.

    Medido: La Fragua se llama `la-fragua` en el tailnet y `ubuntu` en su propio
    sistema. Indexar por `HostName` la dejaba fuera del mapa en silencio -- y en
    silencio es como se pierde un nodo de un panel: no sale un error, sale un
    NO_DATA que parece que el nodo esta caido. El nombre que manda es la primera
    etiqueta de `DNSName`, que es el que resuelve y el que la gente escribe.
    """
    dns = (entrada.get("DNSName") or "").split(".")[0]
    return dns or entrada.get("HostName") or ""


def _tailscale():
    """Quien responde, preguntado a esta maquina y no al tailnet."""
    ruta = shutil.which("tailscale")
    if ruta is None:
        return {}
    crudo = subprocess.run([ruta, "status", "--json"], capture_output=True,
                           text=True, timeout=ESPERA).stdout
    datos = json.loads(crudo)
    vivos = {}
    propio = datos.get("Self") or {}
    if _nombre(propio):
        vivos[_nombre(propio)] = True
    for par in (datos.get("Peer") or {}).values():
        nombre = _nombre(par)
        if nombre:
            vivos[nombre] = bool(par.get("Online"))
    return vivos


def leer():
    if _SIN_RED:
        return sensores.hueco(
            "el panel arranco con la red cortada · los nodos remotos no se "
            "preguntan, y no preguntarlos es la respuesta correcta aqui")

    try:
        vivos = _tailscale()
    except Exception as e:                                       # noqa: BLE001
        vivos = {}
        aviso_ts = f"el tailnet no se pudo consultar · {type(e).__name__}"
    else:
        aviso_ts = "" if vivos else "el tailnet no declara ningun nodo"

    salud, antena, aviso_gw = {}, None, ""
    base = gateway()
    if not base:
        aviso_gw = (f"sin gateway declarado · ponlo en ${VARIABLE} o en "
                    f"estado/gateway.conf · lo de los nodos sale solo del tailnet")
    else:
        try:
            for n in _json_remoto(base, "/api/health/nodes").get("nodes", []):
                salud[n.get("node_id")] = n
            antena = _json_remoto(base, "/api/antenna/health")
        except Exception as e:                                   # noqa: BLE001
            aviso_gw = (f"el gateway no contesta · {type(e).__name__} · "
                        "lo de los nodos remotos sale solo del tailnet")

    correcciones = []
    sin_sonda = []
    filas = []
    for nombre, metal, papel in RACK:
        g = salud.get(EN_EL_GATEWAY.get(nombre, nombre)) or {}
        sondas = dict(g.get("probes") or {})
        arriba = vivos.get(nombre)

        if nombre == "soberano":
            # De primera mano: este codigo se esta ejecutando aqui.
            arriba = True
            if (g.get("health") or "") == "offline":
                correcciones.append(
                    "el registro del gateway da este nodo por caido y apunta a "
                    "otra maquina · se corrige con lo que se sabe de primera mano")

        estado, nota, alerta = "NO_DATA", "", ""
        if arriba is False:
            estado, nota = "OFFLINE", "no responde en el tailnet"
        elif arriba is True:
            estado, nota = "ONLINE", papel

        if nombre == "el-vigia" and antena:
            ais = (antena.get("ais") or {})
            adsb = (antena.get("adsb") or {})
            if arriba and not ais.get("live"):
                estado = "CRITICO"
                alerta = "ais-catcher caido · puerto 10110 cerrado"
                # El matiz que separa un servicio caido de una radio ausente.
                nota = (f"ADS-B vivo · {adsb.get('aircraft', sensores.NO_DATA)} "
                        f"aeronaves · AIS 0 buques")
        if nombre == "la-torre" and arriba:
            # CICATRIZ. Aqui habia `estado = "EN ESPERA"` cuando faltaba la
            # sonda, y eso era exactamente el fallo que este arbol existe para
            # impedir: **una ausencia de dato convertida en una afirmacion de
            # estado**. Que el gateway no conteste no dice nada sobre si el
            # nodo esta dormido -- dice que no lo sabemos. El nodo responde en
            # el tailnet, luego esta en pie; lo que no hay es la sonda, y eso
            # se declara con su nombre.
            if sondas.get("ollama_11434"):
                nota = "Ollama sirviendo"
            else:
                nota = "en pie · inferencia " + sensores.NO_DATA
                sin_sonda.append(nombre)

        filas.append({
            "nodo": nombre, "metal": metal, "estado": estado,
            "nota": nota or sensores.NO_DATA, "alerta": alerta,
            "sondas": sorted(k for k, v in sondas.items() if v is True),
        })

    if sin_sonda:
        correcciones.append(
            "sin sonda profunda de " + ", ".join(sin_sonda)
            + " · responden en el tailnet, pero de sus servicios no hay dato")
    avisos = [a for a in (aviso_ts, aviso_gw) if a] + correcciones
    return sensores.dato(
        nodos=filas,
        en_pie=sum(1 for f in filas if f["estado"] == "ONLINE"),
        criticos=sum(1 for f in filas if f["estado"] == "CRITICO"),
        fuente="tailscale local" + ("" if aviso_gw else " + gateway de la forja"),
        gateway_declarado=bool(base),
        avisos=avisos,
        causa=" · ".join(avisos),
    )


registro.registrar("nodos", leer)
