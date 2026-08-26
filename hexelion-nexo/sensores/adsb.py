"""Las aeronaves que oye la antena. Solo las que ademas dicen donde estan.

Un receptor ADS-B recibe de mas aviones de los que puede situar: muchos emiten
identificacion y altitud sin posicion, o la posicion todavia no ha llegado. El
gateway lo dice en dos cifras --`count_total` y `count_visible`-- y **las dos
viajan**. Ensenar solo las situadas seria contestar «hay dos aviones» cuando se
esta oyendo a ocho, que es una forma de mentir por omision: el numero es cierto
y la frase es falsa.

La ventana geografica es fija y no se ajusta a lo que hay. Ese es el punto
delicado del modulo entero, y esta explicado en `ventana()`.
"""

import json
import os
import urllib.request

import sensores
from sensores import nodos, registro

RUTA = "/api/aircraft"
ESPERA = 5

# La ventana: `lat_sur,lat_norte,lon_oeste,lon_este`. Sin declararla se deduce
# de lo que hay, con suelo -- ver `ventana()`.
VARIABLE = "NEXO_ADSB_VENTANA"

# Grados minimos de lado. Es lo que impide el fallo del encadre automatico:
# con dos aviones a tres kilometros, una ventana ajustada a ellos los pinta en
# esquinas opuestas y el mapa dice que estan lejisimos. Un grado son ~111 km.
SUELO_GRADOS = 1.2
MARGEN = 0.15          # aire alrededor, para que nadie quede pegado al borde

ANCHO, ALTO = 400, 300

# Los tres escalones de altitud, en pies.
ESCALONES = ((10000, "baja"), (25000, "media"), (float("inf"), "alta"))


def _url():
    base = nodos.gateway()
    return (base + RUTA) if base else ""


def ventana(aviones):
    """El rectangulo que se dibuja. Fijo si se declara; con suelo si no.

    **Por que no se encuadra a los datos.** La formula obvia --normalizar entre
    el minimo y el maximo de lo que hay-- tiene dos averias que no se ven hasta
    que muerden:

    1. Con un solo avion, minimo y maximo coinciden y se divide entre cero.
    2. Con dos, quedan clavados en esquinas opuestas **estén donde estén**. Dos
       aviones a tres kilometros se pintan igual que dos a trescientos, y la
       distancia --que es lo unico que un mapa tiene que decir bien-- deja de
       significar nada. Peor: la escala cambia en cada refresco, asi que un
       avion quieto parece moverse porque entro otro por el otro lado.

    Con suelo, un cielo casi vacio se dibuja a escala honesta y solo se abre
    cuando hay algo de verdad lejos.
    """
    declarada = (os.environ.get(VARIABLE) or "").strip()
    if declarada:
        try:
            s, n, o, e = (float(x) for x in declarada.split(","))
            if n > s and e > o:
                return s, n, o, e, "declarada"
        except ValueError:
            pass                      # una ventana ilegible se ignora, no revienta
    if not aviones:
        return None
    lats = [a["lat"] for a in aviones]
    lons = [a["lon"] for a in aviones]
    clat, clon = (min(lats) + max(lats)) / 2, (min(lons) + max(lons)) / 2
    alto = max(max(lats) - min(lats), SUELO_GRADOS) * (1 + MARGEN)
    # Un grado de longitud mide menos que uno de latitud, y el factor es el
    # coseno de la latitud. Sin esto el cielo sale aplastado y las distancias
    # este-oeste se leen mas grandes de lo que son.
    import math
    encoge = max(math.cos(math.radians(clat)), 0.1)
    ancho = max(max(lons) - min(lons), SUELO_GRADOS / encoge) * (1 + MARGEN)
    return (clat - alto / 2, clat + alto / 2,
            clon - ancho / 2, clon + ancho / 2, "deducida")


def escalon(pies):
    if not isinstance(pies, (int, float)):
        return sensores.NO_DATA
    for techo, nombre in ESCALONES:
        if pies < techo:
            return nombre
    return "alta"


def leer():
    url = _url()
    if not url:
        return sensores.hueco(
            "sin gateway declarado · la antena se pregunta a traves de el",
            "NEXO_GATEWAY")
    try:
        with urllib.request.urlopen(url, timeout=ESPERA) as r:
            crudo = json.loads(r.read().decode("utf-8"))
    except Exception as e:                                       # noqa: BLE001
        return sensores.hueco(
            "el gateway de la antena no contesta · de las aeronaves no hay dato",
            type(e).__name__)

    todas = crudo.get("aircraft") or []
    situados = []
    for a in todas:
        lat, lon = a.get("lat"), a.get("lon")
        if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
            continue
        pies = a.get("alt_baro")
        situados.append({
            "hex": (a.get("hex") or sensores.NO_DATA).strip(),
            # `flight` viene relleno de espacios por el formato de la trama.
            "vuelo": (a.get("flight") or "").strip() or sensores.NO_DATA,
            "lat": lat, "lon": lon,
            "pies": pies if isinstance(pies, (int, float)) else sensores.NO_DATA,
            "nudos": a.get("gs") if isinstance(a.get("gs"), (int, float))
                     else sensores.NO_DATA,
            "escalon": escalon(pies),
        })

    oidas = crudo.get("count_total")
    if not isinstance(oidas, int):
        oidas = len(todas)

    if not situados:
        return sensores.hueco(
            f"ninguna aeronave con posicion · se oyen {oidas}, y ninguna dice "
            "donde esta" if oidas else "silencio en la banda · no se oye ninguna",
            f"count_total={oidas}")

    v = ventana(situados)
    return sensores.dato(
        aviones=situados,
        situadas=len(situados),
        oidas=oidas,
        # La cifra que el mapa NO puede ensenar, y que por eso hay que decir.
        mudas=max(oidas - len(situados), 0),
        ventana={"sur": v[0], "norte": v[1], "oeste": v[2], "este": v[3],
                 "origen": v[4]},
    )


registro.registrar("adsb", leer)
