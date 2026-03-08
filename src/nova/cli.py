import typer
import asyncio
from typing import Optional
from nova.utils.logging import setup_unified_logging, get_logger
from nova.utils.config import get_settings
from nova.database.db import init_db

app = typer.Typer(name="nova", help="N.O.V.A. MVP Comm Link CLI")
logger = get_logger(__name__)


@app.command()
def run(
    log_level: Optional[str] = typer.Option(None, help="Override log level"),
) -> None:
    """Run the N.O.V.A. Telegram bot."""
    settings = get_settings()
    level = log_level or settings.log_level

    setup_unified_logging(log_level=level, cli_mode=False)
    logger.info("Starting N.O.V.A. bot...")

    # Initialize DB
    init_db()

    # Run bot
    asyncio.run(start_bot())


async def start_bot() -> None:
    """Run the async bot polling."""
    from nova.bot.platform import start_polling

    await start_polling()


if __name__ == "__main__":
    app()
