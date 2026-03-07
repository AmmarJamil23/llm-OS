from __future__ import annotations

from backend.retrieval.search import similarity_search


def retrieve_tool(query: str, k: int = 5) -> list[dict]:
    """
    Retrieval tool callable by the agent.
    Returns a list of chunk dicts ranked by similarity.
    """
    return similarity_search(query, k=k)
