from nova.database.models import GraphState as DBGraphState, User
from nova.agent.state import AgentState, load_history, serialize_history
from nova.agent.builder import build_graph

# Compile graph once
graph_app = build_graph()


def process_message(
    user: User, text: str, db_state: DBGraphState | None
) -> tuple[str, str]:
    """Process an incoming message and return the response and updated history."""
    history_str = db_state.chat_history if db_state else "[]"

    initial_state = AgentState(
        user=user, current_message=text, chat_history=load_history(history_str)
    )

    result = graph_app.invoke(initial_state)
    new_history_str = serialize_history(result["chat_history"])
    return result["response"], new_history_str
