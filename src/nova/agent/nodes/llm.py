from typing import Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from nova.agent.state import AgentState
from nova.utils.config import get_settings
from nova.agent.persona import NOVA_SYSTEM_PROMPT, SETUP_MODE_PROMPT
from nova.utils.logging import get_logger
from nova.agent.nodes.tools import get_tools_for_user

logger = get_logger(__name__)


def invoke_llm(state: AgentState) -> dict[str, Any]:
    """Invoke the LLM (Planner) with context and tools."""
    user = state.user
    logger.info(f"Invoking LLM Planner for user: {user.name or user.telegram_id}")
    settings = get_settings()

    base_llm = ChatOpenAI(
        model="gpt-4o-mini", temperature=0.7, api_key=settings.openai_api_key
    )

    tools = get_tools_for_user(user.is_setup_completed)
    llm_with_tools = base_llm.bind_tools(tools)

    if user.is_setup_completed:
        profile_block = f"\n\nUser Profile:\nName: {user.name}\nWeight: {user.weight}kg\nHeight: {user.height}cm"
        system_prompt = NOVA_SYSTEM_PROMPT + profile_block
    else:
        sheet_email = settings.google_service_account_email
        if sheet_email:
            sheet_block = (
                "\n\nGoogle Sheet guide (share this when asking for their sheet URL):\n"
                "Here's how to connect your Google Sheet:\n\n"
                "1️⃣ Go to sheets.google.com and create a new blank spreadsheet.\n"
                "2️⃣ Click the green Share button (top right).\n"
                f"3️⃣ Add {sheet_email} as Editor (so I can set up your dashboard).\n"
                "4️⃣ Copy the URL from your browser (e.g. https://docs.google.com/spreadsheets/d/xxxxx/edit) and paste it here.\n\n"
                "Once you share it, I'll set up your Dashboard and Daily Logs tabs. 😊"
            )
        else:
            sheet_block = (
                "\n\nGoogle Sheet guide (share this when asking for their sheet URL):\n"
                "Here's how to connect your Google Sheet:\n\n"
                "1️⃣ Go to sheets.google.com and create a new blank spreadsheet.\n"
                "2️⃣ Click the green Share button (top right).\n"
                "3️⃣ Add our service account as Editor (I'll provide the email when needed).\n"
                "4️⃣ Copy the URL from your browser and paste it here.\n\n"
                "Once you share it, I'll set up your Dashboard and Daily Logs tabs. 😊"
            )
        system_prompt = (
            SETUP_MODE_PROMPT
            + sheet_block
            + f"\n\nThe user's internal ID is {user.id}. Always pass user_id={user.id} when calling tools."
        )
    if state.scenario:
        system_prompt += f"\n\nContext: {state.scenario}"

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
