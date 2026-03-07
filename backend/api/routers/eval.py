from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.core.models import EvalResult
from backend.core.logging import get_logger
from backend.evaluation.dataset import load_dataset
from backend.evaluation.runner import run_evaluation, get_job_results

logger = get_logger(__name__)
router = APIRouter()


class EvalRunRequest(BaseModel):
    dataset_path: str
    k: int = 5


class EvalRunResponse(BaseModel):
    job_id: str


@router.post("/eval/run", response_model=EvalRunResponse, tags=["evaluation"])
async def start_evaluation(request: EvalRunRequest) -> EvalRunResponse:
    """Start an evaluation run over a dataset file."""
    try:
        dataset = load_dataset(request.dataset_path)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    if not dataset:
        raise HTTPException(status_code=422, detail="Dataset is empty.")

    job_id = await run_evaluation(dataset, k=request.k)
    return EvalRunResponse(job_id=job_id)


@router.get("/eval/results/{job_id}", response_model=list[EvalResult], tags=["evaluation"])
async def get_eval_results(job_id: str) -> list[EvalResult]:
    """Retrieve results for a completed evaluation job."""
    results = get_job_results(job_id)
    if results is None:
        raise HTTPException(status_code=404, detail=f"Job not found: {job_id}")
    return results
