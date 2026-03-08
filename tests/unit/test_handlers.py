import pytest
from unittest import mock
from nova.bot.handlers import handle_text_message
from telegram import Update, User as TelegramUser, Message, Chat
from telegram.ext import ContextTypes


@pytest.fixture
def mock_update():
    update = mock.AsyncMock(spec=Update)

    user = mock.MagicMock(spec=TelegramUser)
    user.id = 12345
    update.effective_user = user

    message = mock.AsyncMock(spec=Message)
    message.text = "Hello there"
    message.message_thread_id = None
    update.message = message

    chat = mock.MagicMock(spec=Chat)
    chat.id = 999
    chat.type = "private"
    update.effective_chat = chat

    return update


@pytest.fixture
def mock_context():
    context = mock.MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.bot.username = "test_bot"
    context.bot.send_message = mock.AsyncMock()
    return context


@pytest.mark.asyncio
async def test_handle_text_private_message(mock_update, mock_context):
    """Private messages should always be processed."""
    with (
        mock.patch("nova.bot.handlers.get_user_by_telegram_id") as mock_get_user,
        mock.patch("nova.bot.handlers.save_message"),
        mock.patch("nova.bot.handlers.get_graph_state"),
        mock.patch("nova.bot.handlers.process_message", return_value=("Hi", "[]")),
        mock.patch("nova.bot.handlers.update_graph_state"),
    ):

        mock_db_user = mock.MagicMock()
        mock_db_user.id = 1
        mock_get_user.return_value = mock_db_user

        await handle_text_message(mock_update, mock_context)

        # Verify it went through and sent a reply
        mock_context.bot.send_message.assert_called_once_with(chat_id=999, text="Hi")


@pytest.mark.asyncio
async def test_handle_text_group_message_no_mention(mock_update, mock_context):
    """Group messages without mention should be ignored."""
    mock_update.effective_chat.type = "group"
    mock_update.message.text = "Hello everyone"

    with mock.patch("nova.bot.handlers.get_user_by_telegram_id") as mock_get_user:
        await handle_text_message(mock_update, mock_context)

        # User shouldn't even be looked up
        mock_get_user.assert_not_called()
        mock_context.bot.send_message.assert_not_called()


@pytest.mark.asyncio
async def test_handle_text_group_message_with_mention(mock_update, mock_context):
    """Group messages with mention should strip mention and process."""
    mock_update.effective_chat.type = "group"
    mock_update.message.text = "Hey @test_bot, how are you?"

    with (
        mock.patch("nova.bot.handlers.get_user_by_telegram_id") as mock_get_user,
        mock.patch("nova.bot.handlers.save_message") as mock_save_message,
        mock.patch("nova.bot.handlers.get_graph_state"),
        mock.patch(
            "nova.bot.handlers.process_message", return_value=("I am fine", "[]")
        ) as mock_process,
        mock.patch("nova.bot.handlers.update_graph_state"),
    ):

        mock_db_user = mock.MagicMock()
        mock_db_user.id = 1
        mock_get_user.return_value = mock_db_user

        await handle_text_message(mock_update, mock_context)

        # Verify mention was stripped before processing
        mock_save_message.assert_any_call(
            user_id=1, content="Hey , how are you?", role="user", chat_context="999"
        )

        mock_process.assert_called_once_with(
            mock_db_user, "Hey , how are you?", mock.ANY
        )
        mock_context.bot.send_message.assert_called_once_with(
            chat_id=999, text="I am fine"
        )


@pytest.mark.asyncio
async def test_handle_text_group_topic_mention(mock_update, mock_context):
    """Group messages in a specific topic should reply to that specific topic."""
    mock_update.effective_chat.type = "supergroup"
    mock_update.message.text = "Hey @test_bot, how are you?"
    mock_update.message.message_thread_id = 42

    with (
        mock.patch("nova.bot.handlers.get_user_by_telegram_id") as mock_get_user,
        mock.patch("nova.bot.handlers.save_message"),
        mock.patch("nova.bot.handlers.get_graph_state"),
        mock.patch(
            "nova.bot.handlers.process_message", return_value=("Topic reply", "[]")
        ),
        mock.patch("nova.bot.handlers.update_graph_state"),
    ):

        mock_db_user = mock.MagicMock()
        mock_db_user.id = 1
        mock_get_user.return_value = mock_db_user

        await handle_text_message(mock_update, mock_context)

        mock_context.bot.send_message.assert_called_once_with(
            chat_id=999, message_thread_id=42, text="Topic reply"
        )
