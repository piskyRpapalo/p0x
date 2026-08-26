"""El pipeline de video: sus registros, y cuanto hace que nadie lo toca.

Se listan los `.log` con su tamaño y su fecha. Lo que NO se hace es leerlos: un
registro de 1,4 MiB metido en una respuesta JSON que se pide cada 30 s es una
forma de tirar el panel, y ademas ninguna de esas lineas cabe en una tarjeta.

La cifra que importa aqui no es el tamaño: es **cuantos dias hace del ultimo**.
Un pipeline parado y uno vivo tienen ficheros identicos; solo los separa la fecha.
"""

from datetime import datetime
from pathlib import Path

import sensores
from sensores import registro

ESTUDIO = Path(__file__).resolve().parents[2] / "CineK_Studio"
CUANTOS = 8


def leer():
    if not ESTUDIO.is_dir():
        return sensores.hueco("el estudio no existe en disco")
    registros = sorted(ESTUDIO.rglob("*.log"),
                       key=lambda p: p.stat().st_mtime, reverse=True)[:CUANTOS]
    if not registros:
        return sensores.hueco("el estudio existe pero no tiene ningun registro")

    ahora = datetime.now()
    filas = []
    for f in registros:
        st = f.stat()
        fecha = datetime.fromtimestamp(st.st_mtime)
        filas.append({
            "nombre": str(f.relative_to(ESTUDIO)),
            "bytes": st.st_size,
            "fecha": fecha.isoformat(timespec="minutes"),
            "dias": (ahora - fecha).days,
        })
    quietud = min(f["dias"] for f in filas)
    return sensores.dato(
        registros=filas,
        quietud_dias=quietud,
        # Se dice en voz alta en vez de dejarlo a que alguien reste dos fechas.
        nota=f"nada tocado en {quietud} dias" if quietud >= 1 else "actividad hoy",
    )


registro.registrar("cinek", leer)
