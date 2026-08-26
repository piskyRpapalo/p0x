"""El jardin: el hueco mejor declarado del panel.

El indice del ecosistema lo situa dentro del orquestador. En disco no hay
ninguna carpeta de jardin, ni aqui ni ahi, comprobado cada vez que se pide esta
lectura y no una sola vez cuando se escribio este fichero.

Ese matiz es el modulo entero. Un marcador de posicion que dice «en espera» sin
mirar seguiria diciendolo el dia que el jardin exista, y nadie lo notaria hasta
que hiciera falta un dato de un sensor que llevaba semanas funcionando.
"""

from pathlib import Path

import sensores
from sensores import registro

RAIZ = Path(__file__).resolve().parents[2]
CANDIDATAS = ("jardin", "hexelion/jardin", "le-jardin", "hexelion/le-jardin")


def leer():
    encontradas = [c for c in CANDIDATAS if (RAIZ / c).is_dir()]
    if not encontradas:
        return sensores.hueco(
            "modulo de permacultura: sin carpeta en disco · "
            + " · ".join(f"no hay {c}/" for c in CANDIDATAS[:2]))
    return sensores.dato(
        rutas=encontradas,
        sensores_declarados=sensores.NO_DATA,
        ultima_lectura=sensores.NO_DATA,
        causa="la carpeta existe · todavia no hay lector de sensores",
    )


registro.registrar("jardin", leer)
