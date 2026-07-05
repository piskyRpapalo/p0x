#!/usr/bin/env python3
"""gen_niveles.py — P0X mente/pipeline (Bloque G, misión OBSERVAR).

Genera `descripcion_niveles: {basico, medio, experto}` para cada nodo:
  - ESFERAS: se escribe en su front-matter con `generado_por:
    cc-pendiente-revision` (el Soberano puede editar/borrar el marcador).
  - DOCTRINA (clase=doctrina): el silicio JAMÁS edita el MD → sidecar
    mente/pipeline/niveles_doctrina.yaml que build_graph fusiona al proyectar.

Modelo: el cerebro batch elegido por dato en pipeline/delta_config.yaml.
Idempotente: salta nodos que ya tienen descripcion_niveles.
Correr encolado: p0x-enqueue python3 gen_niveles.py
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

import yaml

MENTE = Path(__file__).resolve().parent.parent
SIDECAR = Path(__file__).with_name("niveles_doctrina.yaml")
CFG = yaml.safe_load((MENTE.parent / "pipeline" / "delta_config.yaml")
                     .read_text(encoding="utf-8"))
OLLAMA = "http://localhost:11434/api/chat"

PROMPT = """Eres el pedagogo de P0X. Escribe en español, sobrio.

TÍTULO: {titulo}
TEXTO:
---
{cuerpo}
---

Resume este conocimiento en tres niveles de profundidad para un selector de UI:
- basico: 1-2 frases, para quien no conoce el tema (sin jerga).
- medio: 2-3 frases, con los conceptos clave nombrados.
- experto: 2-4 frases, denso, con los matices y términos técnicos del texto.

Fiel al texto: no añadas nada que no esté. Responde SOLO con JSON válido:
{{"basico": "...", "medio": "...", "experto": "..."}}"""


def _llm(prompt: str) -> dict | None:
    body = json.dumps({
        "model": CFG["model"],
        "messages": [{"role": "user", "content": prompt}],
        "stream": False, "keep_alive": "5m",
        "options": {"temperature": 0.2, "num_ctx": CFG["num_ctx"]},
    }).encode()
    req = urllib.request.Request(OLLAMA, data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=1800) as r:
        content = json.loads(r.read()).get("message", {}).get("content", "")
    s = content.strip()
    if s.startswith("```"):
        s = re.sub(r"^```(?:json)?\s*|\s*```$", "", s, flags=re.S)
    try:
        d = json.loads(s)
    except json.JSONDecodeError:
        i, j = s.find("{"), s.rfind("}")
        if not (0 <= i < j):
            return None
        try:
            d = json.loads(s[i:j + 1])
        except json.JSONDecodeError:
            return None
    if all(isinstance(d.get(k), str) and d[k].strip()
           for k in ("basico", "medio", "experto")):
        return {k: d[k].strip() for k in ("basico", "medio", "experto")}
    return None


def _split(md: Path) -> tuple[dict, str, str]:
    text = md.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, "", text
    end = lines[1:].index("---") + 1
    fm_raw = "\n".join(lines[1:end])
    body = "\n".join(lines[end + 1:])
    return yaml.safe_load(fm_raw) or {}, fm_raw, body


def procesar_esfera(md: Path) -> bool:
    fm, fm_raw, body = _split(md)
    if not fm or "descripcion_niveles" in fm:
        return False
    niveles = _llm(PROMPT.format(titulo=fm.get("titulo", md.stem),
                                 cuerpo=body.strip()[:4000]))
    if niveles is None:
        print(f"  WARN {md.name}: JSON inválido del modelo — saltada")
        return False
    bloque = ["descripcion_niveles:"]
    for k in ("basico", "medio", "experto"):
        bloque.append(f"  {k}: {json.dumps(niveles[k], ensure_ascii=False)}")
    bloque.append("generado_por: cc-pendiente-revision")
    nuevo = f"---\n{fm_raw}\n" + "\n".join(bloque) + f"\n---\n{body}"
    md.write_text(nuevo, encoding="utf-8")
    return True


def procesar_doctrina(md: Path, sidecar: dict) -> bool:
    fm, _, body = _split(md)
    nid = fm.get("id")
    if not nid or nid in sidecar:
        return False
    niveles = _llm(PROMPT.format(titulo=fm.get("titulo", md.stem),
                                 cuerpo=body.strip()[:4000]))
    if niveles is None:
        print(f"  WARN {md.name}: JSON inválido del modelo — saltada")
        return False
    niveles["generado_por"] = "cc-pendiente-revision"
    sidecar[nid] = niveles
    return True


def main() -> None:
    hechas = 0
    for md in sorted((MENTE / "esferas").glob("*.md")):
        print(f"[gen_niveles] esfera {md.name}")
        if procesar_esfera(md):
            hechas += 1
    sidecar = {}
    if SIDECAR.exists():
        sidecar = yaml.safe_load(SIDECAR.read_text(encoding="utf-8")) or {}
    n0 = len(sidecar)
    for md in sorted((MENTE / "doctrina").glob("*.md")):
        print(f"[gen_niveles] doctrina {md.name}")
        procesar_doctrina(md, sidecar)
    if len(sidecar) > n0:
        SIDECAR.write_text(
            "# GENERADO por gen_niveles.py (cc-pendiente-revision).\n"
            "# El MD de doctrina jamás se toca desde silicio: estos niveles\n"
            "# solo existen en la proyección del grafo (build_graph).\n"
            + yaml.safe_dump(sidecar, allow_unicode=True, sort_keys=True),
            encoding="utf-8")
    print(f"[gen_niveles] esferas escritas: {hechas}; "
          f"doctrinas en sidecar: {len(sidecar)}")


if __name__ == "__main__":
    main()
