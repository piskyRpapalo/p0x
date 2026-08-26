"""En que nivel corre la instalacion del nucleo publico.

No duplica la logica: importa el guardian del propio nucleo y le pregunta. Las
reglas de que cuenta como nivel valido --entero 0..3, y 0 ante cualquier duda--
viven en UN sitio, y ese sitio es `soberania.py` del nucleo. Copiarlas aqui
crearia dos verdades sobre el mismo hecho, que es exactamente lo que el canon
de los niveles existe para impedir.

Se lee y no se toca. Este modulo no escribe una linea en el arbol del nucleo:
el nivel 3 se engancha, no reforma lo que hay debajo.
"""

import sys
from pathlib import Path

import sensores
from sensores import registro

# El nucleo es hermano de esta carpeta, no un sitio fijo del disco.
NUCLEO = Path(__file__).resolve().parents[2] / "aurelius"


def _guardian():
    if str(NUCLEO) not in sys.path:
        sys.path.insert(0, str(NUCLEO))
    import soberania as _sob
    return _sob


def leer():
    try:
        sob = _guardian()
    except Exception as e:                                       # noqa: BLE001
        return sensores.hueco(
            "el nucleo publico no esta junto a este panel · sin el no hay "
            "nivel que leer, y no se supone uno", type(e).__name__)

    # argv vacio a proposito: la bandera de corte gobierna el proceso que la
    # recibio, y el proceso que la recibio no es este panel.
    nivel = sob.obtener_nivel(argv=[])
    nombres = {0: "SANTUARIO", 1: "ARNES", 2: "EXPANSION", 3: "ECOSISTEMA"}
    capacidades = [
        {"nombre": c, "pide": m,
         "concedida": bool(sob.verificar_permiso(c, argv=[]))}
        for c, m in sorted(sob.CAPACIDADES.items(), key=lambda kv: (kv[1], kv[0]))
    ]
    return sensores.dato(
        nivel=nivel,
        nombre=nombres.get(nivel, sensores.NO_DATA),
        maximo=sob.NIVEL_MAXIMO,
        cortado=bool(sob.santuario_activo(argv=[])),
        capacidades=capacidades,
        niveles=[{"n": n, "nombre": nombres[n], "activo": n <= nivel}
                 for n in range(0, sob.NIVEL_MAXIMO + 1)],
    )


registro.registrar("soberania", leer)
