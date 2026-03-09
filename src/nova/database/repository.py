from typing import Optional

from nova.database.db import SessionLocal
from nova.database.models import User, Message, GraphState, DailyMetric


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
    google_sheet_url: Optional[str] = None,
    is_setup_completed: bool = False,
) -> User:
    """Create a new user and return the model."""
    with SessionLocal() as session:
        new_user = User(
            telegram_id=telegram_id,
            name=name,
            weight=weight,
            height=height,
            google_sheet_url=google_sheet_url,
            is_setup_completed=is_setup_completed,
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user


REQUIRED_PROFILE_FIELDS = ["name", "weight", "height", "google_sheet_url"]


def update_user_profile_partial(user_id: int, **kwargs: object) -> Optional[User]:
    """Update only provided profile fields for the user."""
    allowed = {"name", "weight", "height", "google_sheet_url"}
    to_update = {k: v for k, v in kwargs.items() if k in allowed and v is not None}
    if not to_update:
        return get_user_by_id(user_id)

    with SessionLocal() as session:
        db_user = session.query(User).filter(User.id == user_id).one_or_none()
        if not db_user:
            return None
        for k, v in to_update.items():
            setattr(db_user, k, v)
        session.commit()
    recompute_setup_completed(user_id)
    return get_user_by_id(user_id)


def get_user_by_id(user_id: int) -> Optional[User]:
    """Fetch a user by their internal ID."""
    with SessionLocal() as session:
        return session.query(User).filter(User.id == user_id).one_or_none()


def get_missing_profile_fields(user_id: int) -> list[str]:
    """Return list of required field names that are null/empty."""
    user = get_user_by_id(user_id)
    if not user:
        return list(REQUIRED_PROFILE_FIELDS)
    missing: list[str] = []
    if not user.name or not str(user.name).strip():
        missing.append("name")
    if user.weight is None:
        missing.append("weight")
    if user.height is None:
        missing.append("height")
    if not user.google_sheet_url or not str(user.google_sheet_url).strip():
        missing.append("google_sheet_url")
    return missing


def recompute_setup_completed(user_id: int) -> bool:
    """Set is_setup_completed based on current field values; return new value."""
    missing = get_missing_profile_fields(user_id)
    new_value = len(missing) == 0

    with SessionLocal() as session:
        db_user = session.query(User).filter(User.id == user_id).one_or_none()
        if not db_user:
            return False
        db_user.is_setup_completed = new_value
        session.commit()
        session.refresh(db_user)
        return db_user.is_setup_completed


def update_user(user: User) -> User:
    """Update an existing user in the database."""
    with SessionLocal() as session:
        db_user = session.query(User).filter(User.id == user.id).one()
        db_user.name = user.name
        db_user.weight = user.weight
        db_user.height = user.height
        db_user.google_sheet_url = user.google_sheet_url
        db_user.is_setup_completed = user.is_setup_completed
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


def save_daily_metric(
    user_id: int, date_str: str, metric_type: str, value: float
) -> DailyMetric:
    """Save or update a daily metric for a user."""
    from datetime import datetime

    parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()

    with SessionLocal() as session:
        metric = (
            session.query(DailyMetric)
            .filter(
                DailyMetric.user_id == user_id,
                DailyMetric.date == parsed_date,
                DailyMetric.metric_type == metric_type,
            )
            .one_or_none()
        )

        if metric:
            metric.value = value
        else:
            metric = DailyMetric(
                user_id=user_id, date=parsed_date, metric_type=metric_type, value=value
            )
            session.add(metric)

        session.commit()
        session.refresh(metric)
        return metric
