from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    """Domain model representing a N.O.V.A user."""

    id: Optional[int] = None
    telegram_id: int
    name: Optional[str] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    created_at: Optional[datetime] = None


class Message(BaseModel):
    """Domain model representing a message in the system."""

    id: Optional[int] = None
    user_id: int
    content: str
    role: str
    chat_context: str
    timestamp: Optional[datetime] = None


class GraphState(BaseModel):
    """Domain model representing the orchestration state for LangGraph."""

    user_id: int
    current_message: Optional[str] = None
    chat_history: Optional[str] = None
    current_step: Optional[str] = None
    updated_at: Optional[datetime] = None
