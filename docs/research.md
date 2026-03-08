# Research: LLM Research Operating System

**Date:** March 7, 2026  
**Status:** Initial — greenfield project

---

## 1. System Overview

This is a **greenfield project**. The workspace contains only the workflow protocol file (`.github/copilot-instructions.md`). There is no existing codebase to analyze — all architectural decisions will be made from first principles, guided by the project vision defined in the protocol.

The goal is to build an **LLM Research Operating System**: a local-first, production-grade AI research platform that allows users to ingest technical knowledge, perform semantic search, run multi-agent reasoning, evaluate model performance, and visualize results.

---

## 2. Domain Analysis

### 2.1 Core User Needs

- Ingest documents (PDFs, text, markdown) into a searchable knowledge base
- Query the knowledge base with natural language
- Run reasoning workflows with LLM agents over retrieved content
- Compare embedding models, prompts, and retrieval strategies
- Visualize retrieval quality and agent reasoning traces
- Track experiment results and model evaluations

### 2.2 Problem Space

Standard RAG (Retrieval Augmented Generation) pipelines are poorly observable. Users cannot see why a retrieval failed, why one embedding model outperforms another, or how agent reasoning degrades across prompts. This system makes those internals visible and experimentable.

---

## 3. Architecture Analysis

### 3.1 Layered Architecture (from protocol)

```
User Interface (Next.js Dashboard)
         ↓
REST API Gateway (FastAPI)
         ↓
Agent Orchestration Layer (LangGraph)
         ↓
Tool Layer
  ├── Vector Search (FAISS / Chroma)
  ├── Document Processing (chunking, embeddings)
  ├── Experiment Runner
  └── Evaluation Engine
         ↓
Vector Database (FAISS or Chroma)
         ↓
LLM Model Runtime (Ollama + Llama/Mistral)
         ↓
Response and Metrics
```

### 3.2 Module Responsibilities

| Module         | Responsibility                                 |
| -------------- | ---------------------------------------------- |
| `ingestion/`   | Load docs → chunk → embed → store vectors      |
| `retrieval/`   | Semantic search over vector store              |
| `agents/`      | LangGraph reasoning workflows                  |
| `evaluation/`  | Benchmark retrieval and generation quality     |
| `experiments/` | Compare strategies, embeddings, prompts        |
| `api/`         | FastAPI service exposing all capabilities      |
| `frontend/`    | Next.js dashboard for visualization            |
| `infra/`       | Docker Compose for full-stack local deployment |

---

## 4. Technology Stack Assessment

### 4.1 Backend — Python

| Technology            | Purpose                | Rationale                              |
| --------------------- | ---------------------- | -------------------------------------- |
| FastAPI               | REST API gateway       | Async, performant, auto-generated docs |
| LangGraph             | Agent orchestration    | Stateful graph-based agent workflows   |
| LangChain             | LLM tooling and chains | Broad ecosystem, document loaders      |
| FAISS                 | Vector search          | Fast in-process approximate NN search  |
| Chroma                | Alternate vector DB    | Persistent, easy metadata filtering    |
| Sentence Transformers | Embeddings             | Local, no API key required             |
| PyTorch               | ML runtime             | Required by Sentence Transformers      |
| Ollama                | LLM runtime            | Serve Llama/Mistral locally            |
| Pandas / NumPy        | Data manipulation      | Metrics, evaluation results            |

### 4.2 Frontend

| Technology    | Purpose       |
| ------------- | ------------- |
| Next.js       | Dashboard UI  |
| TailwindCSS   | Styling       |
| Recharts / D3 | Visualization |

### 4.3 Infrastructure

| Technology     | Purpose                     |
| -------------- | --------------------------- |
| Docker         | Container runtime           |
| Docker Compose | Multi-service orchestration |

---

## 5. Data Flow Analysis

### 5.1 Ingestion Flow

```
Raw Document (PDF/MD/TXT)
    → DocumentLoader (LangChain)
    → TextSplitter (chunk)
    → EmbeddingModel (Sentence Transformers)
    → VectorStore (FAISS/Chroma)
    → Metadata Store (JSON/SQLite)
```

### 5.2 Query / Retrieval Flow

```
User Query (string)
    → EmbeddingModel (same model as ingestion)
    → VectorStore.similarity_search(k=N)
    → Retrieved Chunks (with scores)
    → LLM Context Assembly
    → Ollama LLM
    → Response + Source Attribution
```

### 5.3 Agent Flow (LangGraph)

```
User Task
    → LangGraph StateGraph
    → Planner Node (decompose task)
    → Retriever Node (vector search tool)
    → Reasoner Node (LLM synthesis)
    → Evaluator Node (check answer quality)
    → Final Response
```

### 5.4 Evaluation Flow

```
Evaluation Dataset (questions + ground truth)
    → Retrieval (for each question)
    → LLM Answer Generation
    → Metrics Computation (Recall@K, MRR, BLEU, BERTScore)
    → Results DataFrame
    → API → Dashboard
```

---

## 6. Key Interfaces and Contracts

### 6.1 API Contracts (planned)

```
POST /api/ingest         → { source: string, type: string } → { doc_id, chunk_count }
POST /api/query          → { query: string, k: int }        → { answer, sources, latency }
POST /api/agent/run      → { task: string, config: object } → { result, trace }
POST /api/eval/run       → { dataset_id: string }           → { job_id }
GET  /api/eval/results   → { job_id }                       → { metrics }
GET  /api/experiments    →                                  → { list of experiments }
POST /api/experiments    → { config: object }               → { experiment_id }
```

### 6.2 Core Data Models

```python
class Document:
    id: str
    source: str
    content: str
    metadata: dict

class Chunk:
    id: str
    doc_id: str
    text: str
    embedding: list[float]
    metadata: dict

class QueryResult:
    query: str
    answer: str
    sources: list[Chunk]
    latency_ms: float

class EvalResult:
    question: str
    answer: str
    ground_truth: str
    recall_at_k: float
    mrr: float
```

---

## 7. Design Patterns to Follow

- **Repository pattern** for vector store abstraction (FAISS and Chroma swappable)
- **Strategy pattern** for embedding models (swap between providers)
- **Pipeline pattern** for ingestion (each step is a composable function)
- **Command pattern** for agent tools (each tool is a callable with schema)
- **Configuration-driven** design (no hardcoded values; use `config.yaml` / `.env`)

---

## 8. Constraints and Assumptions

1. **Local-first**: All components run without internet/API keys by default (Ollama + local embeddings)
2. **No cloud dependencies** in MVP: no OpenAI, no Pinecone, no managed services
3. **Python 3.11+** required (LangGraph API)
4. **Ollama must be installed separately** by the user — it is not bundled in Docker Compose
5. **Data persistence**: vector indices stored in `data/` directory, mounted as Docker volume
6. **Single-user system** in MVP: no auth, no multi-tenancy

---

## 9. Risks and Edge Cases

| Risk                                        | Mitigation                                                   |
| ------------------------------------------- | ------------------------------------------------------------ |
| Ollama not running when API starts          | Health check endpoint; clear error messages                  |
| Embedding model mismatch (ingest vs query)  | Store model name in vector index metadata; validate on query |
| Large document causing OOM during ingestion | Streaming chunker; configurable chunk size                   |
| Vector index corruption                     | Atomic writes; periodic snapshots                            |
| LangGraph version breaking changes          | Pin exact versions in requirements.txt                       |
| Frontend/backend CORS issues in dev         | Configure CORS middleware in FastAPI                         |

---

## 10. Observations and Recommendations

1. **Start with a working backend MVP** before building the frontend — validate the core RAG loop first.
2. **FAISS first, Chroma second** — FAISS is simpler in-process; add Chroma as a configurable alternative.
3. **One embedding model first** — `all-MiniLM-L6-v2` from Sentence Transformers is fast and good enough for MVP.
4. **LangGraph for agents** — even a simple 2-node graph (retrieve + answer) demonstrates the pattern.
5. **Docker Compose** should wire together: `api`, `frontend`, and (optionally) a vector store service.
6. **Evaluation engine** is a strong differentiator — prioritize it over fancy UI.

---

## 11. Project Structure (Proposed)

```
llm-OS/
├── .github/
│   └── copilot-instructions.md
├── docs/
│   ├── research.md          ← this file
│   └── plan.md
├── backend/
│   ├── ingestion/
│   ├── retrieval/
│   ├── agents/
│   ├── evaluation/
│   ├── experiments/
│   ├── api/
│   ├── core/                ← shared config, models, utils
│   └── tests/
├── frontend/
│   └── (Next.js app)
├── data/
│   ├── documents/
│   └── indices/
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
└── README.md
```
