#!/usr/bin/env python3
"""audit_frontmatter.py — contrato §2 del Protocolo del MD Evolutivo.

Verifica (determinista, evidencia por archivo):
- front-matter presente y parseable; id/titulo/tipo básicos
- tipo dentro del vocabulario §2 (+voz/observacion, ya en producción)
- si `clase` presente (MD evolutivo): contrato completo, semver,
  editor válido; clase=doctrina exige editor_autorizado=carbono
- presupuesto_kb no superado (si sí → categoria PODA, Protocolo §4.4)
- changelog append-only vs HEAD del git soberano (§4.3)
- enlaces resuelven a ids reales del árbol mente/
- ids duplicados y .bak-* dentro de mente/ (basura junto al conocimiento)
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_lib import (CAMPOS_EVOLUTIVO, EDITORES_VALIDOS, MENTE, P0X, SEMVER,
                       TIPOS_VALIDOS, escribir, infraccion, leer_frontmatter,
                       md_files, rel)


def changelog_head(path: Path):
    """Changelog de la versión en HEAD (None si el archivo es nuevo)."""
    r = subprocess.run(["git", "-C", str(P0X), "show", f"HEAD:{rel(path)}"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return None
    import re
    import yaml
    m = re.match(r"^---\n(.*?)\n---", r.stdout, re.S)
    if not m:
        return None
    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        return None
    return (fm or {}).get("changelog") if isinstance(fm, dict) else None


def main() -> int:
    vivos, baks = md_files()
    inf = []
    ids = {}

    for p in vivos:
        fm, _ = leer_frontmatter(p)
        if fm is None:
            inf.append(infraccion(p, "sin-front-matter",
                                  "sin front-matter YAML parseable"))
            continue
        for campo in ("id", "titulo", "tipo"):
            if not fm.get(campo):
                inf.append(infraccion(p, "campo-basico-ausente",
                                      f"falta `{campo}`"))
        fid = fm.get("id")
        if fid:
            if fid in ids:
                inf.append(infraccion(p, "id-duplicado",
                                      f"id `{fid}` ya usado por {ids[fid]}"))
            ids[fid] = rel(p)
        tipo = fm.get("tipo")
        if tipo and tipo not in TIPOS_VALIDOS:
            inf.append(infraccion(p, "tipo-fuera-vocabulario",
                                  f"tipo `{tipo}` no está en §2 ni en el "
                                  f"vocabulario en producción"))

        if "clase" in fm:  # MD evolutivo: contrato completo
            faltan = [c for c in CAMPOS_EVOLUTIVO if c not in fm]
            if faltan:
                inf.append(infraccion(p, "contrato-evolutivo-incompleto",
                                      f"clase={fm['clase']} sin: "
                                      + ", ".join(faltan)))
            v = str(fm.get("version", ""))
            if v and not SEMVER.match(v):
                inf.append(infraccion(p, "version-no-semver",
                                      f"version `{v}` no es MAJOR.MINOR.PATCH"))
            ed = fm.get("editor_autorizado")
            if ed and ed not in EDITORES_VALIDOS:
                inf.append(infraccion(p, "editor-invalido",
                                      f"editor_autorizado `{ed}`"))
            if fm["clase"] == "doctrina" and ed not in (None, "carbono"):
                inf.append(infraccion(p, "correa-mal-atada",
                                      f"clase=doctrina con editor `{ed}` — "
                                      f"solo el carbono canoniza (§1)"))
            kb = fm.get("presupuesto_kb")
            if isinstance(kb, (int, float)) and kb > 0:
                real = p.stat().st_size / 1024
                if real > kb:
                    inf.append(infraccion(p, "PODA",
                                          f"{real:.1f}KB > presupuesto "
                                          f"{kb}KB — poda obligatoria (§4.4)"))
            nuevo = fm.get("changelog")
            viejo = changelog_head(p)
            if isinstance(viejo, list) and isinstance(nuevo, list):
                if len(nuevo) < len(viejo) or nuevo[:len(viejo)] != viejo:
                    inf.append(infraccion(p, "changelog-reescrito",
                                          "el changelog del worktree no es "
                                          "append-only sobre HEAD (§4.3)"))

    # enlaces resuelven (segunda pasada, con el censo de ids completo).
    # Resolución IDÉNTICA a build_graph.py:93-96: id completo O slug pelado
    # (id.split('-',1)[-1], convención de las esferas) — divergir aquí
    # fabricaría falsos rotos que el grafo sí resuelve (afinado en B4).
    slugs = set(ids)
    for fid in ids:
        slugs.add(fid.split("-", 1)[-1])
    for p in vivos:
        fm, _ = leer_frontmatter(p)
        if not fm:
            continue
        enlaces = fm.get("enlaces") or []
        if isinstance(enlaces, list):
            for e in enlaces:
                if isinstance(e, str) and e and e not in slugs:
                    inf.append(infraccion(p, "enlace-roto",
                                          f"enlace `{e}` no resuelve a "
                                          f"ningún id/slug de mente/ "
                                          f"(resolución de build_graph)"))

    for b in baks:
        inf.append(infraccion(b, "basura-en-mente",
                              "backup junto al conocimiento — mover fuera "
                              "de SCOPE_DIRS o borrar (ya está en git)"))

    escribir("frontmatter.json",
             {"auditor": "frontmatter", "archivos_auditados": len(vivos),
              "ids_censados": len(ids), "infracciones": inf})
    return 0


if __name__ == "__main__":
    sys.exit(main())
