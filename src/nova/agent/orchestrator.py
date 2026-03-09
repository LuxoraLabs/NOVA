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

    from langchain_core.messages import HumanMessage, AIMessage

    initial_state = AgentState(
        user=user,
        current_message=text,
        chat_history=load_history(history_str),
        messages=[HumanMessage(content=text)],
    )

    result = graph_app.invoke(initial_state)

    # Extract the final AI message from the generated messages
    final_messages = result.get("messages", [])
    response_text = "No response"

    if final_messages:
        # Get the last message, which should be the AI's final answer
        last_message = final_messages[-1]
        response_text = str(last_message.content)

    # Build new history by combining existing history with the new interaction
    new_chat_history = result.get("chat_history", []) + [
        HumanMessage(content=text),
        AIMessage(content=response_text),
    ]

    new_history_str = serialize_history(new_chat_history)
    return response_text, new_history_str
