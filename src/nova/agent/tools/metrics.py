from langchain_core.tools import tool

from nova.utils.logging import get_logger

logger = get_logger(__name__)


@tool
def record_weight(weight: float, date: str) -> str:
    """Record the user's weight for a specific date."""
    # This tool needs access to state/user id, which is tricky with simple @tool
    # We will pass user_id via config or just use state in graph.
    # For now, since LangChain tools don't natively receive state without InjectedState,
    # Let's import InjectedState.
    pass
