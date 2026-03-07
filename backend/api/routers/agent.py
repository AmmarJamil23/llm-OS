from __future__ import annotations

import time

from fastapi import APIRouter, HTTPException

from backend.core.models import AgentRequest, AgentResponse
from backend.core.logging import get_logger
from backend.agents.graph import run_agent

logger = get_logger(__name__)
router = APIRouter()


@router.post("/agent/run", response_model=AgentResponse, tags=["agent"])
async def run_agent_endpoint(request: AgentRequest) -> AgentResponse:
    """Execute the research agent on a task."""
    t0 = time.perf_counter()
    try:
        state = await run_agent(request.task)
    except Exception as exc:
        logger.exception("Agent run failed: %s", exc)
        raise HTTPException(status_code=500, detail="Agent execution failed. Check server logs.")

    return AgentResponse(
        result=state.get("answer", ""),
        trace=state.get("trace", []),
        latency_ms=round((time.perf_counter() - t0) * 1000, 2),
    )
