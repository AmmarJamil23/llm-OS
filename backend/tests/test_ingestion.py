from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from backend.core.models import IngestRequest
from backend.ingestion.loader import load_document
from backend.ingestion.splitter import split_document
from backend.ingestion.embedder import embed_texts


def _write_temp_txt(content: str) -> str:
    tmp = tempfile.NamedTemporaryFile(suffix=".txt", mode="w", delete=False, encoding="utf-8")
    tmp.write(content)
    tmp.close()
    return tmp.name


def test_load_txt_document():
    path = _write_temp_txt("Hello world. This is a test document.")
    doc = load_document(path, "txt")
    assert doc.content == "Hello world. This is a test document."
    assert doc.metadata["doc_type"] == "txt"


def test_load_md_document():
    path = _write_temp_txt("# Title\n\nSome markdown content.")
    doc = load_document(path, "md")
    assert "markdown" in doc.content


def test_load_nonexistent_raises():
    with pytest.raises(FileNotFoundError):
        load_document("/nonexistent/file.txt", "txt")


def test_load_unsupported_type_raises():
    path = _write_temp_txt("content")
    with pytest.raises(ValueError):
        load_document(path, "docx")


def test_split_document_produces_chunks():
    path = _write_temp_txt("A" * 2000)
    doc = load_document(path, "txt")
    chunks = split_document(doc, chunk_size=500, chunk_overlap=50)
    assert len(chunks) > 1
    for chunk in chunks:
        assert chunk.doc_id == doc.id
        assert len(chunk.text) > 0


def test_split_preserves_doc_id():
    path = _write_temp_txt("Some content for splitting.")
    doc = load_document(path, "txt")
    chunks = split_document(doc, chunk_size=10, chunk_overlap=2)
    for chunk in chunks:
        assert chunk.doc_id == doc.id


def test_embed_texts_returns_correct_shape():
    texts = ["Hello world", "Another sentence", "Third text"]
    embeddings = embed_texts(texts)
    assert embeddings.ndim == 2
    assert embeddings.shape[0] == 3
    assert embeddings.shape[1] > 0
    assert embeddings.dtype.name == "float32"
