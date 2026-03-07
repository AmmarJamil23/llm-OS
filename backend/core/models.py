from __future__ import annotations

from pydantic import BaseModel, Field
import uuid


def _new_id() -> str:
    return str(uuid.uuid4())


# ---------------------------------------------------------------------------
# Storage models
# ---------------------------------------------------------------------------

class Document(BaseModel):
    id: str = Field(default_factory=_new_id)
    source: str
    content: str
    metadata: dict = Field(default_factory=dict)


class Chunk(BaseModel):
    id: str = Field(default_factory=_new_id)
    doc_id: str
    text: str
    metadata: dict = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Request / response models
# ---------------------------------------------------------------------------

class IngestRequest(BaseModel):
    source: str        # local file path
    doc_type: str      # "pdf" | "txt" | "md"


class IngestResponse(BaseModel):
    doc_id: str
    chunk_count: int
    latency_ms: float


class QueryRequest(BaseModel):
    query: str
    k: int = 5


class QueryResult(BaseModel):
    query: str
    answer: str
    sources: list[dict]
    latency_ms: float


class AgentRequest(BaseModel):
    task: str


class AgentResponse(BaseModel):
    result: str
    trace: list[dict]
    latency_ms: float


# ---------------------------------------------------------------------------
# Evaluation models
# ---------------------------------------------------------------------------

class EvalDatasetItem(BaseModel):
    id: str = Field(default_factory=_new_id)
    question: str
    ground_truth: str


class EvalResult(BaseModel):
    question: str
    answer: str
    ground_truth: str
    recall_at_k: float
    mrr: float
    latency_ms: float


# ---------------------------------------------------------------------------
# Experiment models
# ---------------------------------------------------------------------------

class ExperimentConfig(BaseModel):
    name: str
    embedding_model: str
    chunk_size: int
    chunk_overlap: int
    retrieval_k: int
    ollama_model: str
    notes: str = ""


class Experiment(BaseModel):
    id: str = Field(default_factory=_new_id)
    config: ExperimentConfig
    results: list[EvalResult] = Field(default_factory=list)
    avg_recall: float = 0.0
    avg_mrr: float = 0.0
    avg_latency_ms: float = 0.0
