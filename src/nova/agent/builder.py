from langgraph.graph import StateGraph
from nova.agent.state import AgentState
from nova.agent.nodes.llm import invoke_llm
from nova.agent.nodes.tools import tool_node
from langgraph.prebuilt import tools_condition


def build_graph() -> StateGraph:
    """Build the LangGraph workflow."""
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", invoke_llm)
    workflow.add_node("tools", tool_node)

    workflow.set_entry_point("agent")

    # Conditional edge from agent to tools or END
    workflow.add_conditional_edges(
        "agent",
        tools_condition,
    )

    # Edge from tools back to agent
    workflow.add_edge("tools", "agent")

    return workflow.compile()
