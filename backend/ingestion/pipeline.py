from __future__ import annotations

import time

from backend.core.models import Chunk, Document, IngestRequest, IngestResponse
from backend.core.logging import get_logger
from backend.ingestion.loader import load_document
from backend.ingestion.splitter import split_document
from backend.ingestion.embedder import embed_texts

logger = get_logger(__name__)


def run_ingestion(request: IngestRequest, vector_store) -> IngestResponse:
    """
    Full ingestion pipeline: load → chunk → embed → store.

    Parameters
    ----------
    request:
        IngestRequest specifying source path and doc_type.
    vector_store:
        An instance of backend.retrieval.store.FAISSStore (or compatible).

    Returns
    -------
    IngestResponse with doc_id, chunk_count, and wall-clock latency.
    """
    t0 = time.perf_counter()

    doc: Document = load_document(request.source, request.doc_type)
    chunks: list[Chunk] = split_document(doc)

    if not chunks:
        raise ValueError(f"Document produced no chunks: {request.source}")

    texts = [c.text for c in chunks]
    embeddings = embed_texts(texts)

    vector_store.add_chunks(chunks, embeddings)

    latency_ms = (time.perf_counter() - t0) * 1000
    logger.info(
        "Ingestion complete doc_id=%s chunks=%d latency=%.1fms",
        doc.id, len(chunks), latency_ms,
    )

    return IngestResponse(
        doc_id=doc.id,
        chunk_count=len(chunks),
        latency_ms=round(latency_ms, 2),
    )
