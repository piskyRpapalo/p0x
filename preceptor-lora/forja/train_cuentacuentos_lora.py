#!/usr/bin/env python3
"""FORJA · el LoRA Cuentacuentos sobre Mistral, en CPU.

QUE ENTRENA Y POR QUE ESTE CAMINO
---------------------------------
`peft` afina PESOS, y un GGUF cuantizado no son pesos afinables: por eso la base
NO es `mistral:7b-instruct-v0.3-q4_K_M` --lo que sirve Ollama-- sino el
safetensors fp16 del repo oficial, que resulta no estar capado. El Q4 es para
servir; el fp16 es para entrenar. Confundirlos cuesta una tarde.

Se descarto `llama-finetune`: su `--lora` solo CARGA un adaptador, no lo entrena.

HIPERPARAMETROS PRESTADOS, NO COPIADOS
--------------------------------------
`rank`, `alpha`, `dropout`, `lr` y los modulos objetivo se importan de
`entrenar_sft_cot.py`, donde el Soberano los firmo el 2026-08-21. Copiarlos aqui
crearia dos verdades sobre el mismo numero, y la segunda envejeceria sola.

PROPOSE-ONLY POR DEFECTO
------------------------
Sin `--ejecutar` no entrena: imprime el plan y para. Es la misma guarda que ya
lleva el trainer hermano, y existe porque un entrenamiento lanzado por accidente
en CPU ocupa la maquina durante horas.

PARADA LIMPIA (IronClaw)
------------------------
SIGINT y SIGTERM no matan el proceso a media escritura: levantan una bandera, el
bucle termina el paso en curso, guarda lo que haya y sale diciendo por que. Un
adaptador a medio escribir es peor que ninguno, porque parece un adaptador.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import logging
import os
import resource
import signal
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent          # preceptor-lora/
P0X = RAIZ.parent
DATASET = P0X / "mente" / "datasets" / "sft_cuentacuentos_mistral_sample.jsonl"
SALIDA = RAIZ / "adapters" / "cuentacuentos_mistral_v1"
REGISTRO = SALIDA / "training.log"
BASE = "mistralai/Mistral-7B-Instruct-v0.3"

# Los hiperparametros firmados viven en un solo sitio.
_spec = importlib.util.spec_from_file_location(
    "entrenar_sft_cot", Path(__file__).with_name("entrenar_sft_cot.py"))
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
HIPER = dict(_mod.HIPER)

PARAR = {"pedido": False, "senal": None}


def _bandera(sig, _frame):
    PARAR["pedido"] = True
    PARAR["senal"] = signal.Signals(sig).name


def diario(destino):
    destino.parent.mkdir(parents=True, exist_ok=True)
    log = logging.getLogger("forja")
    log.setLevel(logging.INFO)
    formato = logging.Formatter("%(asctime)s  %(message)s", "%H:%M:%S")
    for h in (logging.FileHandler(destino, encoding="utf-8"),
              logging.StreamHandler(sys.stdout)):
        h.setFormatter(formato)
        log.addHandler(h)
    return log


def temperatura():
    """El Tctl del k10temp, por NOMBRE. Los numeros de hwmon los reparte el
    kernel en el orden en que aparecen los drivers."""
    base = Path("/sys/class/hwmon")
    for d in sorted(base.glob("hwmon*")):
        try:
            if (d / "name").read_text().strip() == "k10temp":
                return int((d / "temp1_input").read_text()) / 1000.0
        except OSError:
            continue
    return None


def ram_pico_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def ram_libre_mb():
    for linea in Path("/proc/meminfo").read_text().splitlines():
        if linea.startswith("MemAvailable:"):
            return int(linea.split()[1]) / 1024.0
    return None


def cargar(ruta):
    """El dataset en formato Alpaca: instruction, input, output."""
    fuera = []
    for linea in ruta.open(encoding="utf-8"):
        linea = linea.strip()
        if not linea:
            continue
        r = json.loads(linea)
        faltan = {"instruction", "input", "output"} - set(r)
        if faltan:
            raise SystemExit(f"muestra sin {sorted(faltan)}: {linea[:70]}")
        fuera.append(r)
    return fuera


def a_texto(muestra, tok):
    """Formato de turno de Mistral, por su PLANTILLA, no a mano.

    Escribir `[INST] ... [/INST]` a mano funciona hasta que la plantilla del
    modelo cambia y nadie se entera. El tokenizador la trae dentro.
    """
    usuario = muestra["instruction"]
    if muestra["input"]:
        usuario += "\n\n" + muestra["input"]
    return tok.apply_chat_template(
        [{"role": "user", "content": usuario},
         {"role": "assistant", "content": muestra["output"]}],
        tokenize=False)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ejecutar", action="store_true",
                    help="sin esto no entrena: imprime el plan y para")
    ap.add_argument("--base", default=BASE)
    ap.add_argument("--dataset", type=Path, default=DATASET)
    ap.add_argument("--salida", type=Path, default=SALIDA)
    ap.add_argument("--pasos", type=int, default=10,
                    help="prueba de concepto; 0 = una epoca entera")
    ap.add_argument("--hilos", type=int, default=8)
    # fp32 son 28 GB SOLO de pesos para un 7B, sobre ~38 disponibles: no cabe con
    # holgura y el primer pico de activaciones lo tumba. bf16 son 14, y este
    # Ryzen lo tiene en hardware. El adaptador se entrena igual en fp32 porque
    # `peft` sube sus propias capas.
    ap.add_argument("--dtype", default="bfloat16",
                    choices=["bfloat16", "float32"])
    ap.add_argument("--medir", action="store_true",
                    help="entrena SOLO --pasos y reporta segundos por paso, "
                         "pico de RAM y temperatura. Para dimensionar, no para servir")
    a = ap.parse_args(argv)

    muestras = cargar(a.dataset)
    plan = {
        "base": a.base, "dataset": str(a.dataset), "muestras": len(muestras),
        "salida": str(a.salida), "pasos": a.pasos or "una epoca",
        "lora": {k: HIPER[k] for k in ("rank", "alpha", "dropout", "lr")},
        "objetivo": HIPER["objetivo"], "max_len": HIPER["max_len"],
        "hilos": a.hilos, "dtype": a.dtype,
        "ram_libre_mb": round(ram_libre_mb() or 0),
        "temp_c": temperatura(),
    }
    if not a.ejecutar:
        print(json.dumps(plan, ensure_ascii=False, indent=1))
        print("\nPLAN, no ejecucion. Anade --ejecutar cuando el carbono firme.")
        return 0

    a.salida.mkdir(parents=True, exist_ok=True)
    log = diario(a.salida / REGISTRO.name)
    for s in (signal.SIGINT, signal.SIGTERM):
        signal.signal(s, _bandera)

    import torch                                          # noqa: PLC0415
    from peft import LoraConfig, get_peft_model           # noqa: PLC0415
    from transformers import AutoModelForCausalLM, AutoTokenizer  # noqa: PLC0415

    torch.set_num_threads(a.hilos)
    log.info("plan · %s", json.dumps(plan, ensure_ascii=False))

    t0 = time.monotonic()
    tok = AutoTokenizer.from_pretrained(a.base)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    modelo = AutoModelForCausalLM.from_pretrained(
        a.base, dtype=getattr(torch, a.dtype), low_cpu_mem_usage=True)
    log.info("base cargada en %.0f s · RAM pico %.0f MiB · libre %.0f MiB",
             time.monotonic() - t0, ram_pico_mb(), ram_libre_mb() or 0)

    modelo = get_peft_model(modelo, LoraConfig(
        r=HIPER["rank"], lora_alpha=HIPER["alpha"], lora_dropout=HIPER["dropout"],
        bias="none", task_type="CAUSAL_LM", target_modules=HIPER["objetivo"]))
    entrenables = sum(p.numel() for p in modelo.parameters() if p.requires_grad)
    total = sum(p.numel() for p in modelo.parameters())
    log.info("adaptador · %s entrenables de %s (%.3f%%)",
             f"{entrenables:,}", f"{total:,}", 100 * entrenables / total)

    textos = [a_texto(m, tok) for m in muestras]
    opt = torch.optim.AdamW(
        [p for p in modelo.parameters() if p.requires_grad], lr=HIPER["lr"])
    modelo.train()

    pasos = a.pasos or len(textos)
    tiempos, perdidas = [], []
    for paso in range(pasos):
        if PARAR["pedido"]:
            log.info("parada limpia pedida por %s · se guarda lo que hay",
                     PARAR["senal"])
            break
        ini = time.monotonic()
        lote = tok(textos[paso % len(textos)], return_tensors="pt",
                   truncation=True, max_length=HIPER["max_len"])
        lote["labels"] = lote["input_ids"].clone()
        salida = modelo(**lote)
        salida.loss.backward()
        opt.step()
        opt.zero_grad()
        dt = time.monotonic() - ini
        tiempos.append(dt)
        perdidas.append(float(salida.loss))
        log.info("paso %d/%d · perdida %.4f · %.1f s · RAM pico %.0f MiB · %s C",
                 paso + 1, pasos, perdidas[-1], dt, ram_pico_mb(),
                 temperatura())

    modelo.save_pretrained(str(a.salida))
    medida = {
        "dtype": a.dtype,
        "fecha": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "base": a.base, "pasos_hechos": len(tiempos),
        "segundos_por_paso": round(sum(tiempos) / max(len(tiempos), 1), 2),
        "perdida_primera": round(perdidas[0], 4) if perdidas else None,
        "perdida_ultima": round(perdidas[-1], 4) if perdidas else None,
        "ram_pico_mb": round(ram_pico_mb()),
        "temp_final_c": temperatura(),
        "parado_por": PARAR["senal"],
        "solo_medicion": bool(a.medir),
    }
    (a.salida / "medida.json").write_text(
        json.dumps(medida, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    log.info("guardado en %s · %s", a.salida, json.dumps(medida, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
