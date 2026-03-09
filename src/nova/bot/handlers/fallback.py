"""Fallback: non-text messages (stickers, photos, etc.)—ignore or brief reply."""

from telegram import Update
from telegram.ext import ContextTypes


async def handle_non_text_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Non-text: send text to use /nova."""
    if update.message:
        await update.message.reply_text("Send text or /nova to interact.")
