from __future__ import annotations

import httpx

from backend.core.config import settings
from backend.core.logging import get_logger

logger = get_logger(__name__)

_GENERATE_URL = "/api/generate"
_CHAT_URL = "/api/chat"


async def generate(prompt: str, model: str | None = None, system: str | None = None) -> str:
    """
    Send a prompt to Ollama and return the complete response text.

    Uses the /api/generate endpoint (single-turn).
    """
    model = model or settings.ollama_model
    payload: dict = {"model": model, "prompt": prompt, "stream": False}
    if system:
        payload["system"] = system

    url = settings.ollama_base_url.rstrip("/") + _GENERATE_URL
    logger.debug("Ollama generate model=%s url=%s", model, url)

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

    return data.get("response", "").strip()


async def chat(messages: list[dict], model: str | None = None) -> str:
    """
    Multi-turn chat with Ollama using the /api/chat endpoint.

    *messages* should be a list of {"role": "user"|"assistant"|"system", "content": str}.
    Returns the assistant's reply string.
    """
    model = model or settings.ollama_model
    payload = {"model": model, "messages": messages, "stream": False}

    url = settings.ollama_base_url.rstrip("/") + _CHAT_URL
    logger.debug("Ollama chat model=%s turns=%d", model, len(messages))

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

    return data.get("message", {}).get("content", "").strip()


async def is_available() -> bool:
    """Return True if the Ollama server is reachable."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(settings.ollama_base_url.rstrip("/") + "/api/tags")
            return resp.status_code == 200
    except Exception:
        return False


def build_rag_prompt(query: str, context_chunks: list[dict]) -> str:
    """Assemble a RAG prompt from retrieved context chunks."""
    context = "\n\n---\n\n".join(
        f"[Source: {c.get('metadata', {}).get('filename', 'unknown')}]\n{c['text']}"
        for c in context_chunks
    )
    return (
        f"You are a knowledgeable research assistant. "
        f"Answer the question using only the provided context. "
        f"If the context does not contain the answer, say so.\n\n"
        f"CONTEXT:\n{context}\n\n"
        f"QUESTION: {query}\n\n"
        f"ANSWER:"
    )
