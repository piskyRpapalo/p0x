"""
embed.py — P0X mente/pipeline
Embeddings vía nomic-embed-text en Ollama (la-fragua :11434, 768-d).
Todo local, cero telemetría: nada de esto llama a un servicio externo.

Doble uso:
1) funciones sueltas embed_text()/embed_batch() para to_qdrant.py
2) OllamaEmbeddings(chonkie.embeddings.base.BaseEmbeddings) para que chunk.py
   pueda usar el MISMO modelo local en el SemanticChunker, en vez de bajar
   un modelo HF nuevo (minishlab/potion-base-32M por defecto en Chonkie).
"""
from pathlib import Path

import numpy as np
import requests
import yaml

HW = yaml.safe_load(Path(__file__).with_name("hw.yaml").read_text())
_OLLAMA = HW["ollama_embed"]
_URL = f"http://{_OLLAMA['host']}:{_OLLAMA['port']}/api/embeddings"
_MODEL = _OLLAMA["model"]
DIMS = _OLLAMA["dims"]


def embed_text(text: str, prefix: str = "search_document: ") -> np.ndarray:
    """Embebe un string. Prefijo nomic: search_document: para chunks indexados,
    search_query: para consultas futuras (no usado en esta pasada)."""
    resp = requests.post(_URL, json={"model": _MODEL, "prompt": f"{prefix}{text}"}, timeout=60)
    resp.raise_for_status()
    vec = resp.json()["embedding"]
    if len(vec) != DIMS:
        raise ValueError(f"embedding de {len(vec)} dims, esperaba {DIMS} (revisar hw.yaml/modelo)")
    return np.array(vec, dtype=np.float32)


def embed_batch(texts: list[str], prefix: str = "search_document: ") -> list[np.ndarray]:
    return [embed_text(t, prefix) for t in texts]


try:
    from chonkie.embeddings.base import BaseEmbeddings

    class OllamaEmbeddings(BaseEmbeddings):
        """Wrapper local para que Chonkie use nomic-embed-text (Ollama) en vez
        de descargar un modelo HF adicional. Mantiene "todo local"."""

        def __init__(self) -> None:
            super().__init__()

        def embed(self, text: str) -> np.ndarray:
            return embed_text(text, prefix="")

        def embed_batch(self, texts: list[str]) -> list[np.ndarray]:
            return [self.embed(t) for t in texts]

        @property
        def dimension(self) -> int:
            return DIMS

        def get_tokenizer(self):
            # nomic-embed-text no expone su tokenizer vía Ollama; se usa el
            # WordTokenizer de Chonkie (aproximación por palabras) para las
            # ventanas del SemanticChunker. No es el tokenizer exacto del
            # modelo — STUB aceptable, se afina si hace falta con datos reales.
            from chonkie import WordTokenizer

            return WordTokenizer()

except ImportError:  # pragma: no cover
    OllamaEmbeddings = None
