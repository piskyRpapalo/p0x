#!/usr/bin/env python3
"""FASE 5 · HEALTH GUARDIAN · lee la bitácora y avisa si no converge. Stdlib.

No entrena, no toca modelos. Lee lo que dejaron las fases 2 y 3 y responde a
una sola pregunta: ¿esto va a algún sitio?

«No converge» se define aquí y se mide, en vez de dejarse a la vista de quien
mire la gráfica: la pérdida de la última ventana no mejora la de la anterior
en al menos `MEJORA_MIN`.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
VENTANA = 20
MEJORA_MIN = 0.01


def leer_perdidas(ruta):
    valores = []
    try:
        for linea in ruta.open(encoding="utf-8"):
            linea = linea.strip()
            if not linea:
                continue
            try:
                d = json.loads(linea)
            except json.JSONDecodeError:
                continue
            if isinstance(d.get("loss"), (int, float)):
                valores.append(float(d["loss"]))
    except OSError:
        return None
    return valores


def converge(v):
    if len(v) < VENTANA * 2:
        return None, f"solo {len(v)} pasos · hacen falta {VENTANA*2}"
    antes = sum(v[-VENTANA*2:-VENTANA]) / VENTANA
    ahora = sum(v[-VENTANA:]) / VENTANA
    mejora = antes - ahora
    return mejora >= MEJORA_MIN, f"{antes:.4f} → {ahora:.4f} (mejora {mejora:+.4f})"


def main(argv=None):
    ap = argparse.ArgumentParser(description="FASE 5 · health guardian")
    ap.add_argument("--perdidas", type=Path, default=RAIZ / "salida" / "loss.jsonl")
    ap.add_argument("--informe", type=Path, default=RAIZ / "salida" / "tester.json")
    a = ap.parse_args(argv)

    alerta = False
    medido = False

    v = leer_perdidas(a.perdidas)
    if v is None:
        print(f"[guardian-5] NO_DATA · no existe {a.perdidas}")
    else:
        medido = True
        ok, detalle = converge(v)
        if ok is None:
            print(f"[guardian-5] pérdida: aún no medible · {detalle}")
        elif ok:
            print(f"[guardian-5] pérdida: converge · {detalle}")
        else:
            print(f"[guardian-5] ALERTA · la pérdida no baja · {detalle}")
            alerta = True

    try:
        inf = json.loads(a.informe.read_text(encoding="utf-8"))
        tasa, umbral = inf.get("tasa", 0.0), inf.get("umbral", 0.10)
        medido = True
        print(f"[guardian-5] tests: fallo {tasa:.0%} (umbral {umbral:.0%})")
        if tasa > umbral:
            print("[guardian-5] ALERTA · el afinado no pasa la suite")
            alerta = True
    except (OSError, json.JSONDecodeError):
        print(f"[guardian-5] NO_DATA · no existe {a.informe}")

    if alerta:
        print("[guardian-5] ROJO · hay algo que mirar antes de promover")
        return 1
    if not medido:
        # Sin dato no se dice "sano": eso seria fabricar un sensor deshonesto
        # encima de uno honesto. NO_DATA es una respuesta, "verde" no lo es.
        print("[guardian-5] NO_DATA · no hay nada medido todavia. No digo sano.")
        return 2
    print("[guardian-5] sin alertas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
