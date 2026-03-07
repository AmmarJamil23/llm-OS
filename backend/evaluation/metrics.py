from __future__ import annotations


def recall_at_k(retrieved_texts: list[str], ground_truth: str, k: int = 5) -> float:
    """
    Recall@K: 1.0 if ground_truth appears (case-insensitive substring match)
    in the top-k retrieved chunks, else 0.0.
    """
    top_k = retrieved_texts[:k]
    gt_lower = ground_truth.lower()
    for text in top_k:
        if gt_lower in text.lower():
            return 1.0
    return 0.0


def mean_reciprocal_rank(retrieved_texts: list[str], ground_truth: str) -> float:
    """
    MRR: 1/rank of the first retrieved chunk that contains the ground truth.
    Returns 0.0 if not found.
    """
    gt_lower = ground_truth.lower()
    for rank, text in enumerate(retrieved_texts, start=1):
        if gt_lower in text.lower():
            return 1.0 / rank
    return 0.0


def compute_metrics(
    retrieved_texts: list[str],
    ground_truth: str,
    k: int = 5,
) -> dict[str, float]:
    """Return a dict of all computed metrics for a single query."""
    return {
        "recall_at_k": recall_at_k(retrieved_texts, ground_truth, k),
        "mrr": mean_reciprocal_rank(retrieved_texts, ground_truth),
    }
