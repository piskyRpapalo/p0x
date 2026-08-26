"""Los sensores del Nexo. Uno por fuente, y ninguno adivina.

Contrato unico y sin excepciones: un sensor devuelve un dict con la clave
`estado`, que vale `"ok"` o `"NO_DATA"`. Cuando vale `"NO_DATA"` trae `causa`
con una frase que se puede enseñar. Nunca lanza, nunca devuelve None y nunca
rellena un hueco con un cero -- un cero decorativo es indistinguible de una
medida, y esa confusion es la averia que este contrato existe para impedir.

Todo sensor lleva ademas `medido`, la hora ISO en que se leyo. Una cifra sin su
hora es un rumor con decimales.
"""

from datetime import datetime

NO_DATA = "NO_DATA"


def ahora():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def hueco(causa, detalle=""):
    """Un hueco declarado, con su motivo. La unica forma legitima de no tener dato.

    `causa` es una frase para una persona: que falta y, si se puede, que hacer.
    `detalle` es para quien depura -- el nombre de la excepcion, la ruta que no
    estaba--. Van separados porque mezclarlos convierte la causa en jerga:
    «ModuleNotFoundError» tiene la FORMA de una explicacion y no explica nada a
    quien esta mirando el panel. Y porque una causa que acaba en «Error» no se
    distingue de una causa que no se escribio.
    """
    return {"estado": NO_DATA, "causa": causa, "detalle": detalle,
            "medido": ahora()}


def dato(**campos):
    campos.setdefault("estado", "ok")
    campos.setdefault("causa", "")
    campos["medido"] = ahora()
    return campos


def a_prueba_de_balas(fn):
    """Un sensor que revienta es un sensor que apaga el panel entero.

    Envuelve la lectura para que cualquier fallo salga como hueco declarado en
    vez de como una excepcion que se lleva por delante `/api/estado`.
    """
    def envuelto(*a, **k):
        try:
            salida = fn(*a, **k)
        except Exception as e:                                   # noqa: BLE001
            return hueco("este sensor no pudo completar su lectura",
                         type(e).__name__)
        if not isinstance(salida, dict) or "estado" not in salida:
            return hueco("el sensor devolvio algo que no es una lectura")
        return salida
    envuelto.__name__ = fn.__name__
    envuelto.__doc__ = fn.__doc__
    return envuelto
