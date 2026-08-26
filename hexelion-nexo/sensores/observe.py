"""La camara. Un `<img>` y nada mas -- el navegador ya sabe leer MJPEG.

Un flujo MJPEG es una sucesion de imagenes por una conexion que no se cierra, y
la etiqueta `<img>` lleva decadas sabiendo consumirlo. Ponerle JavaScript encima
no anade nada: anade bytes, una dependencia y un sitio donde fallar.

La direccion NO vive en este fichero. Se declara en `$NEXO_CAMARA`, y sin
declararla no se emite ninguna etiqueta que apunte fuera: el panel por defecto
no carga un solo recurso de ninguna red. Esa es la razon de que se compruebe
ANTES de pintar -- un `<img>` roto ensena el icono de imagen partida del
navegador, que es la version grafica del cero decorativo: parece un fallo del
panel y es un fallo de la camara, y no dice cual.
"""

import os
import urllib.request

import sensores
from sensores import registro

VARIABLE = "NEXO_CAMARA"
ESPERA = 3


def direccion():
    return (os.environ.get(VARIABLE) or "").strip()


def _responde(url):
    """Un byte basta. No se descarga el flujo: se comprueba que empieza."""
    peticion = urllib.request.Request(url, method="GET")
    r = urllib.request.urlopen(peticion, timeout=ESPERA)
    try:
        tipo = r.headers.get("Content-Type", "")
        r.read(1)
        return tipo
    finally:
        r.close()


def leer():
    url = direccion()
    if not url:
        return sensores.hueco(
            f"sin camara declarada · ponla en ${VARIABLE} si hay una",
            "el panel por defecto no apunta a ninguna")
    try:
        tipo = _responde(url)
    except Exception as e:                                       # noqa: BLE001
        return sensores.hueco(
            "camara sin senal · la direccion esta declarada y no contesta",
            type(e).__name__)
    return sensores.dato(url=url, tipo=tipo or sensores.NO_DATA,
                         mjpeg="multipart" in tipo.lower())


registro.registrar("observe", leer)
