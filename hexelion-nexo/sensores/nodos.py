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

# El rack tampoco vive en el codigo, y por dos motivos distintos. El primero es
# el mismo del gateway: son nombres de maquina. El segundo es que un rack
# cableado aqui hace que este repo solo sirva para UN rack -- el nuestro-- y
# quien lo clone vera cuatro tarjetas de nodos que no tiene.
#
# Formato de `rack.conf`, una linea por nodo, separadas por `|`:
#   nombre | metal | papel | nombre_en_el_gateway
#
# Sin fichero no se inventa un rack: se declara el hueco. Un panel de nodos que
# se rellena con nodos de ejemplo es peor que uno vacio, porque el vacio se ve.
RACK_CONF = Path(__file__).resolve().parents[1] / "estado" / "rack.conf"
NODO_PROPIO = "NEXO_NODO_PROPIO"     # cual de ellos es esta maquina


def rack():
    """Los nodos declarados. Lista vacia si no hay ninguno -- y eso se dice."""
    filas = []
    try:
        crudo = RACK_CONF.read_text(encoding="utf-8")
    except OSError:
        return filas
    for linea in crudo.splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#"):
            continue
        partes = [c.strip() for c in linea.split("|")]
        while len(partes) < 4:
            partes.append("")
        filas.append(tuple(partes[:4]))
    return filas


def propio():
    """Cual de los nodos es esta maquina. Sin declararlo, ninguno lo es.

    Importa: es el unico del que se sabe algo de primera mano, y por eso el
    unico cuyo estado puede corregir lo que diga un registro remoto.
    """
    return (os.environ.get(NODO_PROPIO) or "").strip()

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


def _host(url):
    """La primera etiqueta del host de una URL. Sin dominio y sin puerto.

    Se recorta a proposito: lo que hace falta enseñar es a que MAQUINA apunta
    una sonda, y el dominio de la red privada no pinta nada en una pantalla.
    """
    try:
        # Sin `://` no hay host. `file:/run/algo.json` es el caso real -- la
        # cadena de ADS-B se lee de un fichero LOCAL del gateway-- y sin esta
        # linea se reportaba una maquina llamada «file», que no existe.
        if "://" not in url:
            return ""
        autoridad = url.split("://", 1)[1].split("/")[0]
        return autoridad.split("@")[-1].split(":")[0].split(".")[0]
    except Exception:                                            # noqa: BLE001
        return ""


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
        aviso_ts = ("la red malla no contesta en esta maquina · de quien "
                    f"responde no hay dato ({type(e).__name__})")
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
            aviso_gw = ("el gateway no contesta · las sondas profundas de "
                        "nodo no llegan, y lo que se sabe sale solo de la red "
                        f"malla ({type(e).__name__})")

    declarados = rack()
    if not declarados:
        return sensores.hueco(
            f"sin rack declarado · una linea por nodo en {RACK_CONF.name} "
            "(nombre | metal | papel | nombre_en_el_gateway)")

    yo = propio()
    correcciones = []
    sin_sonda = []
    filas = []
    for nombre, metal, papel, en_gateway in declarados:
        g = salud.get(en_gateway or nombre) or {}
        sondas = dict(g.get("probes") or {})
        arriba = vivos.get(nombre)

        if nombre and nombre == yo:
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

        if antena and "AIS" in papel.upper():
            ais = (antena.get("ais") or {})
            adsb = (antena.get("adsb") or {})
            if arriba and not ais.get("live"):
                estado = "CRITICO"
                # CICATRIZ. Aqui ponia «ais-catcher caido» a secas, y eso
                # atribuia la averia AL NODO DE ESTA TARJETA. Falso: la sonda
                # de AIS del gateway apunta a un host propio, que puede no ser
                # este -- y medido el 2026-08-27, no lo era: seguia mirando al
                # nodo donde la cadena vivia ANTES de moverla. Una alerta que
                # senala la maquina equivocada manda a arreglar lo que no esta
                # roto, y deja lo roto donde estaba.
                #
                # Ahora la alerta dice a DONDE MIRA la sonda, que es lo unico
                # que este panel sabe de verdad, y avisa cuando ese sitio no es
                # el nodo de la tarjeta.
                mira = _host(ais.get("origin") or "")
                alerta = "la sonda de AIS no recibe · mira a " + (mira or sensores.NO_DATA)
                if mira and mira != nombre:
                    alerta += f" · que NO es {nombre}"
                    correcciones.append(
                        f"la sonda de AIS apunta a «{mira}» y la tarjeta es de "
                        f"«{nombre}» · uno de los dos esta desfasado, y no es "
                        "algo que este panel pueda decidir")
                nota = (f"ADS-B vivo · {adsb.get('aircraft', sensores.NO_DATA)} "
                        f"aeronaves · AIS 0 buques")
        if arriba and "INFERENCIA" in papel.upper() and nombre != yo:
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
