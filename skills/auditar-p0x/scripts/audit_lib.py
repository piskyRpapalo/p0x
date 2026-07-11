"""audit_lib.py — utilidades compartidas de los auditores de higiene P0X.

Deterministas, stdlib+yaml. Cero LLM aquí. Cada infracción es un dict:
  {"archivo": <rel>, "categoria": <slug>, "detalle": <es>, "severidad": ...}
La severidad la asigna audit_report.py por tabla — los auditores solo
recogen EVIDENCIA.
"""
import json
import os
import re
from pathlib import Path

import yaml

P0X = Path(os.environ.get("P0X_ROOT", "/mnt/nvme/p0x"))
MENTE = P0X / "mente"
OUT = MENTE / "auditorias" / "out"

# Dirs de conocimiento indexado (ingest_mente.SCOPE_DIRS) — el contrato §2
# rige ahí; feedback/telemetria/auditorias son registro operativo con
# contrato propio y necropolis es tumba (jamás se audita como vivo).
SCOPE_DIRS = ("codice", "corpus", "esferas", "doctrina", "voces", "lengua", "manual", "reflejos")

TIPOS_VALIDOS = {"doctrina", "operativo", "esfera", "principio", "tecnica",
                 "voz", "observacion"}
EDITORES_VALIDOS = {"carbono", "silicio-telemetria"}
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
CAMPOS_EVOLUTIVO = ("version", "editor_autorizado", "metrica_exito",
                    "umbral_reedicion", "presupuesto_kb", "n_medicion",
                    "changelog")


def md_files():
    """Todos los .md vivos bajo SCOPE_DIRS + feedback (PENDIENTES tiene
    contrato evolutivo). Los .bak-* se devuelven aparte: son infracción."""
    vivos, baks = [], []
    for d in SCOPE_DIRS + ("feedback",):
        base = MENTE / d
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*")):
            if not p.is_file():
                continue
            if ".bak" in p.name:
                baks.append(p)
            elif p.suffix == ".md":
                vivos.append(p)
    return vivos, baks


def leer_frontmatter(path: Path):
    """(front-matter dict | None, cuerpo). None si no hay FM parseable."""
    txt = path.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\n(.*?)\n---\n?", txt, re.S)
    if not m:
        return None, txt
    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        return None, txt
    return (fm if isinstance(fm, dict) else None), txt[m.end():]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(P0X))
    except ValueError:
        return str(path)


def infraccion(archivo, categoria: str, detalle: str) -> dict:
    return {"archivo": rel(archivo) if isinstance(archivo, Path) else archivo,
            "categoria": categoria, "detalle": detalle}


def escribir(nombre: str, data: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / nombre
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                 encoding="utf-8")
    print(f"{nombre}: {len(data.get('infracciones', []))} infracciones "
          f"→ {rel(p)}")
