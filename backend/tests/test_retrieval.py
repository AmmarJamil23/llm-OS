from __future__ import annotations

import numpy as np
import pytest

from backend.core.models import Chunk
from backend.retrieval.store import FAISSStore
from backend.ingestion.embedder import embed_texts


@pytest.fixture
def tmp_store(tmp_path):
    index_path = str(tmp_path / "test.index")
    return FAISSStore(index_path=index_path)


def _make_chunks(n: int) -> list[Chunk]:
    return [
        Chunk(doc_id="doc-1", text=f"Chunk number {i} with some content.", metadata={})
        for i in range(n)
    ]


def test_store_add_and_search(tmp_store):
    chunks = _make_chunks(5)
    texts = [c.text for c in chunks]
    embeddings = embed_texts(texts)

    tmp_store.add_chunks(chunks, embeddings)
    assert tmp_store.total_chunks == 5


def test_search_returns_top_k(tmp_store):
    chunks = _make_chunks(10)
    embeddings = embed_texts([c.text for c in chunks])
    tmp_store.add_chunks(chunks, embeddings)

    query_vec = embed_texts(["Chunk number 3"])[0]
    results = tmp_store.search(query_vec, k=3)

    assert len(results) == 3
    for chunk, score in results:
        assert isinstance(chunk, Chunk)
        assert isinstance(score, float)


def test_search_empty_store_returns_empty(tmp_store):
    query_vec = np.random.rand(384).astype(np.float32)
    results = tmp_store.search(query_vec, k=5)
    assert results == []


def test_store_persists_and_reloads(tmp_path):
    index_path = str(tmp_path / "persist.index")
    store1 = FAISSStore(index_path=index_path)
    chunks = _make_chunks(3)
    embeddings = embed_texts([c.text for c in chunks])
    store1.add_chunks(chunks, embeddings)

    store2 = FAISSStore(index_path=index_path)
    assert store2.total_chunks == 3
