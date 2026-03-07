from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.core.config import settings
from backend.core.logging import get_logger
from backend.ingestion.embedder import get_embedding_model
from backend.retrieval.store import get_vector_store

from backend.api.routers import health, ingest, query, agent, eval, experiments

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up LLM-OS API...")
    get_embedding_model()   # warm up embedding model
    get_vector_store()      # load or create FAISS index
    logger.info("Startup complete.")
    yield
    logger.info("Shutting down LLM-OS API.")


app = FastAPI(
    title="LLM Research OS",
    description="Local-first AI research platform: ingest documents, run semantic search, and invoke LLM agents.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(ingest.router, prefix="/api")
app.include_router(query.router, prefix="/api")
app.include_router(agent.router, prefix="/api")
app.include_router(eval.router, prefix="/api")
app.include_router(experiments.router, prefix="/api")
