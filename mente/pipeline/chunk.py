"""
chunk.py — P0X mente/pipeline
Chunking semántico con Chonkie (SemanticChunker) usando el wrapper local de
nomic-embed-text (embed.OllamaEmbeddings) para no bajar un modelo HF nuevo.

STUB DE TAMAÑOS: los valores de threshold/chunk_size/min_sentences_per_chunk
de abajo son un punto de partida razonable, NO una regla derivada. Se afinan
cuando exista corpus real con el que medir recall/precision de retrieval —
mismo patrón que los stubs NotImplementedError de registro_tecnicas/models.py.
"""
from dataclasses import dataclass

from chonkie import SemanticChunker

from embed import OllamaEmbeddings

# --- STUB: se afina con datos reales del corpus, no se decreta hoy ---
STUB_THRESHOLD = 0.7
STUB_CHUNK_SIZE = 512
STUB_MIN_SENTENCES_PER_CHUNK = 2
# ----------------------------------------------------------------------

_chunker: SemanticChunker | None = None


def _get_chunker() -> SemanticChunker:
    global _chunker
    if _chunker is None:
        _chunker = SemanticChunker(
            embedding_model=OllamaEmbeddings(),
            threshold=STUB_THRESHOLD,
            chunk_size=STUB_CHUNK_SIZE,
            min_sentences_per_chunk=STUB_MIN_SENTENCES_PER_CHUNK,
        )
    return _chunker


@dataclass
class TextChunk:
    index: int
    text: str


def chunk_markdown(text: str) -> list[TextChunk]:
    """Divide un .md (ya sin el bloque de front-matter) en chunks semánticos."""
    if not text.strip():
        return []
    chunks = _get_chunker().chunk(text)
    return [TextChunk(index=i, text=c.text) for i, c in enumerate(chunks)]
