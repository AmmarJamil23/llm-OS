from __future__ import annotations

import time
import uuid

from backend.core.models import EvalDatasetItem, EvalResult
from backend.core.logging import get_logger
from backend.core import llm
from backend.retrieval.search import similarity_search
from backend.evaluation.metrics import compute_metrics

logger = get_logger(__name__)

# In-memory job store: job_id → list[EvalResult]
_jobs: dict[str, list[EvalResult]] = {}


def get_job_results(job_id: str) -> list[EvalResult] | None:
    return _jobs.get(job_id)


async def run_evaluation(
    dataset: list[EvalDatasetItem],
    k: int = 5,
) -> str:
    """
    Run evaluation over a dataset asynchronously.
    Returns a job_id that can be used to fetch results.
    """
    job_id = str(uuid.uuid4())
    results: list[EvalResult] = []

    logger.info("Starting eval job=%s items=%d", job_id, len(dataset))

    for item in dataset:
        t0 = time.perf_counter()

        sources = similarity_search(item.question, k=k)
        retrieved_texts = [s["text"] for s in sources]

        prompt = llm.build_rag_prompt(item.question, sources) if sources else (
            f"{item.question}\n\nAnswer:"
        )
        answer = await llm.generate(prompt)

        metrics = compute_metrics(retrieved_texts, item.ground_truth, k=k)
        latency_ms = (time.perf_counter() - t0) * 1000

        results.append(
            EvalResult(
                question=item.question,
                answer=answer,
                ground_truth=item.ground_truth,
                recall_at_k=metrics["recall_at_k"],
                mrr=metrics["mrr"],
                latency_ms=round(latency_ms, 2),
            )
        )

    _jobs[job_id] = results
    logger.info(
        "Eval job=%s complete. avg_recall=%.3f avg_mrr=%.3f",
        job_id,
        sum(r.recall_at_k for r in results) / len(results) if results else 0,
        sum(r.mrr for r in results) / len(results) if results else 0,
    )
    return job_id
