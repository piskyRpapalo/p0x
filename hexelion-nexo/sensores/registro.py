"""El reparto de sensores. La unica lista, como en `bin/pruebas`.

Existe por el mismo motivo que aquella: un panel que descubre sus sensores
automaticamente deja de avisar el dia que uno desaparece -- simplemente pinta
una tarjeta menos, y nadie se entera hasta que hace falta el dato.
"""

import sensores

SENSORES = {}


def registrar(nombre, leer):
    SENSORES[nombre] = leer
    return leer


def uno(nombre):
    leer = SENSORES.get(nombre)
    if leer is None:
        return sensores.hueco(f"no hay ningun sensor llamado «{nombre}»")
    return sensores.a_prueba_de_balas(leer)()


def todo():
    """Todas las lecturas de una vez. Un sensor caido no tumba a los demas."""
    return {"medido": sensores.ahora(),
            "lecturas": {n: uno(n) for n in sorted(SENSORES)}}
