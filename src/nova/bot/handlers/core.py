"""Shared message processing logic for Nova bot handlers."""

from telegram import Update
from telegram.ext import ContextTypes

from nova.agent.orchestrator import process_message
from nova.database.repository import (
    get_user_by_telegram_id,
    create_user,
    get_graph_state,
    update_graph_state,
    save_message,
)
from nova.utils.logging import get_logger

logger = get_logger(__name__)


async def process_and_reply(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    text: str,
    user,
    chat_id: int,
    chat_context: str,
    scenario: str | None = None,
) -> None:
    """Core logic to process message, invoke LangGraph, and send a reply."""
    db_user = get_user_by_telegram_id(user.id)
    if not db_user:
        is_private = update.effective_chat.type == "private"
        if is_private:
            db_user = create_user(
                telegram_id=user.id,
                is_setup_completed=False,
            )
        else:
            await update.message.reply_text(
                f"Operator {user.name or ''} not recognized. Please send me a direct message to securely initialize your profile."
            )
            return

    # Save incoming message
    save_message(
        user_id=db_user.id, content=text, role="user", chat_context=chat_context
    )

    # Get state
    db_state = get_graph_state(db_user.id)

    try:
        response, new_history = process_message(
            db_user, text, db_state, scenario=scenario
        )

        # Save updated state
        update_graph_state(
            user_id=db_user.id,
            current_message=text,
            chat_history=new_history,
            current_step="completed",
        )

        # Save outgoing message
        save_message(
            user_id=db_user.id,
            content=response,
            role="assistant",
            chat_context=chat_context,
        )

        send_kwargs = {"chat_id": chat_id, "text": response, "parse_mode": "HTML"}
        # Only add thread_id for supergroups; DMs (chat_id > 0) must never get it.
        if (
            chat_id < 0
            and update.message.message_thread_id
            and chat_id == update.effective_chat.id
            and update.effective_chat.type == "supergroup"
        ):
            send_kwargs["message_thread_id"] = update.message.message_thread_id

        logger.debug(
            f"Routing response to chat_id: {chat_id}, thread_id: {update.message.message_thread_id}"
        )
        await context.bot.send_message(**send_kwargs)
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await context.bot.send_message(
            chat_id=chat_id,
            text="N.O.V.A system error. Connection to cognitive core failed.",
            parse_mode="HTML",
        )
