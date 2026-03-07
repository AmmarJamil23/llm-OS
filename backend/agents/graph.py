from __future__ import annotations

from typing import Any

from langgraph.graph import StateGraph, END

from backend.agents.nodes import planner_node, retriever_node, synthesizer_node
from backend.core.logging import get_logger

logger = get_logger(__name__)


def build_agent_graph() -> StateGraph:
    """
    Build and compile the research agent graph.

    Nodes:
        planner    → refine user task into a search query
        retriever  → fetch relevant chunks from vector store
        synthesizer → generate a final answer from context
    """
    graph = StateGraph(dict)

    graph.add_node("planner", planner_node)
    graph.add_node("retriever", retriever_node)
    graph.add_node("synthesizer", synthesizer_node)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "retriever")
    graph.add_edge("retriever", "synthesizer")
    graph.add_edge("synthesizer", END)

    return graph.compile()


# Singleton compiled graph
_agent = None


def get_agent():
    global _agent
    if _agent is None:
        _agent = build_agent_graph()
    return _agent


async def run_agent(task: str) -> dict[str, Any]:
    """Run the agent on a task and return final state."""
    agent = get_agent()
    initial_state: dict[str, Any] = {"task": task, "trace": []}
    final_state = await agent.ainvoke(initial_state)
    return final_state
