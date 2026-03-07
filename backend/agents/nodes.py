from __future__ import annotations

from typing import Any

from backend.core import llm
from backend.agents.tools import retrieve_tool
from backend.core.logging import get_logger

logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# State schema is a plain dict passed between nodes.
# Keys used:
#   task        : str   — original user task
#   query       : str   — refined search query (set by planner)
#   sources     : list  — retrieved chunks
#   answer      : str   — synthesized answer
#   trace       : list  — reasoning trace entries
# ---------------------------------------------------------------------------


async def planner_node(state: dict[str, Any]) -> dict[str, Any]:
    """
    Decompose the user task into a focused retrieval query.
    Appends a trace entry.
    """
    task = state["task"]
    prompt = (
        f"You are a research assistant. "
        f"Given the following task, generate a concise search query (max 20 words) "
        f"that will retrieve the most relevant information from a knowledge base.\n\n"
        f"Task: {task}\n\n"
        f"Search query:"
    )
    query = await llm.generate(prompt)
    query = query.strip().strip('"').strip("'")
    logger.info("Planner produced query: %s", query)

    trace = state.get("trace", [])
    trace.append({"node": "planner", "output": query})
    return {**state, "query": query, "trace": trace}


async def retriever_node(state: dict[str, Any]) -> dict[str, Any]:
    """Retrieve relevant chunks using the refined query."""
    query = state.get("query") or state["task"]
    sources = retrieve_tool(query, k=5)
    logger.info("Retriever found %d sources", len(sources))

    trace = state.get("trace", [])
    trace.append({"node": "retriever", "output": f"{len(sources)} chunks retrieved"})
    return {**state, "sources": sources, "trace": trace}


async def synthesizer_node(state: dict[str, Any]) -> dict[str, Any]:
    """Synthesize a final answer from the task and retrieved sources."""
    task = state["task"]
    sources = state.get("sources", [])

    prompt = llm.build_rag_prompt(task, sources) if sources else (
        f"Answer the following task as best you can:\n\n{task}\n\nAnswer:"
    )
    answer = await llm.generate(prompt)
    logger.info("Synthesizer produced answer (%d chars)", len(answer))

    trace = state.get("trace", [])
    trace.append({"node": "synthesizer", "output": answer[:200] + "..." if len(answer) > 200 else answer})
    return {**state, "answer": answer, "trace": trace}
