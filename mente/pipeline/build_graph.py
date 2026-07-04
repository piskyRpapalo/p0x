"""
build_graph.py — P0X mente/pipeline
Lee el front-matter de grafo de TODO .md en mente/** y escribe
grafo/second_brain.json — la PROYECCIÓN derivada (no fuente de verdad).

Archivos sin front-matter YAML válido (p.ej. CODICE_david.md, que usa un
comentario HTML como cabecera) se OMITEN del grafo con aviso — no se les
inventa un `tipo` fuera del enum del doc de arquitectura
(esfera|principio|tecnica|fracaso|analogia|doctrina|voz). Siguen indexados en
Qdrant para búsqueda vía ingest_mente.py; solo no aparecen como nodo aquí.
"""
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

import yaml

MENTE_ROOT = Path(__file__).resolve().parent.parent
GRAFO_OUT = MENTE_ROOT / "grafo" / "second_brain.json"
DEST_ASSETS = Path("/home/ubuntu/hexelion/assets/second_brain.json")

FRONTMATTER_RE_START = "---"


def _extract_descripcion(body_lines: list[str]) -> str:
    """Cuerpo del .md tras el front-matter, sin el H1 (ya está en 'titulo').
    Texto plano recortado — es lo que pinta el panel lateral de la pagina grande."""
    lines = [ln for ln in body_lines if not ln.strip().startswith("# ")]
    text = "\n".join(lines).strip()
    # colapsa lineas en blanco repetidas
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    return text


def _parse_frontmatter(md_path: Path) -> dict | None:
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != FRONTMATTER_RE_START:
        return None
    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        return None
    block = "\n".join(lines[1:end])
    try:
        data = yaml.safe_load(block)
    except yaml.YAMLError:
        return None
    if not isinstance(data, dict) or "id" not in data:
        return None
    data["descripcion"] = _extract_descripcion(lines[end + 1:])
    return data


def _label(titulo: str) -> str:
    return titulo.split(" / ")[0].strip() if titulo else titulo


def build_graph() -> dict:
    md_files = sorted(MENTE_ROOT.glob("**/*.md"))
    fm_by_id: dict[str, dict] = {}
    skipped: list[str] = []

    for md in md_files:
        fm = _parse_frontmatter(md)
        if fm is None:
            skipped.append(str(md.relative_to(MENTE_ROOT)))
            continue
        fm_by_id[fm["id"]] = fm

    # 'enlaces' se resuelve por slug pelado (convención esferas: "redes-linux")
    # O por id completo (convención doctrina: "doctrina-ai-interna") — aditivo,
    # no reemplaza la resolución por slug pelado ya usada por las esferas.
    slug_to_id: dict[str, str] = {}
    for node_id in fm_by_id:
        slug_to_id[node_id] = node_id
        slug_to_id.setdefault(node_id.split("-", 1)[-1], node_id)

    edge_pairs: set[tuple[str, str]] = set()
    for node_id, fm in fm_by_id.items():
        for slug in fm.get("enlaces") or []:
            target_id = slug_to_id.get(slug)
            if target_id is None or target_id == node_id:
                continue
            edge_pairs.add(tuple(sorted((node_id, target_id))))

    degree: dict[str, int] = {node_id: 0 for node_id in fm_by_id}
    for a, b in edge_pairs:
        degree[a] += 1
        degree[b] += 1

    nodes = [
        {
            "id": node_id,
            "label": _label(fm.get("titulo", node_id)),
            "tipo": fm.get("tipo"),
            "nivel": fm.get("nivel"),
            "size": degree[node_id],
            "descripcion": fm.get("descripcion", ""),
        }
        for node_id, fm in sorted(fm_by_id.items())
    ]
    links = [{"source": a, "target": b} for a, b in sorted(edge_pairs)]

    if skipped:
        print(f"[build_graph] omitidos (sin front-matter YAML valido): {skipped}")

    return {
        "nodes": nodes,
        "links": links,
        "meta": {
            "generado": datetime.now(timezone.utc).isoformat(),
            "fuente": "mente/**",
            "solo_lectura": True,
        },
    }


def write_graph(graph: dict) -> None:
    GRAFO_OUT.parent.mkdir(parents=True, exist_ok=True)
    GRAFO_OUT.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
    # copia (no symlink) a assets/: con follow_symlink=False en StaticFiles el JSON
    # se sirve igual desde /assets sin ampliar lo servible con un enlace hacia fuera
    # del directorio montado; se refresca en cada ingesta porque este write corre
    # en cada llamada real del pipeline (ver ingest_mente.py).
    shutil.copy(GRAFO_OUT, DEST_ASSETS)


def main() -> None:
    graph = build_graph()
    write_graph(graph)
    print(f"[build_graph] {len(graph['nodes'])} nodes, {len(graph['links'])} links -> {GRAFO_OUT}")


if __name__ == "__main__":
    main()
