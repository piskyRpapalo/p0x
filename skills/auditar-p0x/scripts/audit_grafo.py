#!/usr/bin/env python3
"""audit_grafo.py — coherencia second_brain.json ↔ MDs fuente.

Verifica (determinista):
- nodos huérfanos (grado 0) y aristas con extremo inexistente
- tipos de nodo fuera de vocabulario
- MD indexable sin nodo en el grafo / nodo sin MD fuente
- esferas sin descripcion_niveles (selector básico/medio/experto vacío)
- fuga de Necrópolis al grafo (guardia af5325f — crítico si reaparece)
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_lib import MENTE, TIPOS_VALIDOS, escribir, infraccion, \
    leer_frontmatter, md_files

GRAFO = MENTE / "grafo" / "second_brain.json"


def main() -> int:
    inf = []
    if not GRAFO.exists():
        escribir("grafo.json", {"auditor": "grafo", "error":
                 "second_brain.json no existe — correr ingest_mente",
                 "infracciones": [infraccion(GRAFO, "grafo-ausente",
                                             "no hay grafo que auditar")]})
        return 0
    g = json.loads(GRAFO.read_text(encoding="utf-8"))
    nodos = {n["id"]: n for n in g.get("nodes", [])}
    links = g.get("links", g.get("edges", []))

    grado = {i: 0 for i in nodos}
    for l in links:
        s, t = l.get("source"), l.get("target")
        for extremo in (s, t):
            if extremo not in nodos:
                inf.append(infraccion("mente/grafo/second_brain.json",
                                      "arista-rota",
                                      f"arista {s}→{t}: `{extremo}` no es nodo"))
            else:
                grado[extremo] += 1

    for i, n in nodos.items():
        if grado[i] == 0:
            inf.append(infraccion("mente/grafo/second_brain.json",
                                  "nodo-huerfano", f"`{i}` sin ninguna arista"))
        tipo = n.get("tipo")
        if tipo and tipo not in TIPOS_VALIDOS:
            inf.append(infraccion("mente/grafo/second_brain.json",
                                  "tipo-fuera-vocabulario",
                                  f"nodo `{i}` tipo `{tipo}`"))
        if n.get("tipo") == "esfera" and not n.get("descripcion_niveles"):
            inf.append(infraccion("mente/grafo/second_brain.json",
                                  "esfera-sin-niveles",
                                  f"esfera `{i}` sin descripcion_niveles "
                                  f"(gen_niveles.py pendiente sobre ella)"))

    # espejo MD ↔ grafo
    vivos, _ = md_files()
    ids_md = {}
    for p in vivos:
        fm, _ = leer_frontmatter(p)
        if fm and fm.get("id"):
            ids_md[fm["id"]] = p
    for fid, p in ids_md.items():
        if fid not in nodos and "feedback" not in str(p):
            inf.append(infraccion(p, "md-fuera-del-grafo",
                                  f"id `{fid}` indexable pero sin nodo — "
                                  f"¿re-ingesta pendiente?"))
    for i in nodos:
        if i not in ids_md:
            inf.append(infraccion("mente/grafo/second_brain.json",
                                  "nodo-sin-fuente",
                                  f"nodo `{i}` sin MD fuente en mente/"))

    # fuga de necrópolis (la guardia que ya se cazó una vez)
    necro = MENTE / "necropolis"
    if necro.is_dir():
        tumbas = {d.name for d in necro.iterdir() if d.is_dir()}
        for i in nodos:
            if any(t in i for t in tumbas):
                inf.append(infraccion("mente/grafo/second_brain.json",
                                      "fuga-necropolis",
                                      f"nodo `{i}` referencia una tumba"))

    escribir("grafo.json", {"auditor": "grafo", "nodos": len(nodos),
                            "aristas": len(links), "infracciones": inf})
    return 0


if __name__ == "__main__":
    sys.exit(main())
