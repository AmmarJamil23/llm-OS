from __future__ import annotations

import json
import tempfile

import pytest

from backend.evaluation.dataset import load_dataset
from backend.evaluation.metrics import recall_at_k, mean_reciprocal_rank, compute_metrics


# ---------------------------------------------------------------------------
# Metrics tests
# ---------------------------------------------------------------------------

def test_recall_at_k_found():
    retrieved = ["The capital of France is Paris.", "Another chunk."]
    assert recall_at_k(retrieved, "Paris", k=5) == 1.0


def test_recall_at_k_not_found():
    retrieved = ["Some unrelated text.", "More unrelated content."]
    assert recall_at_k(retrieved, "Paris", k=5) == 0.0


def test_recall_at_k_respects_k():
    retrieved = ["unrelated", "unrelated", "Paris is here", "unrelated"]
    assert recall_at_k(retrieved, "Paris", k=2) == 0.0
    assert recall_at_k(retrieved, "Paris", k=3) == 1.0


def test_mrr_first_rank():
    retrieved = ["Paris is the capital of France.", "Another chunk."]
    assert mean_reciprocal_rank(retrieved, "Paris") == 1.0


def test_mrr_second_rank():
    retrieved = ["Unrelated.", "Paris is here."]
    assert mean_reciprocal_rank(retrieved, "Paris") == pytest.approx(0.5)


def test_mrr_not_found():
    retrieved = ["Unrelated.", "Also unrelated."]
    assert mean_reciprocal_rank(retrieved, "Paris") == 0.0


def test_compute_metrics_returns_all_keys():
    result = compute_metrics(["Paris text"], "Paris", k=1)
    assert "recall_at_k" in result
    assert "mrr" in result


# ---------------------------------------------------------------------------
# Dataset loading tests
# ---------------------------------------------------------------------------

def test_load_json_dataset(tmp_path):
    data = [
        {"id": "1", "question": "What is AI?", "ground_truth": "Artificial Intelligence"},
        {"id": "2", "question": "What is ML?", "ground_truth": "Machine Learning"},
    ]
    p = tmp_path / "dataset.json"
    p.write_text(json.dumps(data), encoding="utf-8")

    items = load_dataset(str(p))
    assert len(items) == 2
    assert items[0].question == "What is AI?"


def test_load_csv_dataset(tmp_path):
    content = "id,question,ground_truth\n1,What is NLP?,Natural Language Processing\n"
    p = tmp_path / "dataset.csv"
    p.write_text(content, encoding="utf-8")

    items = load_dataset(str(p))
    assert len(items) == 1
    assert items[0].ground_truth == "Natural Language Processing"


def test_load_nonexistent_dataset():
    with pytest.raises(FileNotFoundError):
        load_dataset("/nonexistent/dataset.json")
