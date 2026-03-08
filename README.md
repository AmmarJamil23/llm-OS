# LLM Research Operating System (llm-OS)

## Overview

LLM-OS is a production-grade, local-first AI research platform. It enables document ingestion, semantic search, multi-agent reasoning, experiment tracking, and evaluation—all through a REST API and a Next.js dashboard. Designed for technical excellence and business awareness, it is ideal for researchers, builders, and entrepreneurs.

---

## Project Structure & File Explanations

### Root

- `docker-compose.yml`: Orchestrates backend, frontend, and data volumes for local deployment.
- `Dockerfile.backend`: Builds the Python FastAPI backend container.
- `Dockerfile.frontend`: Builds the Next.js frontend container.
- `requirements.txt`: Python dependencies for backend and core modules.
- `README.md`: Project documentation and instructions.

### backend/

- `__init__.py`: Marks backend as a Python package.
- `agents/`: Implements agent orchestration (LangGraph workflows).
  - `graph.py`: Defines agent graphs and state transitions.
  - `nodes.py`: Implements agent nodes (planner, retriever, reasoner, evaluator).
  - `tools.py`: Defines agent tools (vector search, document processing).
- `api/`: FastAPI REST service.
  - `main.py`: Entry point for API server.
  - `routers/`: Modular API endpoints.
    - `agent.py`: Agent orchestration endpoints.
    - `eval.py`: Evaluation endpoints.
    - `experiments.py`: Experiment management endpoints.
    - `health.py`: Health check endpoint.
    - `ingest.py`: Document ingestion endpoints.
    - `query.py`: Semantic search endpoints.
- `core/`: Core utilities and configuration.
  - `config.py`: System configuration loader.
  - `llm.py`: LLM runtime integration (Ollama, etc).
  - `logging.py`: Logging setup.
  - `models.py`: Data models (Document, Chunk, QueryResult, EvalResult).
- `evaluation/`: Evaluation engine.
  - `dataset.py`: Loads and manages evaluation datasets.
  - `metrics.py`: Implements retrieval and generation metrics.
  - `runner.py`: Runs evaluation jobs.
- `experiments/`: Experiment runner and tracker.
  - `comparator.py`: Compares embeddings, prompts, retrieval strategies.
  - `tracker.py`: Tracks experiment results.
- `ingestion/`: Document ingestion pipeline.
  - `embedder.py`: Embedding model integration (Sentence Transformers).
  - `loader.py`: Document loader (PDF, MD, TXT).
  - `pipeline.py`: Orchestrates ingestion steps.
  - `splitter.py`: Text chunking logic.
- `retrieval/`: Vector search engine.
  - `search.py`: Semantic search logic.
  - `store.py`: Vector store abstraction (FAISS/Chroma).
- `tests/`: Backend unit and integration tests.
  - `test_api.py`: API endpoint tests.
  - `test_evaluation.py`: Evaluation engine tests.
  - `test_ingestion.py`: Ingestion pipeline tests.
  - `test_retrieval.py`: Retrieval engine tests.

### data/

- `documents/`: Raw and processed documents.
- `experiments/`: Experiment results and logs.
- `indices/`: Vector indices (FAISS/Chroma).

### docs/

- `plan.md`: Implementation plan, task breakdown, and business outcomes.
- `research.md`: System architecture, module responsibilities, and design analysis.

### frontend/

- Next.js dashboard for visualization and user interaction.
- `app/`: Main app pages.
  - `agent/page.tsx`: Agent orchestration UI.
  - `evaluation/page.tsx`: Evaluation dashboard.
  - `experiments/page.tsx`: Experiment management UI.
  - `query/page.tsx`: Semantic search UI.
- `components/`: Reusable UI components.
- `lib/api.ts`: API client for frontend-backend communication.
- `globals.css`, `layout.tsx`, etc.: Styling and layout.

---

## System Architecture

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

---

## How to Run the Project

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Ollama (for LLM runtime, install separately: https://ollama.com)

### 1. Clone the repository

```bash
git clone https://github.com/your-org/llm-OS.git
cd llm-OS
```

### 2. Build and start with Docker Compose

```bash
docker-compose up --build
```

This launches backend (FastAPI), frontend (Next.js), and mounts data volumes.

### 3. Access the dashboard

- Open http://localhost:3000 for the Next.js dashboard.
- Backend API runs at http://localhost:8000.

### 4. Ingest documents

- Use the dashboard or POST `/api/ingest` with a document source.

### 5. Run queries and experiments

- Use dashboard pages or API endpoints for semantic search, agent workflows, evaluation, and experiments.

---

## Common Pitfalls

- **Ollama not installed:** LLM runtime will fail. Install Ollama separately.
- **Python version mismatch:** Use Python 3.11+ for LangGraph compatibility.
- **Data not persisted:** Ensure `data/` is mounted as a Docker volume.
- **Cloud dependencies:** MVP is local-first; do not use OpenAI/Pinecone APIs.
- **Hardcoded values:** Use config files, not hardcoded parameters.
- **Duplicate logic:** Reuse modules, avoid redundant code.
- **Performance bottlenecks:** Optimize embedding and retrieval batch sizes.

---

## Product Perspective

- **User Problem Solved:** Makes LLM research observable, experimentable, and reproducible.
- **User Value:** Visualizes retrieval quality, agent reasoning, and experiment results.
- **Scalability:** Designed for local-first, but can be extended to cloud and multi-user.
- **Demonstrability:** Dashboard visualizes AI reasoning and performance metrics for portfolio, investors, and users.

---

## Entrepreneurial Perspective

- **Unique Capabilities:** Not just a chatbot—enables deep research, experiment tracking, and evaluation.
- **Business Value:** Useful for companies building RAG, agent, or evaluation pipelines.
- **Potential SaaS:** Can be extended to multi-user, cloud, and enterprise features.
- **Customer Segments:** AI researchers, ML engineers, product teams, technical founders.
- **Sales Messaging:** Solves the pain of invisible retrieval and agent reasoning; makes AI workflows transparent and measurable.

---

## Persistent Documentation

- `docs/research.md`: System architecture, module analysis, and design patterns.
- `docs/plan.md`: Implementation plan, task breakdown, and business outcomes.

---

## Contributing

Follow the engineering workflow in `.github/copilot-instructions.md`:

1. Research the codebase and write findings in `docs/research.md`.
2. Create a detailed plan in `docs/plan.md`.
3. Refine plan through annotation cycles.
4. Implement tasks and mark progress in `plan.md`.
5. Verify code, fix errors, and optimize architecture.

---

## License

MIT License

uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload