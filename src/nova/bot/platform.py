from telegram import Update
from telegram.ext import Application
from nova.utils.config import get_settings
from nova.utils.logging import get_logger

logger = get_logger(__name__)


def start_polling() -> None:
    """Initialize and start the Telegram bot polling."""
    settings = get_settings()

    # To avoid circular imports, import handlers locally or register them here
    from nova.bot.handlers import register_handlers

    app = Application.builder().token(settings.telegram_bot_token).build()

    register_handlers(app)

    logger.info("Starting Telegram bot polling...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)
