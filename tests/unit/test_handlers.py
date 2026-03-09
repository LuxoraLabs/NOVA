import pytest
from unittest import mock
from nova.bot.handlers import handle_text_message, handle_nova_command
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
async def test_handle_nova_command_in_group(mock_update, mock_context):
    """Group messages with /nova command should be processed."""
    mock_update.effective_chat.type = "group"
    mock_update.message.text = "/nova how are you?"
    mock_context.args = ["how", "are", "you?"]

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

        await handle_nova_command(mock_update, mock_context)

        # Verify command args were joined and passed
        mock_save_message.assert_any_call(
            user_id=1, content="how are you?", role="user", chat_context="999"
        )

        mock_process.assert_called_once_with(mock_db_user, "how are you?", mock.ANY)
        mock_context.bot.send_message.assert_called_once_with(
            chat_id=999, text="I am fine"
        )


@pytest.mark.asyncio
async def test_handle_nova_command_in_topic(mock_update, mock_context):
    """Group messages in a specific topic using /nova should reply to that topic."""
    mock_update.effective_chat.type = "supergroup"
    mock_update.message.text = "/nova how are you?"
    mock_update.message.message_thread_id = 42
    mock_context.args = ["how", "are", "you?"]

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

        await handle_nova_command(mock_update, mock_context)

        mock_context.bot.send_message.assert_called_once_with(
            chat_id=999, message_thread_id=42, text="Topic reply"
        )


@pytest.mark.asyncio
async def test_handle_text_group_message_reply_to_bot(mock_update, mock_context):
    """Group messages that reply to the bot should be processed even without a mention."""
    mock_update.effective_chat.type = "group"
    mock_update.message.text = "Yes, I agree."

    # Mock that this message replies to the bot
    mock_reply_to = mock.MagicMock()
    mock_reply_to.from_user.id = 99999  # Bot's ID
    mock_update.message.reply_to_message = mock_reply_to
    mock_context.bot.id = 99999

    with (
        mock.patch("nova.bot.handlers.get_user_by_telegram_id") as mock_get_user,
        mock.patch("nova.bot.handlers.save_message"),
        mock.patch("nova.bot.handlers.get_graph_state"),
        mock.patch(
            "nova.bot.handlers.process_message", return_value=("I hear you", "[]")
        ),
        mock.patch("nova.bot.handlers.update_graph_state"),
    ):
        mock_db_user = mock.MagicMock()
        mock_db_user.id = 1
        mock_get_user.return_value = mock_db_user

        await handle_text_message(mock_update, mock_context)

        mock_context.bot.send_message.assert_called_once_with(
            chat_id=999, text="I hear you"
        )


@pytest.mark.asyncio
async def test_handle_nova_command_in_group_unregistered(mock_update, mock_context):
    """Unregistered users using /nova in a group should be directed to DM."""
    mock_update.effective_chat.type = "group"
    mock_update.message.text = "/nova hello"
    mock_context.args = ["hello"]
    mock_update.effective_user.name = "@TestUser"

    with (
        mock.patch("nova.bot.handlers.get_user_by_telegram_id", return_value=None),
        mock.patch("nova.bot.handlers.process_message") as mock_process,
    ):
        await handle_nova_command(mock_update, mock_context)

        mock_process.assert_not_called()
        mock_update.message.reply_text.assert_called_once()
        args, kwargs = mock_update.message.reply_text.call_args
        assert (
            "direct message" in args[0].lower()
            or "dm" in args[0].lower()
            or "private" in args[0].lower()
        )


@pytest.mark.asyncio
async def test_handle_height_asks_for_sheet(mock_update, mock_context):
    """Providing height should now ask for Google Sheet URL."""
    from nova.bot.handlers import handle_height, SHEET_URL

    mock_update.message.text = "180.5"
    mock_context.user_data = {"name": "Test", "weight": 80.0}

    result = await handle_height(mock_update, mock_context)

    assert result == SHEET_URL
    mock_update.message.reply_text.assert_called_once()
    assert "Data Vault" in mock_update.message.reply_text.call_args[0][0]
    assert "blank spreadsheet" in mock_update.message.reply_text.call_args[0][0]


@pytest.mark.asyncio
async def test_handle_height_sheet_prompt_includes_service_account_email(
    mock_update, mock_context
):
    """When google_service_account_email is configured, prompt includes it and Editor instruction."""
    from nova.bot.handlers import handle_height, SHEET_URL

    mock_update.message.text = "180"
    mock_context.user_data = {"name": "Test", "weight": 80.0}
    service_email = "nova-bot@my-project.iam.gserviceaccount.com"

    with mock.patch("nova.bot.handlers.get_settings") as mock_get_settings:
        mock_settings = mock.MagicMock()
        mock_settings.google_service_account_email = service_email
        mock_get_settings.return_value = mock_settings

        result = await handle_height(mock_update, mock_context)

    assert result == SHEET_URL
    reply = mock_update.message.reply_text.call_args[0][0]
    assert service_email in reply
    assert "Editor" in reply


@pytest.mark.asyncio
async def test_handle_height_sheet_prompt_fallback_when_email_missing(
    mock_update, mock_context
):
    """When google_service_account_email is not configured, prompt uses generic instructions."""
    from nova.bot.handlers import handle_height, SHEET_URL

    mock_update.message.text = "180"
    mock_context.user_data = {"name": "Test", "weight": 80.0}

    with mock.patch("nova.bot.handlers.get_settings") as mock_get_settings:
        mock_settings = mock.MagicMock()
        mock_settings.google_service_account_email = None
        mock_get_settings.return_value = mock_settings

        result = await handle_height(mock_update, mock_context)

    assert result == SHEET_URL
    reply = mock_update.message.reply_text.call_args[0][0]
    assert "Data Vault" in reply
    assert "share" in reply.lower() or "Share" in reply
    assert "Editor" in reply


@pytest.mark.asyncio
async def test_handle_sheet_url_success(mock_update, mock_context):
    """Providing a sheet URL finishes registration."""
    from nova.bot.handlers import handle_sheet_url
    from telegram.ext import ConversationHandler

    mock_update.message.text = "https://docs.google.com/spreadsheets/d/12345/edit"
    mock_context.user_data = {"name": "Test", "weight": 80.0, "height": 180.5}

    with mock.patch("nova.bot.handlers.create_user") as mock_create_user:
        result = await handle_sheet_url(mock_update, mock_context)

        assert result == ConversationHandler.END
        mock_create_user.assert_called_once_with(
            telegram_id=mock_update.effective_user.id,
            name="Test",
            weight=80.0,
            height=180.5,
            google_sheet_url="https://docs.google.com/spreadsheets/d/12345/edit",
        )
        mock_update.message.reply_text.assert_called_once()
        assert "Registration complete" in mock_update.message.reply_text.call_args[0][0]
