from __future__ import annotations

import csv
import json
from pathlib import Path

from backend.core.models import EvalDatasetItem
from backend.core.logging import get_logger

logger = get_logger(__name__)


def load_dataset(path: str) -> list[EvalDatasetItem]:
    """
    Load an evaluation dataset from a JSON or CSV file.

    JSON format: list of {"id": ..., "question": ..., "ground_truth": ...}
    CSV format: header row with columns: id, question, ground_truth
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    suffix = p.suffix.lower()
    if suffix == ".json":
        items = _load_json(p)
    elif suffix == ".csv":
        items = _load_csv(p)
    else:
        raise ValueError(f"Unsupported dataset format: {suffix}. Use .json or .csv")

    logger.info("Loaded %d eval items from %s", len(items), path)
    return items


def _load_json(path: Path) -> list[EvalDatasetItem]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return [EvalDatasetItem(**item) for item in raw]


def _load_csv(path: Path) -> list[EvalDatasetItem]:
    items: list[EvalDatasetItem] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            items.append(
                EvalDatasetItem(
                    id=row.get("id", ""),
                    question=row["question"],
                    ground_truth=row["ground_truth"],
                )
            )
    return items
