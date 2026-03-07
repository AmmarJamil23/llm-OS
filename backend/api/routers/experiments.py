from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.core.models import Experiment, ExperimentConfig, EvalResult
from backend.core.logging import get_logger
from backend.experiments.tracker import save_experiment, load_experiment, list_experiments
from backend.experiments.comparator import compare_experiments

logger = get_logger(__name__)
router = APIRouter()


class CreateExperimentRequest(BaseModel):
    config: ExperimentConfig
    results: list[EvalResult] = []


class CompareRequest(BaseModel):
    experiment_a_id: str
    experiment_b_id: str


@router.get("/experiments", response_model=list[Experiment], tags=["experiments"])
async def get_experiments() -> list[Experiment]:
    """List all persisted experiments."""
    return list_experiments()


@router.post("/experiments", response_model=Experiment, tags=["experiments"])
async def create_experiment(request: CreateExperimentRequest) -> Experiment:
    """Save a new experiment with optional pre-computed results."""
    return save_experiment(request.config, request.results)


@router.get("/experiments/{experiment_id}", response_model=Experiment, tags=["experiments"])
async def get_experiment(experiment_id: str) -> Experiment:
    """Get a single experiment by ID."""
    exp = load_experiment(experiment_id)
    if exp is None:
        raise HTTPException(status_code=404, detail=f"Experiment not found: {experiment_id}")
    return exp


@router.post("/experiments/compare", response_model=dict, tags=["experiments"])
async def compare(request: CompareRequest) -> dict:
    """Compare two experiments side by side."""
    a = load_experiment(request.experiment_a_id)
    b = load_experiment(request.experiment_b_id)
    if a is None:
        raise HTTPException(status_code=404, detail=f"Experiment A not found: {request.experiment_a_id}")
    if b is None:
        raise HTTPException(status_code=404, detail=f"Experiment B not found: {request.experiment_b_id}")
    return compare_experiments(a, b)
