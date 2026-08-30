#!/usr/bin/env python3
"""Exporta las fases de `continuidad.db` a `Alejandria/fases.json`.

POR QUE UN EXPORTADOR Y NO UN FICHERO A MANO
--------------------------------------------
`plan_v5.md` dice que el margen del Ojo lee `Alejandria/fases.json`. La
tentacion es escribir ese fichero a mano una vez y olvidarlo. Seria la
segunda verdad sobre las fases del proyecto: la de `continuidad.db` --que es
la que absorbe cada cierre de sesion-- y la del JSON, que envejeceria en
silencio mientras el panel la sigue pintando en verde.

Asi que el JSON es SALIDA. La tabla `fases` de la continuidad es la fuente, y
este script solo la traduce. Si el JSON no existe, el Ojo pinta NO_DATA con su
remedio, que es honesto; lo que no puede pasar es que exista y mienta.

    python3 ~/p0x/Alejandria/fases.py
"""
from __future__ import annotations

import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
DB = RAIZ.parent / "preceptor-internal" / "continuidad" / "continuidad.db"
SALIDA = RAIZ / "fases.json"


def exportar(db: Path = DB, salida: Path = SALIDA) -> int:
    if not db.exists():
        print(f"NO_DATA · no existe {db}", file=sys.stderr)
        print("remedio: python3 preceptor-internal/continuidad/semilla.py",
              file=sys.stderr)
        return 1
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    try:
        filas = [dict(r) for r in con.execute(
            "SELECT nombre, estado, entrega, nota, actualizada_en FROM fases")]
    except sqlite3.Error as e:
        print(f"NO_DATA · la tabla `fases` no se pudo leer: {e}", file=sys.stderr)
        return 1
    finally:
        con.close()

    salida.write_text(json.dumps({
        "estado": "OK",
        # La fuente viaja DENTRO del dato. Un JSON suelto en un directorio no
        # dice de donde salio, y a los tres dias nadie se acuerda.
        "fuente": "continuidad.db · tabla fases",
        "generado": datetime.now(timezone.utc).astimezone().isoformat(
            timespec="seconds"),
        "fases": filas,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(filas)} fases -> {salida}")
    return 0


if __name__ == "__main__":
    raise SystemExit(exportar())
