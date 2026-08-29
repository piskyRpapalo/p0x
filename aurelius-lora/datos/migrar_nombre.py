#!/usr/bin/env python3
"""Deriva el dataset v7 del v6 cambiando solo el nombre del asistente.

`data/` no se versiona (es el alma, P4): se reconstruye desde el canon. Por eso
la migracion de nombre tiene que ser un script y no un fichero, o el v7 seria
irreproducible y nadie podria comprobar que solo cambio el nombre.

Toca UNICAMENTE la etiqueta de turno `[Aurelius]` -> `[Preceptor]`. Las
menciones a "Aurelius" dentro del turno del USUARIO se dejan intactas a
proposito: el caso EC-1.3 es un intento de manipulacion por halago, y quien
lo escriba seguira usando el nombre que ve en pantalla. Cambiarlas exige
firma del Soberano, no una decision del script.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
VIEJO, NUEVO = "[Aurelius]", "[Preceptor]"


def main(argv=None):
    ap = argparse.ArgumentParser(description="v6 -> v7 · solo el nombre")
    ap.add_argument("--origen", type=Path, default=RAIZ / "data" / "sft_cot.jsonl")
    ap.add_argument("--destino", type=Path, default=RAIZ / "data" / "sft_cot_v7.jsonl")
    a = ap.parse_args(argv)

    if not a.origen.is_file():
        print(f"[migrar] no existe {a.origen}")
        return 1

    registros, etiquetas = [], 0
    for linea in a.origen.open(encoding="utf-8"):
        linea = linea.strip()
        if not linea:
            continue
        r = json.loads(linea)
        texto = r.get("texto", "")
        etiquetas += texto.count(VIEJO)
        r["texto"] = texto.replace(VIEJO, NUEVO)
        registros.append(r)

    a.destino.write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in registros),
        encoding="utf-8",
    )
    print(f"[migrar] {len(registros)} registros · {etiquetas} etiquetas · {a.destino}")

    # Un generador que no se comprueba a si mismo es una promesa, no un dato.
    escritos = [json.loads(l) for l in a.destino.open(encoding="utf-8") if l.strip()]
    originales = [json.loads(l) for l in a.origen.open(encoding="utf-8") if l.strip()]
    for viejo, nuevo in zip(originales, escritos):
        if viejo["texto"].replace(VIEJO, NUEVO) != nuevo["texto"]:
            print("[migrar] ROJO: un registro cambio en algo que no es el nombre")
            return 1
        if {k: v for k, v in viejo.items() if k != "texto"} != \
           {k: v for k, v in nuevo.items() if k != "texto"}:
            print("[migrar] ROJO: cambio un campo que no es el texto")
            return 1
    print("[migrar] VERDE · lo unico que cambia es el nombre")
    return 0


if __name__ == "__main__":
    sys.exit(main())
