"""Unified logging setup for the application"""

import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler
from rich.logging import RichHandler


def setup_unified_logging(
    log_level: str = "INFO",
    log_dir: str = "./logs",
    enable_console: bool = True,
    enable_file: bool = True,
    cli_mode: bool = False,
) -> None:
    """Setup unified logging configuration."""
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    if enable_file:
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)

    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    root_logger.handlers.clear()

    for logger_name, logger_obj in logging.root.manager.loggerDict.items():
        if isinstance(logger_obj, logging.Logger):
            logger_obj.setLevel(logging.NOTSET)
            logger_obj.propagate = True

    noisy_loggers = (
        "asyncio",
        "httpx",
        "httpcore",
        "openai",
        "aio_pika",
        "aiormq",
        "urllib3",
        "sqlalchemy.engine",
        "sqlalchemy.orm",
        "sqlalchemy.pool",
        "telegram",
        "telegram.ext",
    )
    for logger_name in noisy_loggers:
        logging.getLogger(logger_name).setLevel(logging.WARNING)

    if enable_console:
        if cli_mode:
            console_handler = RichHandler(
                rich_tracebacks=True,
                markup=True,
                show_time=False,
                show_level=False,
                show_path=False,
            )
        else:
            console_handler = RichHandler(
                rich_tracebacks=True,
                markup=True,
                show_time=True,
                show_level=True,
                show_path=False,
                log_time_format="[%H:%M:%S]",
            )
        console_handler.setLevel(numeric_level)
        root_logger.addHandler(console_handler)

    if enable_file:
        log_file = Path(log_dir) / "nova_bot.log"
        file_handler = RotatingFileHandler(
            log_file, maxBytes=10 * 1024 * 1024, backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for the given name."""
    return logging.getLogger(name)
