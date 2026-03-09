import json
from typing import List, Annotated
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langgraph.graph.message import add_messages

from nova.database.models import User
from nova.utils.logging import get_logger

logger = get_logger(__name__)


class AgentState(BaseModel):
    user: User
    current_message: str
    chat_history: List[BaseMessage] = Field(default_factory=list)
    messages: Annotated[List[BaseMessage], add_messages] = Field(default_factory=list)
    response: str = ""

    model_config = {"arbitrary_types_allowed": True}


def load_history(chat_history_str: str | None) -> List[BaseMessage]:
    """Parse JSON chat history string into BaseMessages."""
    if not chat_history_str:
        return []
    try:
        data = json.loads(chat_history_str)
        messages: List[BaseMessage] = []
        for msg in data:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
        return messages
    except Exception as e:
        logger.error(f"Error parsing chat history: {e}")
        return []


def serialize_history(messages: List[BaseMessage]) -> str:
    """Serialize BaseMessages into JSON string."""
    data = []
    for msg in messages[-10:]:  # Keep last 10 messages for memory
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        data.append({"role": role, "content": msg.content})
    return json.dumps(data)
