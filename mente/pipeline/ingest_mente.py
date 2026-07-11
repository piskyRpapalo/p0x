"""
ingest_mente.py — P0X mente/pipeline
ORQUESTADOR: recorre mente/{codice,corpus,esferas,doctrina,voces}/**.md, decide qué
reindexar por hash sha256 (manifiesto local), y para lo que cambió corre
chunk -> embed -> to_qdrant. Al final siempre regenera grafo/second_brain.json.

Pensado para correr encolado: p0x-enqueue python3 ingest_mente.py
(serializado vía task-spooler, nice/ionice, no compite con Faro/Gateway).

Ámbito EXCLUIDO a propósito: mente/tecnicas/*.json (formato distinto, es el
registro de técnicas de registro_tecnicas/models.py) y mente/pipeline/ (código,
no contenido).
"""
import hashlib
import json
import sys
from pathlib import Path

MENTE_ROOT = Path(__file__).resolve().parent.parent
PIPELINE_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = PIPELINE_DIR / ".ingest_manifest.json"

sys.path.insert(0, str(PIPELINE_DIR))

import build_graph  # noqa: E402
from chunk import chunk_markdown  # noqa: E402
from embed import embed_batch  # noqa: E402
from to_qdrant import ensure_collection, get_client, replace_file_points  # noqa: E402

SCOPE_DIRS = ["codice", "corpus", "esferas", "doctrina", "voces", "lengua", "manual", "reflejos"]


def _iter_md_files():
    for d in SCOPE_DIRS:
        base = MENTE_ROOT / d
        if base.exists():
            yield from sorted(base.glob("**/*.md"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_manifest() -> dict:
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text())
    return {}


def _save_manifest(manifest: dict) -> None:
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def _strip_frontmatter(text: str) -> tuple[str, dict | None]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return text, None
    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        return text, None
    import yaml

    block = "\n".join(lines[1:end])
    try:
        fm = yaml.safe_load(block)
    except yaml.YAMLError:
        fm = None
    body = "\n".join(lines[end + 1:])
    return body, (fm if isinstance(fm, dict) else None)


def _metadata_from_frontmatter(fm: dict | None) -> dict:
    if fm is None:
        return {"id": None, "tipo": None, "capa": None, "esfera": None, "evidencia_fuerza": None, "fuente": None}
    node_id = fm.get("id")
    tipo = fm.get("tipo")
    slug = node_id.split("-", 1)[-1] if node_id else None
    return {
        "id": node_id,
        "tipo": tipo,
        "capa": fm.get("capa_codice"),
        "esfera": slug if tipo == "esfera" else None,
        "evidencia_fuerza": fm.get("evidencia_fuerza"),
        "fuente": fm.get("fuente"),
    }


def main() -> None:
    manifest = _load_manifest()
    client = get_client()
    ensure_collection(client)

    total_files = 0
    reindexed_files = 0
    total_points = 0

    for md_path in _iter_md_files():
        # sigue symlinks (CODICE_david.md) para leer el contenido real
        real_path = md_path.resolve()
        rel_path = str(md_path.relative_to(MENTE_ROOT))
        total_files += 1
        digest = _sha256(real_path)

        if manifest.get(rel_path) == digest:
            print(f"[ingest_mente] sin cambios, salto: {rel_path}")
            continue

        text = real_path.read_text(encoding="utf-8")
        body, fm = _strip_frontmatter(text)
        chunks = chunk_markdown(body)
        metadata = _metadata_from_frontmatter(fm)

        if not chunks:
            n_points = replace_file_points(client, rel_path, [], metadata)
        else:
            vectors = embed_batch([c.text for c in chunks])
            triples = [(c.index, c.text, v.tolist()) for c, v in zip(chunks, vectors)]
            n_points = replace_file_points(client, rel_path, triples, metadata)

        print(f"[ingest_mente] reindexado: {rel_path} -> {n_points} chunks")
        manifest[rel_path] = digest
        reindexed_files += 1
        total_points += n_points

    _save_manifest(manifest)

    graph = build_graph.build_graph()
    build_graph.write_graph(graph)

    print(
        f"[ingest_mente] listo: {total_files} archivos vistos, "
        f"{reindexed_files} reindexados, {total_points} chunks nuevos, "
        f"grafo {len(graph['nodes'])} nodes / {len(graph['links'])} links"
    )


if __name__ == "__main__":
    main()
