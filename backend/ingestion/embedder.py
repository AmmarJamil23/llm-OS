from __future__ import annotations

import threading
from typing import Any

import numpy as np

from backend.core.config import settings
from backend.core.logging import get_logger

logger = get_logger(__name__)

_lock = threading.Lock()
_model: Any = None


def get_embedding_model():
    """Return the singleton SentenceTransformer instance, loading it on first call."""
    global _model
    if _model is None:
        with _lock:
            if _model is None:
                from sentence_transformers import SentenceTransformer
                logger.info("Loading embedding model: %s", settings.embedding_model)
                _model = SentenceTransformer(settings.embedding_model)
                logger.info("Embedding model loaded.")
    return _model


def embed_texts(texts: list[str]) -> np.ndarray:
    """Encode a list of texts into a 2-D float32 numpy array."""
    model = get_embedding_model()
    embeddings: np.ndarray = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=False,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )
    return embeddings.astype(np.float32)


def embed_query(query: str) -> np.ndarray:
    """Encode a single query string into a 1-D float32 numpy array."""
    return embed_texts([query])[0]
