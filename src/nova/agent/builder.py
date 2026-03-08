from langgraph.graph import StateGraph, END
from nova.agent.state import AgentState
from nova.agent.nodes.llm import invoke_llm


def build_graph() -> StateGraph:
    """Build the LangGraph workflow."""
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", invoke_llm)
    workflow.set_entry_point("agent")
    workflow.add_edge("agent", END)
    return workflow.compile()
