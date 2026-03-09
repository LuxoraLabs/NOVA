"""Bot handlers: pass user messages to LLM, save to database. Only /nova command."""

from telegram.ext import Application, CommandHandler, MessageHandler, filters

from nova.bot.handlers.nova import handle_nova_command
from nova.bot.handlers.text import handle_text_message
from nova.bot.handlers.fallback import handle_non_text_message

__all__ = [
    "handle_nova_command",
    "handle_text_message",
    "handle_non_text_message",
    "register_handlers",
]


def register_handlers(app: Application) -> None:
    """Register handlers. Only /nova command; all text passes to LLM."""
    app.add_handler(CommandHandler("nova", handle_nova_command))
    app.add_handler(
        MessageHandler(
            (filters.TEXT | filters.CAPTION) & ~filters.COMMAND,
            handle_text_message,
        )
    )
    app.add_handler(
        MessageHandler(
            ~(filters.TEXT | filters.CAPTION) & ~filters.COMMAND,
            handle_non_text_message,
        )
    )
