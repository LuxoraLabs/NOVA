"""Handler for direct text messages (private chat only)."""

from telegram import Update
from telegram.ext import ContextTypes

from nova.bot.handlers.core import process_and_reply
from nova.utils.logging import get_logger

logger = get_logger(__name__)


async def handle_text_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Handle standard text messages in private chat only. Groups/channels/topics require /nova."""
    user = update.effective_user
    if not user or not update.message:
        return

    text = update.message.text or update.message.caption
    if not text:
        return

    if update.effective_chat.type != "private":
        return  # Ignore direct messages in groups, channels, topics—use /nova there

    chat_id = update.effective_chat.id
    chat_context = "private"

    logger.debug(
        f"Received message payload in chat_id: {chat_id}, thread_id: {update.message.message_thread_id}"
    )

    await process_and_reply(update, context, text, user, chat_id, chat_context)
