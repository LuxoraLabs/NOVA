from typing import Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from nova.agent.state import AgentState
from nova.utils.config import get_settings
from nova.agent.persona import NOVA_SYSTEM_PROMPT
from nova.utils.logging import get_logger

logger = get_logger(__name__)


def invoke_llm(state: AgentState) -> dict[str, Any]:
    """Invoke the LLM with context."""
    logger.info(f"Invoking LLM for user: {state.user.name}")
    settings = get_settings()

    # Optional API Key handling (can fall back to env var)
    llm = ChatOpenAI(
        model="gpt-4o-mini", temperature=0.7, api_key=settings.openai_api_key
    )

    system_prompt = (
        NOVA_SYSTEM_PROMPT
        + f"\n\nUser Profile:\nName: {state.user.name}\nWeight: {state.user.weight}kg\nHeight: {state.user.height}cm"
    )
    messages = (
        [SystemMessage(content=system_prompt)]
        + state.chat_history
        + [HumanMessage(content=state.current_message)]
    )

    try:
        response = llm.invoke(messages)
        new_response_text = str(response.content)
    except Exception as e:
        logger.error(f"LLM Error: {e}")
        new_response_text = "N.O.V.A system error. Connection to cognitive core failed. Please try again."

    new_history = state.chat_history + [
        HumanMessage(content=state.current_message),
        AIMessage(content=new_response_text),
    ]
    return {"response": new_response_text, "chat_history": new_history}
