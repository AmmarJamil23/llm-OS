from __future__ import annotations

import time

from backend.core.models import Chunk
from backend.core.logging import get_logger
from backend.ingestion.embedder import embed_query
from backend.retrieval.store import FAISSStore, get_vector_store

logger = get_logger(__name__)


def similarity_search(
    query: str,
    k: int = 5,
    store: FAISSStore | None = None,
) -> list[dict]:
    """
    Embed *query* and return the top-k most similar chunks.

    Returns a list of dicts:
        {
            "text": str,
            "score": float,
            "metadata": dict,
            "chunk_id": str,
            "doc_id": str,
        }
    """
    t0 = time.perf_counter()
    store = store or get_vector_store()

    query_vec = embed_query(query)
    raw: list[tuple[Chunk, float]] = store.search(query_vec, k=k)

    results = [
        {
            "text": chunk.text,
            "score": round(score, 4),
            "metadata": chunk.metadata,
            "chunk_id": chunk.id,
            "doc_id": chunk.doc_id,
        }
        for chunk, score in raw
    ]

    latency_ms = (time.perf_counter() - t0) * 1000
    logger.info(
        "Search query='%s...' k=%d hits=%d latency=%.1fms",
        query[:60], k, len(results), latency_ms,
    )
    return results
