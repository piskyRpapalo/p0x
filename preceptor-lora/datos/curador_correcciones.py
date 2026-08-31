#!/usr/bin/env python3
"""El eslabon [4] del flywheel: Bronze -> Silver. **Solo stdlib.**

QUE HACE
--------
Lee los pares corregidos que la persona CONSINTIO, los agrupa por
(modelo_base x skill) y los deja listos para la Forja. Abre la memoria en
**solo lectura**: este modulo no edita ni borra nada de lo que alguien
escribio.

POR QUE EXISTE ESTE FICHERO Y NO SE REUSO OTRO
----------------------------------------------
Habia en el rack un `curador.py` (L3, en los bucles) y llegue a escribir en un
documento de contrato que era este eslabon. **No lo es.** Aquel consulta
`engrams` y `links`: es higiene de la memoria --duplicados y enlaces rotos-- y
no toca ni una correccion. Comparten nombre porque LORATELIER_P0X.md llama
«Curador» al que cura el dataset, y ese parecido basto para confundirme. Queda
escrito aqui para que no vuelva a pasar.

LAS DOS COSAS QUE ESTE MODULO SE NIEGA A HACER
----------------------------------------------
1. **No entrena.** Deja un dataset; encenderlo es otra puerta.
2. **No sube `consent` de nadie.** `consent` nace en 0 en `captura.py` y solo
   el carbono lo sube. Un par capturado no es material de entrenamiento: es un
   recuerdo de la persona. Colarlo seria entrenar con algo que nadie autorizo,
   y es el fallo mas caro que hay porque una vez esta en los pesos no se
   deshace.

CERO NO ES LO MISMO QUE LIMPIO
------------------------------
Sobre una memoria sin correcciones, «0 pares» no significa que el dataset este
limpio: significa que no hay dataset. El estado sale NO_DATA con su causa, y
nunca un cero que parezca una medida. Es el mismo modo de fallo que S0 vigila
en los bucles: el filtro que da verde porque no miro.
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timezone


def _abrir_solo_lectura(ruta):
    """En modo `ro` de verdad, no por disciplina: por el motor."""
    return sqlite3.connect(f"file:{ruta}?mode=ro", uri=True)


def curar(ruta_db, skill="general"):
    """Bronze -> Silver. Devuelve el paquete entero, medido o declarado."""
    ahora = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    base = {"esquema": 1, "generado": ahora, "skill": skill,
            "fuente": os.path.basename(str(ruta_db)),
            "pares": [], "grupos": {}, "mirados": 0,
            "descartados": {"sin_consentimiento": 0, "sin_correccion": 0}}

    if not os.path.isfile(ruta_db):
        base["estado"] = "NO_DATA"
        base["causa"] = f"no hay memoria en {ruta_db}: nada que curar"
        return base
    try:
        c = _abrir_solo_lectura(ruta_db)
        filas = c.execute(
            "select prompt, respuesta, correccion, modelo, idioma, consent, motivo"
            " from turnos").fetchall()
        c.close()
    except sqlite3.Error as e:
        base["estado"] = "NO_DATA"
        base["causa"] = f"la memoria existe pero no se pudo leer: {e}"
        return base

    base["mirados"] = len(filas)
    for prompt, resp, corr, modelo, idioma, consent, motivo in filas:
        # El orden de los dos filtros importa para el recuento: un turno sin
        # consentimiento se descarta por eso aunque ademas le falte la
        # correccion. Contarlo dos veces inflaria los descartes.
        if not consent:
            base["descartados"]["sin_consentimiento"] += 1
            continue
        if not corr or not str(corr).strip():
            base["descartados"]["sin_correccion"] += 1
            continue
        base["pares"].append({
            "prompt": prompt,
            "rechazado": resp,      # lo que el modelo dijo
            "elegido": corr,        # lo que la persona esperaba
            "modelo_base": modelo,
            "idioma": idioma,
            "motivo": motivo,
            "skill": skill,
        })
        base["grupos"][modelo] = base["grupos"].get(modelo, 0) + 1

    if not base["pares"]:
        base["estado"] = "NO_DATA"
        base["causa"] = (
            f"ninguna correccion consentida entre los {len(filas)} turnos "
            f"mirados ({base['descartados']['sin_consentimiento']} sin "
            f"consentimiento, {base['descartados']['sin_correccion']} sin "
            "correccion). Cero pares no es un dataset limpio: es que no hay "
            "dataset")
        return base

    base["estado"] = "MEDIDO"
    base["como"] = ("pares con consent=1 y correccion no vacia, agrupados por "
                    "el modelo que los produjo")
    return base


def main(argv=None):
    ap = argparse.ArgumentParser(description="Bronze -> Silver")
    ap.add_argument("--db", default=os.path.expanduser("~/.preceptoros/memory.db"))
    ap.add_argument("--skill", default="general")
    ap.add_argument("--salida")
    a = ap.parse_args(argv)
    r = curar(a.db, a.skill)
    txt = json.dumps(r, ensure_ascii=False, indent=1) + "\n"
    if a.salida:
        open(a.salida, "w", encoding="utf-8").write(txt)
        print(f"escrito {a.salida}", file=sys.stderr)
    else:
        print(txt)
    print(f"{r['estado']} · {len(r['pares'])} pares de {r['mirados']} turnos",
          file=sys.stderr)
    # Sale 1 cuando no hay dataset. Un guion de la Forja que encadene con esto
    # tiene que PARAR, no seguir con las manos vacias.
    return 0 if r["estado"] == "MEDIDO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
