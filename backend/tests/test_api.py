from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend.api.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"
    assert "ollama" in data


def test_ingest_file_not_found():
    response = client.post(
        "/api/ingest",
        json={"source": "/nonexistent/file.txt", "doc_type": "txt"},
    )
    assert response.status_code == 404


def test_ingest_txt_document(tmp_path):
    doc_file = tmp_path / "test.txt"
    doc_file.write_text("This is a test document with enough content to produce at least one chunk.")

    response = client.post(
        "/api/ingest",
        json={"source": str(doc_file), "doc_type": "txt"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "doc_id" in data
    assert data["chunk_count"] >= 1
    assert data["latency_ms"] > 0


def test_query_no_documents_returns_gracefully():
    # May return "no documents found" message rather than error
    response = client.post(
        "/api/query",
        json={"query": "What is the meaning of life?", "k": 3},
    )
    # Should not be 500
    assert response.status_code in (200, 502)


def test_ingest_then_query(tmp_path):
    doc_file = tmp_path / "knowledge.txt"
    doc_file.write_text(
        "The LLM Research OS is a local-first AI research platform. "
        "It supports semantic search, agent reasoning, and model evaluation."
    )

    # Ingest
    ingest_resp = client.post(
        "/api/ingest",
        json={"source": str(doc_file), "doc_type": "txt"},
    )
    assert ingest_resp.status_code == 200

    # Query (LLM may not be available in CI, so only check structure)
    query_resp = client.post(
        "/api/query",
        json={"query": "What is LLM Research OS?", "k": 3},
    )
    assert query_resp.status_code in (200, 502)
    if query_resp.status_code == 200:
        data = query_resp.json()
        assert "answer" in data
        assert "sources" in data
