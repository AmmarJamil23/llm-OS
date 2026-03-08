# Implementation Plan: LLM Research Operating System

**Date:** March 7, 2026  
**Status:** APPROVED — implementation in progress

---

## 1. Feature Description and Business Outcome

**What we're building:** A local-first AI research platform where users can ingest documents, run semantic search, invoke LLM agents, run evaluations, and manage experiments — all through a REST API and a visual dashboard.

**Business outcome:**

- Demonstrates production-grade ML engineering skills (portfolio value)
- Solves a real problem: RAG pipelines are opaque; this makes them transparent and experimental
- Can be positioned as a SaaS product for research teams, enterprises, and ML practitioners

---

## 2. Architecture Approach

Follow a **layered backend-first strategy**:

1. Solid Python backend with clean module boundaries
2. FastAPI REST gateway with auto-generated docs
3. LangGraph agent layer on top of the retrieval layer
4. Evaluation and experiment modules as independent services wired to the API
5. Next.js frontend consuming the API
6. Docker Compose tying everything together

Each layer is independently testable. No layer knows about presentation concerns.

---

## 3. Step-by-Step Implementation Strategy

### Phase 1 — Project Scaffold and Core Infrastructure

Set up directory structure, dependency management, Docker, and shared config/models.

### Phase 2 — Document Ingestion Pipeline

Load → chunk → embed → store. Foundation for everything else.

### Phase 3 — Vector Retrieval Engine

Query vectors, return ranked chunks with scores.

### Phase 4 — LLM Integration (Ollama)

Connect to local Ollama runtime, generate answers from retrieved context.

### Phase 5 — FastAPI Gateway

Expose ingestion, query, and agent endpoints. Validate inputs. Handle errors.

### Phase 6 — LangGraph Agent

Build a graph-based agent: planner → retriever → synthesizer.

### Phase 7 — Evaluation Engine

Accept evaluation datasets, compute Recall@K, MRR, latency.

### Phase 8 — Experiment Runner

Track experiment configs and results. Compare strategies.

### Phase 9 — Next.js Frontend

Dashboard for search, agent interaction, evaluation results, experiment comparison.

### Phase 10 — Docker Compose

Wire all services. Persistent volumes for data.

---

## 4. Files to Be Created

```
backend/
  core/
    config.py           ← Pydantic settings from .env / config.yaml
    models.py           ← Shared data models (Document, Chunk, QueryResult, etc.)
    logging.py          ← Structured logging setup
  ingestion/
    __init__.py
    loader.py           ← Document loading (PDF, TXT, MD)
    splitter.py         ← Text chunking strategies
    embedder.py         ← Sentence Transformer embedding wrapper
    pipeline.py         ← Orchestrates load → chunk → embed → store
  retrieval/
    __init__.py
    store.py            ← VectorStore abstraction (FAISS implementation)
    search.py           ← similarity_search with scores and metadata
  agents/
    __init__.py
    graph.py            ← LangGraph StateGraph definition
    nodes.py            ← Individual graph nodes (retrieve, reason, evaluate)
    tools.py            ← Tool definitions callable by agent
  evaluation/
    __init__.py
    dataset.py          ← Load evaluation datasets (JSON/CSV)
    metrics.py          ← Recall@K, MRR, latency
    runner.py           ← Orchestrate evaluation runs
  experiments/
    __init__.py
    tracker.py          ← Log experiment configs and results
    comparator.py       ← Compare two experiment results
  api/
    __init__.py
    main.py             ← FastAPI app entry point
    routers/
      ingest.py         ← POST /api/ingest
      query.py          ← POST /api/query
      agent.py          ← POST /api/agent/run
      eval.py           ← POST /api/eval/run, GET /api/eval/results
      experiments.py    ← GET/POST /api/experiments
      health.py         ← GET /health
  tests/
    test_ingestion.py
    test_retrieval.py
    test_agents.py
    test_evaluation.py
    test_api.py

frontend/
  (Next.js app — scaffolded with create-next-app)

data/
  documents/            ← Raw uploaded files
  indices/              ← FAISS index files
  experiments/          ← Experiment result JSON files

docker-compose.yml
Dockerfile.backend
Dockerfile.frontend
.env.example
requirements.txt
README.md
```

---

## 5. Core Data Models

```python
# backend/core/models.py

class Document(BaseModel):
    id: str
    source: str
    content: str
    metadata: dict = {}

class Chunk(BaseModel):
    id: str
    doc_id: str
    text: str
    metadata: dict = {}

class QueryRequest(BaseModel):
    query: str
    k: int = 5

class QueryResult(BaseModel):
    query: str
    answer: str
    sources: list[dict]
    latency_ms: float

class IngestRequest(BaseModel):
    source: str          # filepath or URL
    doc_type: str        # "pdf", "txt", "md"

class IngestResponse(BaseModel):
    doc_id: str
    chunk_count: int
    latency_ms: float

class EvalDatasetItem(BaseModel):
    id: str
    question: str
    ground_truth: str

class EvalResult(BaseModel):
    question: str
    answer: str
    ground_truth: str
    recall_at_k: float
    mrr: float
    latency_ms: float
```

---

## 6. API Contracts

| Method | Path                         | Request Body            | Response            |
| ------ | ---------------------------- | ----------------------- | ------------------- |
| POST   | `/api/ingest`                | `IngestRequest`         | `IngestResponse`    |
| POST   | `/api/query`                 | `QueryRequest`          | `QueryResult`       |
| POST   | `/api/agent/run`             | `{ task: str }`         | `{ result, trace }` |
| POST   | `/api/eval/run`              | `{ dataset_path: str }` | `{ job_id }`        |
| GET    | `/api/eval/results/{job_id}` | —                       | `list[EvalResult]`  |
| GET    | `/api/experiments`           | —                       | `list[Experiment]`  |
| POST   | `/api/experiments`           | `{ config }`            | `{ experiment_id }` |
| GET    | `/health`                    | —                       | `{ status: "ok" }`  |

---

## 7. Dependency Specification

```txt
# requirements.txt (key packages)
fastapi>=0.110.0
uvicorn[standard]>=0.27.0
pydantic>=2.0
pydantic-settings>=2.0
langchain>=0.2.0
langchain-community>=0.2.0
langgraph>=0.1.0
sentence-transformers>=2.6.0
faiss-cpu>=1.7.4
PyPDF2>=3.0.0
python-multipart>=0.0.9
httpx>=0.27.0
pandas>=2.0.0
numpy>=1.26.0
pytest>=8.0.0
python-dotenv>=1.0.0
```

---

## 8. Configuration Design

```python
# backend/core/config.py
class Settings(BaseSettings):
    # LLM
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5:3b-instruct"

    # Embeddings
    embedding_model: str = "all-MiniLM-L6-v2"

    # Vector store
    vector_store_type: str = "faiss"       # or "chroma"
    faiss_index_path: str = "data/indices/main.index"

    # Ingestion
    chunk_size: int = 500
    chunk_overlap: int = 50

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: list[str] = ["http://localhost:3000"]

    model_config = SettingsConfigDict(env_file=".env")
```

---

## 9. Testing Strategy

| Test               | Method                                                           |
| ------------------ | ---------------------------------------------------------------- |
| Ingestion pipeline | `pytest`: assert chunk count > 0, embeddings shape correct       |
| Retrieval          | `pytest`: query returns k results with scores                    |
| API endpoints      | `pytest` + `TestClient`: assert status codes and response shapes |
| Agent graph        | `pytest`: assert graph produces a result dict with `answer` key  |
| Evaluation metrics | `pytest`: assert Recall@1=1.0 for trivial dataset                |
| End-to-end         | Manual: curl/Postman against running server                      |

---

## 10. Performance Considerations

- Embedding generation is the slowest step — batch chunks before encoding
- FAISS `IndexFlatL2` is fine for MVP (<100K vectors); upgrade to `IndexIVFFlat` if needed
- Ollama inference latency depends on hardware — expose `latency_ms` in all API responses
- Async FastAPI endpoints for I/O-bound operations (file reads, Ollama HTTP calls)
- Lazy-load embedding model at startup (not per-request)

---

## 11. Tradeoffs and Alternatives

| Decision        | Chosen                | Alternative       | Reason                           |
| --------------- | --------------------- | ----------------- | -------------------------------- |
| Vector DB       | FAISS                 | Chroma            | FAISS is in-process, zero config |
| LLM runtime     | Ollama                | OpenAI API        | Local, no cost, no key required  |
| Embeddings      | Sentence Transformers | OpenAI embeddings | Local, reproducible              |
| Agent framework | LangGraph             | CrewAI            | More control, graph is explicit  |
| API framework   | FastAPI               | Flask             | Async, Pydantic, auto-docs       |

---

## 12. Implementation Tasks

> Developer: review and annotate this section before approving implementation.

### Phase 1 — Project Scaffold

- [x] Create directory structure
- [x] Create `requirements.txt`
- [x] Create `.env.example`
- [x] Create `backend/core/config.py`
- [x] Create `backend/core/models.py`
- [x] Create `backend/core/logging.py`

### Phase 2 — Ingestion Pipeline

- [x] `backend/ingestion/loader.py` — PDF, TXT, MD loaders
- [x] `backend/ingestion/splitter.py` — RecursiveCharacterTextSplitter wrapper
- [x] `backend/ingestion/embedder.py` — Sentence Transformer wrapper (singleton)
- [x] `backend/ingestion/pipeline.py` — Orchestrates the full ingestion flow
- [x] `backend/tests/test_ingestion.py`

### Phase 3 — Retrieval Engine

- [x] `backend/retrieval/store.py` — FAISS store abstraction
- [x] `backend/retrieval/search.py` — similarity_search returning ranked chunks
- [x] `backend/tests/test_retrieval.py`

### Phase 4 — LLM Integration

- [x] `backend/core/llm.py` — Ollama client wrapper (async HTTP)
- [x] Test Ollama reachability in health check

### Phase 5 — FastAPI Gateway

- [x] `backend/api/main.py` — App, CORS, lifespan
- [x] `backend/api/routers/health.py`
- [x] `backend/api/routers/ingest.py`
- [x] `backend/api/routers/query.py`
- [x] `backend/tests/test_api.py`

### Phase 6 — LangGraph Agent

- [x] `backend/agents/tools.py` — retrieval tool definition
- [x] `backend/agents/nodes.py` — retrieve, reason nodes
- [x] `backend/agents/graph.py` — StateGraph wiring
- [x] `backend/api/routers/agent.py`
- [x] `backend/tests/test_agents.py`

### Phase 7 — Evaluation Engine

- [x] `backend/evaluation/dataset.py`
- [x] `backend/evaluation/metrics.py`
- [x] `backend/evaluation/runner.py`
- [x] `backend/api/routers/eval.py`
- [x] `backend/tests/test_evaluation.py`

### Phase 8 — Experiment Runner

- [x] `backend/experiments/tracker.py`
- [x] `backend/experiments/comparator.py`
- [x] `backend/api/routers/experiments.py`

### Phase 9 — Frontend

- [x] Scaffold Next.js app in `frontend/`
- [x] Search page (query input + results)
- [x] Agent page (task input + reasoning trace)
- [x] Evaluation results page (metrics table + charts)
- [x] Experiment comparison page

### Phase 10 — Docker

- [x] `Dockerfile.backend`
- [x] `Dockerfile.frontend`
- [x] `docker-compose.yml`
- [x] `README.md` with setup instructions

---

## 13. Developer Notes Section

> Add your annotations, corrections, or approvals below this line.
> Copilot will read this section and update the plan accordingly.

## **[Annotation acknowledged]** LLM model set to `qwen2.5:3b-instruct` via Ollama. Updated in Section 8 (Configuration Design). All other plan items approved as-is.
