from __future__ import annotations

import time

from fastapi import APIRouter, HTTPException

from backend.core.models import QueryRequest, QueryResult
from backend.core.logging import get_logger
from backend.core import llm
from backend.retrieval.search import similarity_search

logger = get_logger(__name__)
router = APIRouter()


@router.post("/query", response_model=QueryResult, tags=["query"])
async def query_documents(request: QueryRequest) -> QueryResult:
    """Retrieve relevant chunks then answer with the LLM."""
    t0 = time.perf_counter()

    try:
        sources = similarity_search(request.query, k=request.k)
    except Exception as exc:
        logger.exception("Retrieval failed: %s", exc)
        raise HTTPException(status_code=500, detail="Retrieval failed.")

    if not sources:
        return QueryResult(
            query=request.query,
            answer="No relevant documents found in the knowledge base.",
            sources=[],
            latency_ms=round((time.perf_counter() - t0) * 1000, 2),
        )

    prompt = llm.build_rag_prompt(request.query, sources)
    try:
        answer = await llm.generate(prompt)
    except Exception as exc:
        logger.exception("LLM generation failed: %s", exc)
        raise HTTPException(status_code=502, detail="LLM generation failed. Is Ollama running?")

    return QueryResult(
        query=request.query,
        answer=answer,
        sources=sources,
        latency_ms=round((time.perf_counter() - t0) * 1000, 2),
    )
