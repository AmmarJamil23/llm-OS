from __future__ import annotations

from backend.core.models import Experiment


def compare_experiments(a: Experiment, b: Experiment) -> dict:
    """
    Compare two experiments and return a summary of their differences.

    Returns a dict with absolute and relative deltas for key metrics.
    """
    def delta(va: float, vb: float) -> dict:
        diff = round(vb - va, 4)
        pct = round((diff / va * 100) if va != 0 else 0.0, 2)
        return {"a": va, "b": vb, "delta": diff, "delta_pct": pct}

    return {
        "experiment_a": {"id": a.id, "name": a.config.name},
        "experiment_b": {"id": b.id, "name": b.config.name},
        "avg_recall": delta(a.avg_recall, b.avg_recall),
        "avg_mrr": delta(a.avg_mrr, b.avg_mrr),
        "avg_latency_ms": delta(a.avg_latency_ms, b.avg_latency_ms),
        "config_diff": {
            "embedding_model": {"a": a.config.embedding_model, "b": b.config.embedding_model},
            "chunk_size": {"a": a.config.chunk_size, "b": b.config.chunk_size},
            "retrieval_k": {"a": a.config.retrieval_k, "b": b.config.retrieval_k},
            "ollama_model": {"a": a.config.ollama_model, "b": b.config.ollama_model},
        },
    }
