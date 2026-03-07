from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from backend.core import llm

router = APIRouter()


@router.get("/health", tags=["health"])
async def health_check():
    ollama_ok = await llm.is_available()
    return JSONResponse(
        content={
            "status": "ok",
            "ollama": "available" if ollama_ok else "unavailable",
        }
    )
