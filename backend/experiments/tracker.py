from __future__ import annotations

import json
import uuid
from pathlib import Path

from backend.core.models import Experiment, ExperimentConfig, EvalResult
from backend.core.logging import get_logger

logger = get_logger(__name__)

_EXPERIMENTS_DIR = Path("data/experiments")


def _ensure_dir() -> None:
    _EXPERIMENTS_DIR.mkdir(parents=True, exist_ok=True)


def save_experiment(config: ExperimentConfig, results: list[EvalResult]) -> Experiment:
    """Persist an experiment with its results to disk and return the Experiment object."""
    _ensure_dir()

    avg_recall = sum(r.recall_at_k for r in results) / len(results) if results else 0.0
    avg_mrr = sum(r.mrr for r in results) / len(results) if results else 0.0
    avg_latency = sum(r.latency_ms for r in results) / len(results) if results else 0.0

    exp = Experiment(
        config=config,
        results=results,
        avg_recall=round(avg_recall, 4),
        avg_mrr=round(avg_mrr, 4),
        avg_latency_ms=round(avg_latency, 2),
    )

    path = _EXPERIMENTS_DIR / f"{exp.id}.json"
    path.write_text(exp.model_dump_json(indent=2), encoding="utf-8")
    logger.info("Saved experiment id=%s to %s", exp.id, path)
    return exp


def load_experiment(experiment_id: str) -> Experiment | None:
    """Load a single experiment by ID. Returns None if not found."""
    path = _EXPERIMENTS_DIR / f"{experiment_id}.json"
    if not path.exists():
        return None
    return Experiment.model_validate_json(path.read_text(encoding="utf-8"))


def list_experiments() -> list[Experiment]:
    """Return all persisted experiments ordered by file modification time (newest first)."""
    _ensure_dir()
    paths = sorted(_EXPERIMENTS_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    results: list[Experiment] = []
    for p in paths:
        try:
            results.append(Experiment.model_validate_json(p.read_text(encoding="utf-8")))
        except Exception as exc:
            logger.warning("Could not parse experiment file %s: %s", p, exc)
    return results
