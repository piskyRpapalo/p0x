"""
to_qdrant.py — P0X mente/pipeline
Upsert idempotente de chunks embebidos a Qdrant, colección 'mente' (768-d,
Cosine — mismo esquema que la colección hermana hexelion_sinodo_memory).

La API key NO vive en hw.yaml (es un secreto). Se lee de $QDRANT_API_KEY o,
si no está exportada, de /home/ubuntu/hexelion/config/.env (solo lectura).
"""
import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

import yaml
from qdrant_client import QdrantClient
from qdrant_client.http import models as qm

HW = yaml.safe_load(Path(__file__).with_name("hw.yaml").read_text())
_Q = HW["qdrant"]
COLLECTION = _Q["collection"]
DIMS = HW["ollama_embed"]["dims"]
_NAMESPACE = uuid.UUID("d7f6a5e4-b3c2-41d0-9f8e-7c6b5a4d3e2f")  # namespace fijo para uuid5 estable


def _load_api_key() -> str:
    key = os.environ.get("QDRANT_API_KEY")
    if key:
        return key
    env_path = Path("/home/ubuntu/hexelion/config/.env")
    if env_path.exists():
        m = re.search(r"^QDRANT_API_KEY=(.+)$", env_path.read_text(), re.MULTILINE)
        if m:
            return m.group(1).strip()
    raise RuntimeError(
        "QDRANT_API_KEY no encontrada (ni en entorno ni en hexelion/config/.env)"
    )


def get_client() -> QdrantClient:
    # https=False explicito: qdrant-client asume TLS en cuanto ve api_key,
    # pero este Qdrant self-hosted (hexelion-qdrant) habla HTTP plano en tailnet.
    return QdrantClient(host=_Q["host"], port=_Q["port"], api_key=_load_api_key(), https=False)


def ensure_collection(client: QdrantClient) -> None:
    existing = {c.name for c in client.get_collections().collections}
    if COLLECTION not in existing:
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=qm.VectorParams(size=DIMS, distance=qm.Distance.COSINE),
            on_disk_payload=True,
        )


def _point_id(rel_path: str, chunk_index: int) -> str:
    return str(uuid.uuid5(_NAMESPACE, f"{rel_path}:{chunk_index}"))


def replace_file_points(
    client: QdrantClient,
    rel_path: str,
    chunks_with_vectors: list[tuple[int, str, list[float]]],
    metadata: dict,
) -> int:
    """Reemplaza TODOS los puntos de rel_path (borra + inserta) — idempotente
    incluso si el archivo encoge (evita chunks huérfanos)."""
    client.delete(
        collection_name=COLLECTION,
        points_selector=qm.FilterSelector(
            filter=qm.Filter(must=[qm.FieldCondition(key="path", match=qm.MatchValue(value=rel_path))])
        ),
    )
    if not chunks_with_vectors:
        return 0
    now = datetime.now(timezone.utc).isoformat()
    points = [
        qm.PointStruct(
            id=_point_id(rel_path, idx),
            vector=vec,
            payload={
                "path": rel_path,
                "chunk_index": idx,
                "text": text,
                "updated_at": now,
                **metadata,
            },
        )
        for idx, text, vec in chunks_with_vectors
    ]
    client.upsert(collection_name=COLLECTION, points=points)
    return len(points)
