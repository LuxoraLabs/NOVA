"""Handler for /nova. Passes user message to LLM; creates user if needed."""

from telegram import Update
from telegram.ext import ContextTypes

from nova.bot.handlers.core import process_and_reply
from nova.database.repository import get_user_by_telegram_id, create_user
from nova.utils.logging import get_logger

logger = get_logger(__name__)


async def handle_nova_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Handle /nova. Pass message to LLM; create user if first contact."""
    user = update.effective_user
    if not user or not update.message:
        return

    text = " ".join(context.args) if context.args else ""
    chat_id = update.effective_chat.id
    is_private = update.effective_chat.type == "private"
    chat_context = "private" if is_private else str(chat_id)

    logger.debug(f"/nova in chat_id={chat_id}, type={update.effective_chat.type}")

    db_user = get_user_by_telegram_id(user.id)
    if not db_user:
        db_user = create_user(telegram_id=user.id, is_setup_completed=False)
        logger.info(f"Created user {user.id}")
        if is_private:
            await process_and_reply(
                update, context, text or "Hi", user, chat_id, chat_context
            )
        else:
            await process_and_reply(
                update,
                context,
                "",
                user,
                chat_id,
                str(chat_id),
                scenario="User said /nova in a group but has no profile. Call check_setup_complete first. Respond in the group: briefly ask them to send you a direct message to set up their profile (data stays private). No fixed text—reply naturally.",
            )
            try:
                await process_and_reply(
                    update,
                    context,
                    "",
                    user,
                    user.id,
                    "private",
                    scenario="User opened DM after being prompted from the group. Call check_setup_complete first. Welcome them warmly and help them complete profile setup. No fixed text—reply naturally.",
                )
            except Exception as e:
                logger.warning(f"Could not send DM to {user.id}: {e}")
        return

    await process_and_reply(update, context, text or "Hi", user, chat_id, chat_context)
