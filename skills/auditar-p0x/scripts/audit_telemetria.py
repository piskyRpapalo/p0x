#!/usr/bin/env python3
"""audit_telemetria.py — Protocolo §3: la re-edición nace de datos.

Lee sinodo.jsonl y lengua.jsonl y calcula, SIN inventar:
- por voz: n, tasa grounded, tokens medios in/out, latencia media/p95
- por dominio·op (lengua): n, tasa valida, tokens, latencia
- cruza con el contrato de cada voz (n_medicion, umbral_reedicion):
  n < n_medicion → "sin línea base" (verdad honesta, no infracción)
  umbral numérico parseable Y cruzado Y n>=n_medicion → candidato re-edición
  umbral no parseable → se dice tal cual (jamás se adivina)
"""
import json
import re
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_lib import MENTE, escribir, infraccion, leer_frontmatter

TELE = MENTE / "telemetria"


def cargar(nombre):
    p = TELE / nombre
    if not p.exists():
        return []
    out = []
    for line in p.read_text(encoding="utf-8").splitlines():
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def stats(regs, campo_ok):
    n = len(regs)
    ok = sum(1 for r in regs if r.get(campo_ok))
    ms = sorted(r.get("ms", 0) for r in regs)
    return {
        "n": n,
        f"tasa_{campo_ok}": round(ok / n, 3) if n else None,
        "tok_in_medio": round(statistics.mean(r.get("tok_in", 0) for r in regs), 1) if n else None,
        "tok_out_medio": round(statistics.mean(r.get("tok_out", 0) for r in regs), 1) if n else None,
        "ms_medio": round(statistics.mean(ms), 0) if n else None,
        "ms_p95": ms[int(n * 0.95) - 1] if n >= 2 else (ms[0] if n else None),
    }


def umbral_tasa_fallo(texto):
    """Extrae un umbral numérico de fallo del texto libre de umbral_reedicion.
    Solo patrones inequívocos ('>10%', '>= 1/20'); si no, None (honesto)."""
    if not texto:
        return None
    m = re.search(r">\s*=?\s*(\d+(?:\.\d+)?)\s*%", str(texto))
    if m:
        return float(m.group(1)) / 100
    m = re.search(r">\s*=?\s*(\d+)\s*/\s*(\d+)", str(texto))
    if m:
        return int(m.group(1)) / int(m.group(2))
    return None


def main() -> int:
    inf = []
    sinodo = cargar("sinodo.jsonl")
    lengua = cargar("lengua.jsonl")

    por_voz = {}
    for r in sinodo:
        por_voz.setdefault(r.get("voz", "?"), []).append(r)
    voces = {}
    for voz, regs in sorted(por_voz.items()):
        s = stats(regs, "grounded")
        md = MENTE / "voces" / f"{voz}.md"
        fm, _ = leer_frontmatter(md) if md.exists() else (None, "")
        if fm:
            n_med = fm.get("n_medicion") or 0
            s["n_medicion"] = n_med
            s["linea_base"] = s["n"] >= n_med
            if not s["linea_base"]:
                s["nota"] = f"sin línea base (n={s['n']} < n_medicion={n_med})"
            else:
                u = umbral_tasa_fallo(fm.get("umbral_reedicion"))
                if u is None:
                    s["nota"] = ("umbral_reedicion no evaluable "
                                 "automáticamente (texto libre)")
                elif (1 - (s["tasa_grounded"] or 0)) > u:
                    inf.append(infraccion(f"mente/voces/{voz}.md",
                               "umbral-cruzado",
                               f"tasa no-grounded {1-(s['tasa_grounded'] or 0):.1%} > "
                               f"umbral {u:.0%} con n={s['n']}>=n_medicion — "
                               f"candidato a re-edición (§3)"))
        voces[voz] = s

    por_dom = {}
    for r in lengua:
        por_dom.setdefault(f"{r.get('dom','?')}·{r.get('op','?')}", []).append(r)
    dominios = {k: stats(v, "valida") for k, v in sorted(por_dom.items())}

    escribir("telemetria.json",
             {"auditor": "telemetria",
              "sinodo_registros": len(sinodo), "lengua_registros": len(lengua),
              "por_voz": voces, "por_dominio_op": dominios,
              "infracciones": inf})
    return 0


if __name__ == "__main__":
    sys.exit(main())
