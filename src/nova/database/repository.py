from typing import Optional

from nova.database.db import SessionLocal
from nova.database.models import User, Message, GraphState


def get_user_by_telegram_id(telegram_id: int) -> Optional[User]:
    """Fetch a user by their Telegram ID."""
    with SessionLocal() as session:
        try:
            return (
                session.query(User)
                .filter(User.telegram_id == telegram_id)
                .one_or_none()
            )
        except Exception:
            return None


def create_user(
    telegram_id: int,
    name: Optional[str] = None,
    weight: Optional[float] = None,
    height: Optional[float] = None,
) -> User:
    """Create a new user and return the model."""
    with SessionLocal() as session:
        new_user = User(
            telegram_id=telegram_id, name=name, weight=weight, height=height
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user


def update_user(user: User) -> User:
    """Update an existing user in the database."""
    with SessionLocal() as session:
        db_user = session.query(User).filter(User.id == user.id).one()
        db_user.name = user.name
        db_user.weight = user.weight
        db_user.height = user.height
        session.commit()
        session.refresh(db_user)
        return db_user


def save_message(user_id: int, content: str, role: str, chat_context: str) -> Message:
    """Save a message to the database."""
    with SessionLocal() as session:
        new_message = Message(
            user_id=user_id, content=content, role=role, chat_context=chat_context
        )
        session.add(new_message)
        session.commit()
        session.refresh(new_message)
        return new_message


def get_graph_state(user_id: int) -> Optional[GraphState]:
    """Get the orchestration state for a user."""
    with SessionLocal() as session:
        return (
            session.query(GraphState)
            .filter(GraphState.user_id == user_id)
            .one_or_none()
        )


def update_graph_state(
    user_id: int,
    current_message: Optional[str],
    chat_history: Optional[str],
    current_step: Optional[str],
) -> GraphState:
    """Insert or update a graph state."""
    with SessionLocal() as session:
        db_state = (
            session.query(GraphState)
            .filter(GraphState.user_id == user_id)
            .one_or_none()
        )
        if not db_state:
            db_state = GraphState(
                user_id=user_id,
                current_message=current_message,
                chat_history=chat_history,
                current_step=current_step,
            )
            session.add(db_state)
        else:
            db_state.current_message = current_message
            db_state.chat_history = chat_history
            db_state.current_step = current_step

        session.commit()
        session.refresh(db_state)
        return db_state
