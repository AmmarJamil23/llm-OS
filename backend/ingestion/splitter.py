from __future__ import annotations

from backend.core.config import settings
from backend.core.models import Chunk, Document
from backend.core.logging import get_logger

logger = get_logger(__name__)


def split_document(doc: Document, chunk_size: int | None = None, chunk_overlap: int | None = None) -> list[Chunk]:
    """Split a Document into overlapping text chunks."""
    chunk_size = chunk_size or settings.chunk_size
    chunk_overlap = chunk_overlap or settings.chunk_overlap

    text = doc.content
    chunks: list[Chunk] = []
    start = 0
    index = 0

    while start < len(text):
        end = start + chunk_size
        chunk_text = text[start:end].strip()
        if chunk_text:
            chunks.append(
                Chunk(
                    doc_id=doc.id,
                    text=chunk_text,
                    metadata={**doc.metadata, "chunk_index": index, "source": doc.source},
                )
            )
            index += 1
        start += chunk_size - chunk_overlap

    logger.info(
        "Split doc_id=%s into %d chunks (size=%d overlap=%d)",
        doc.id, len(chunks), chunk_size, chunk_overlap,
    )
    return chunks
