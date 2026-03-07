from __future__ import annotations

import json
import pickle
import threading
from pathlib import Path
from typing import Any

import numpy as np

from backend.core.config import settings
from backend.core.models import Chunk
from backend.core.logging import get_logger

logger = get_logger(__name__)

_store_lock = threading.Lock()
_store_instance: FAISSStore | None = None


class FAISSStore:
    """
    In-process FAISS vector store.

    Stores float32 L2-normalised embeddings alongside Chunk metadata.
    Persists index + metadata to disk so state survives restarts.
    """

    def __init__(self, index_path: str | None = None):
        import faiss

        self._index_path = Path(index_path or settings.faiss_index_path)
        self._meta_path = self._index_path.with_suffix(".meta.pkl")
        self._index_path.parent.mkdir(parents=True, exist_ok=True)

        self._chunks: list[Chunk] = []
        self._dim: int | None = None
        self._index: Any = None  # faiss.Index

        if self._index_path.exists() and self._meta_path.exists():
            self._load(faiss)
        else:
            logger.info("No existing FAISS index found. Starting fresh.")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add_chunks(self, chunks: list[Chunk], embeddings: np.ndarray) -> None:
        """Add chunks with pre-computed embeddings to the index."""
        import faiss

        if embeddings.ndim != 2:
            raise ValueError("embeddings must be 2-D (n_chunks × dim)")

        n, dim = embeddings.shape

        if self._index is None:
            self._dim = dim
            self._index = faiss.IndexFlatIP(dim)   # inner-product on unit vectors == cosine
            logger.info("Created new FAISS IndexFlatIP dim=%d", dim)
        elif dim != self._dim:
            raise ValueError(f"Dimension mismatch: store={self._dim}, new={dim}")

        self._index.add(embeddings)
        self._chunks.extend(chunks)
        self._save()
        logger.info("Added %d vectors. Store total: %d", n, self._index.ntotal)

    def search(self, query_vec: np.ndarray, k: int = 5) -> list[tuple[Chunk, float]]:
        """Return top-k (Chunk, score) pairs ordered by descending similarity."""
        if self._index is None or self._index.ntotal == 0:
            return []

        query_vec = query_vec.reshape(1, -1).astype(np.float32)
        k = min(k, self._index.ntotal)
        scores, indices = self._index.search(query_vec, k)

        results: list[tuple[Chunk, float]] = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            results.append((self._chunks[idx], float(score)))
        return results

    @property
    def total_chunks(self) -> int:
        return len(self._chunks)

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def _save(self) -> None:
        import faiss

        faiss.write_index(self._index, str(self._index_path))
        with open(self._meta_path, "wb") as f:
            pickle.dump(self._chunks, f)
        logger.debug("FAISS index saved to %s", self._index_path)

    def _load(self, faiss) -> None:
        self._index = faiss.read_index(str(self._index_path))
        with open(self._meta_path, "rb") as f:
            self._chunks = pickle.load(f)
        self._dim = self._index.d
        logger.info(
            "Loaded FAISS index from %s (total=%d dim=%d)",
            self._index_path, self._index.ntotal, self._dim,
        )


def get_vector_store() -> FAISSStore:
    """Return the singleton FAISSStore instance."""
    global _store_instance
    if _store_instance is None:
        with _store_lock:
            if _store_instance is None:
                _store_instance = FAISSStore()
    return _store_instance
