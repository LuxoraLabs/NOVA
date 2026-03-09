from nova.database.repository import (
    create_user,
    get_user_by_telegram_id,
    update_user,
    update_user_profile_partial,
    get_missing_profile_fields,
    recompute_setup_completed,
    save_message,
    get_graph_state,
    update_graph_state,
)


def test_update_user_profile_partial(mock_db_session):
    """update_user_profile_partial updates only provided fields and recomputes is_setup_completed."""
    user = create_user(
        telegram_id=99999,
        is_setup_completed=False,
    )
    assert user.is_setup_completed is False

    updated = update_user_profile_partial(user.id, name="Alice", weight=65.0)
    assert updated is not None
    assert updated.name == "Alice"
    assert updated.weight == 65.0
    assert updated.height is None
    assert updated.is_setup_completed is False  # still missing height, google_sheet_url

    updated2 = update_user_profile_partial(
        user.id,
        height=170.0,
        google_sheet_url="https://docs.google.com/spreadsheets/d/1",
    )
    assert updated2 is not None
    assert updated2.name == "Alice"
    assert updated2.height == 170.0
    assert updated2.google_sheet_url == "https://docs.google.com/spreadsheets/d/1"
    assert updated2.is_setup_completed is True


def test_get_missing_profile_fields(mock_db_session):
    """get_missing_profile_fields returns required fields that are null/empty."""
    user = create_user(
        telegram_id=88888,
        name="Bob",
        weight=80.0,
        is_setup_completed=False,
    )
    missing = get_missing_profile_fields(user.id)
    assert "height" in missing
    assert "google_sheet_url" in missing
    assert "name" not in missing
    assert "weight" not in missing


def test_recompute_setup_completed(mock_db_session):
    """recompute_setup_completed sets is_setup_completed based on field completeness."""
    user = create_user(
        telegram_id=77777,
        is_setup_completed=False,
    )
    user = get_user_by_telegram_id(77777)
    user.name = "Charlie"
    user.weight = 70.0
    user.height = 175.0
    user.google_sheet_url = "https://sheet.example.com"
    update_user(user)

    result = recompute_setup_completed(user.id)
    assert result is True
    user2 = get_user_by_telegram_id(77777)
    assert user2.is_setup_completed is True


def test_create_and_get_user(mock_db_session):
    user = create_user(telegram_id=12345, name="John Doe", weight=80.5, height=180.0)
    assert user.id is not None
    assert user.telegram_id == 12345
    assert user.name == "John Doe"

    fetched_user = get_user_by_telegram_id(12345)
    assert fetched_user is not None
    assert fetched_user.id == user.id
    assert fetched_user.name == "John Doe"


def test_update_user(mock_db_session):
    user = create_user(telegram_id=54321, name="Jane Doe")
    user.weight = 65.0
    user.height = 170.0

    updated_user = update_user(user)
    assert updated_user.weight == 65.0
    assert updated_user.height == 170.0

    fetched_user = get_user_by_telegram_id(54321)
    assert fetched_user.weight == 65.0


def test_save_message(mock_db_session):
    user = create_user(telegram_id=111)

    msg = save_message(
        user_id=user.id, content="Hello bot", role="user", chat_context="private"
    )

    assert msg.id is not None
    assert msg.user_id == user.id
    assert msg.content == "Hello bot"
    assert msg.role == "user"
    assert msg.chat_context == "private"


def test_graph_state_operations(mock_db_session):
    user = create_user(telegram_id=222)

    state = update_graph_state(
        user_id=user.id,
        current_message="Test message",
        chat_history="[]",
        current_step="agent",
    )

    assert state.user_id == user.id
    assert state.current_message == "Test message"

    fetched_state = get_graph_state(user.id)
    assert fetched_state is not None
    assert fetched_state.current_message == "Test message"

    # Update existing
    updated_state = update_graph_state(
        user_id=user.id,
        current_message="New message",
        chat_history='[{"role": "user"}]',
        current_step="end",
    )

    assert updated_state.current_message == "New message"

    fetched_updated_state = get_graph_state(user.id)
    assert fetched_updated_state.current_message == "New message"
    assert fetched_updated_state.chat_history == '[{"role": "user"}]'
