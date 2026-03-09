from typing import Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from nova.agent.state import AgentState
from nova.utils.config import get_settings
from nova.agent.persona import NOVA_SYSTEM_PROMPT
from nova.utils.logging import get_logger
from nova.agent.nodes.tools import tools

logger = get_logger(__name__)


def invoke_llm(state: AgentState) -> dict[str, Any]:
    """Invoke the LLM (Planner) with context and tools."""
    logger.info(f"Invoking LLM Planner for user: {state.user.name}")
    settings = get_settings()

    base_llm = ChatOpenAI(
        model="gpt-4o-mini", temperature=0.7, api_key=settings.openai_api_key
    )

    llm_with_tools = base_llm.bind_tools(tools)

    system_prompt = (
        NOVA_SYSTEM_PROMPT
        + f"\n\nUser Profile:\nName: {state.user.name}\nWeight: {state.user.weight}kg\nHeight: {state.user.height}cm"
    )

    # Compile messages: system prompt + chat history + agent steps (messages) + current message
    msgs = [SystemMessage(content=system_prompt)] + state.chat_history

    if state.current_message and not state.messages:
        # If this is the first turn in the current graph run
        msgs.append(HumanMessage(content=state.current_message))
    else:
        # If we are iterating, include previous messages from this run
        msgs.extend(state.messages)

    try:
        response = llm_with_tools.invoke(msgs)
        return {"messages": [response]}
    except Exception as e:
        logger.error(f"LLM Error: {e}")
        return {"messages": []}
