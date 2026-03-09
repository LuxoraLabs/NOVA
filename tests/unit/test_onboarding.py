import pytest
from unittest import mock
from nova.bot.handlers import (
    start_command,
    handle_name,
    handle_weight,
    handle_height,
    cancel_onboarding,
    NAME,
    WEIGHT,
    HEIGHT,
)
from telegram import Update, User as TelegramUser, Message
from telegram.ext import ContextTypes, ConversationHandler


@pytest.fixture
def mock_update():
    update = mock.AsyncMock(spec=Update)
    user = mock.MagicMock(spec=TelegramUser)
    user.id = 12345
    update.effective_user = user

    message = mock.AsyncMock(spec=Message)
    update.message = message

    return update


@pytest.fixture
def mock_context():
    context = mock.MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.user_data = {}
    return context


@pytest.mark.asyncio
async def test_start_command_new_user(mock_update, mock_context):
    with mock.patch("nova.bot.handlers.get_user_by_telegram_id", return_value=None):
        state = await start_command(mock_update, mock_context)

        assert state == NAME
        mock_update.message.reply_text.assert_called_once()
        assert (
            "What is your preferred Name/Callsign?"
            in mock_update.message.reply_text.call_args[0][0]
        )


@pytest.mark.asyncio
async def test_start_command_existing_user(mock_update, mock_context):
    mock_db_user = mock.MagicMock()
    mock_db_user.name = "TestUser"

    with mock.patch(
        "nova.bot.handlers.get_user_by_telegram_id", return_value=mock_db_user
    ):
        state = await start_command(mock_update, mock_context)

        assert state == ConversationHandler.END
        mock_update.message.reply_text.assert_called_once()
        assert "Welcome back" in mock_update.message.reply_text.call_args[0][0]


@pytest.mark.asyncio
async def test_handle_name(mock_update, mock_context):
    mock_update.message.text = "John Doe"

    state = await handle_name(mock_update, mock_context)

    assert state == WEIGHT
    assert mock_context.user_data["name"] == "John Doe"
    mock_update.message.reply_text.assert_called_once()
    assert "weight" in mock_update.message.reply_text.call_args[0][0].lower()


@pytest.mark.asyncio
async def test_handle_weight_valid(mock_update, mock_context):
    mock_update.message.text = "75.5"

    state = await handle_weight(mock_update, mock_context)

    assert state == HEIGHT
    assert mock_context.user_data["weight"] == 75.5
    mock_update.message.reply_text.assert_called_once()
    assert "height" in mock_update.message.reply_text.call_args[0][0].lower()


@pytest.mark.asyncio
async def test_handle_weight_invalid(mock_update, mock_context):
    mock_update.message.text = "abc"

    state = await handle_weight(mock_update, mock_context)

    assert state == WEIGHT
    assert "weight" not in mock_context.user_data
    mock_update.message.reply_text.assert_called_once()
    assert "Invalid input" in mock_update.message.reply_text.call_args[0][0]


@pytest.mark.asyncio
async def test_handle_height_valid(mock_update, mock_context):
    from nova.bot.handlers import SHEET_URL

    mock_update.message.text = "180"
    mock_context.user_data = {"name": "John", "weight": 75.5}

    state = await handle_height(mock_update, mock_context)

    assert state == SHEET_URL
    assert mock_context.user_data["height"] == 180.0

    mock_update.message.reply_text.assert_called_once()
    assert "Data Vault" in mock_update.message.reply_text.call_args[0][0]


@pytest.mark.asyncio
async def test_cancel_onboarding(mock_update, mock_context):
    state = await cancel_onboarding(mock_update, mock_context)

    assert state == ConversationHandler.END
    mock_update.message.reply_text.assert_called_once()
    assert "canceled" in mock_update.message.reply_text.call_args[0][0].lower()
