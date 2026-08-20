#!/usr/bin/env python3
"""FASE 2 · TRAINER GUARDIAN · LoRA en CPU sobre Qwen3-4B-Instruct.

NO es QLoRA. La Q de QLoRA es la cuantización NF4 de bitsandbytes, y ese kernel
es CUDA. En este metal --Radeon 780M integrada, sin NVIDIA-- lo que hay es LoRA
en bf16/fp32. Cabe de sobra en 40 GiB, porque en LoRA solo se entrenan los
adaptadores. Ver README §2 B1: el problema no era el espacio, era el nombre.

CERROJO DOBLE. Este guion no entrena hasta que se cumplan las dos:
  1. `--ejecutar`, explícito.
  2. FASE0_VEREDICTO.json existe y nombra un entrenador elegido.

Sin la segunda, entrenar sería elegir entrenador por intuición, que es
justamente lo que la Fase 0 existe para impedir.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
VEREDICTO = RAIZ / "FASE0_VEREDICTO.json"
DATASET = RAIZ / "data" / "lora_dataset.jsonl"
SALIDA = RAIZ / "salida"

BASE_HF = "Qwen/Qwen3-4B-Instruct-2507"     # los pesos sin cuantizar, no el GGUF

HIPER = {                                    # punto de partida, no dogma
    "rank": 16, "alpha": 32, "dropout": 0.05,
    "lr": 2e-4, "epocas": 3, "batch": 1, "acumulacion": 8,
    "max_len": 1024, "objetivo": ["q_proj", "k_proj", "v_proj", "o_proj"],
}


def veredicto():
    try:
        return json.loads(VEREDICTO.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def revisar():
    """Todo lo que falta, dicho de una vez. No se para en el primer hueco."""
    faltas = []
    v = veredicto()
    if v is None:
        faltas.append(f"no existe {VEREDICTO.name}: corre forja/minirun.py --escribir")
    elif not v.get("elegido"):
        faltas.append("el veredicto de la Fase 0 no nombra entrenador elegido")
    if not DATASET.is_file():
        faltas.append(f"no existe {DATASET}: datos/construir_dataset.py --ejecutar")
    if not shutil.which("llama-quantize"):
        faltas.append("llama-quantize no está: sin él no hay export a GGUF (Fase 2 §b)")
    return faltas, v


def main(argv=None):
    ap = argparse.ArgumentParser(description="FASE 2 · trainer guardian")
    ap.add_argument("--ejecutar", action="store_true")
    ap.add_argument("--version", default="v1")
    a = ap.parse_args(argv)

    faltas, v = revisar()
    print(f"[guardian-2] base: {BASE_HF} (pesos sin cuantizar, ~8 GB)")
    print(f"[guardian-2] LoRA r={HIPER['rank']} alpha={HIPER['alpha']} "
          f"lr={HIPER['lr']} epocas={HIPER['epocas']}")
    print(f"[guardian-2] entrenador elegido: {(v or {}).get('elegido') or 'NO_DATA'}")
    print(f"[guardian-2] salida prevista: {SALIDA / a.version}")

    if faltas:
        print("[guardian-2] BLOQUEADO · falta:")
        for f in faltas:
            print(f"    · {f}")
    if not a.ejecutar:
        print("[guardian-2] CERROJO: no se entrena. Añade --ejecutar")
        return 0
    if faltas:
        print("[guardian-2] no entreno con huecos. Paro.", file=sys.stderr)
        return 2

    print("[guardian-2] el bucle de entrenamiento se escribe contra el "
          "entrenador que firme la Fase 0, no antes: cada uno tiene su API y "
          "escribir para los tres es escribir tres veces mal.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
