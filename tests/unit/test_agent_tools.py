import pytest
from unittest import mock
from nova.agent.tools.sheet_setup import setup_google_sheet
from nova.agent.tools.profile import (
    update_profile_field,
    get_profile_status,
    check_setup_complete,
)


@pytest.fixture
def mock_config():
    with mock.patch("nova.agent.tools.sheet_setup.get_settings") as mock_get:
        settings = mock.MagicMock()
        settings.google_application_credentials = '{"dummy": "json"}'
        mock_get.return_value = settings
        yield mock_get


def test_setup_google_sheet_success(mock_config):
    """Test successful initialization of Google Sheet."""
    with mock.patch(
        "nova.agent.tools.sheet_setup.GoogleSheetsService"
    ) as mock_service_class:
        mock_instance = mock.MagicMock()
        mock_instance.initialize_sheet_structure.return_value = (
            True,
            "Successfully initialized the N.O.V.A Data Vault structure.",
        )
        mock_service_class.return_value = mock_instance

        result = setup_google_sheet.invoke(
            {"sheet_url": "https://docs.google.com/spreadsheets/d/123/edit"}
        )

        assert "Successfully" in result
        mock_instance.initialize_sheet_structure.assert_called_once_with(
            "https://docs.google.com/spreadsheets/d/123/edit"
        )


def test_setup_google_sheet_failure(mock_config):
    """Test failed initialization of Google Sheet."""
    with mock.patch(
        "nova.agent.tools.sheet_setup.GoogleSheetsService"
    ) as mock_service_class:
        mock_instance = mock.MagicMock()
        mock_instance.initialize_sheet_structure.return_value = (
            False,
            "Failed to initialize sheet due to an API permissions error.",
        )
        mock_service_class.return_value = mock_instance

        result = setup_google_sheet.invoke(
            {"sheet_url": "https://docs.google.com/spreadsheets/d/123/edit"}
        )

        assert "Error: Failed to initialize sheet" in result


def test_setup_google_sheet_no_credentials():
    """Test behavior when no Google credentials are set."""
    with mock.patch("nova.agent.tools.sheet_setup.get_settings") as mock_get:
        settings = mock.MagicMock()
        settings.google_application_credentials = None
        mock_get.return_value = settings

        result = setup_google_sheet.invoke(
            {"sheet_url": "https://docs.google.com/spreadsheets/d/123/edit"}
        )

        assert "Error: Google Sheets credentials are not configured" in result


def test_update_profile_field_updates_and_recomputes():
    """update_profile_field updates provided fields and recomputes is_setup_completed."""
    with mock.patch(
        "nova.agent.tools.profile.update_user_profile_partial"
    ) as mock_update:
        mock_user = mock.MagicMock()
        mock_user.id = 1
        mock_user.is_setup_completed = False
        mock_update.return_value = mock_user

        result = update_profile_field.invoke(
            {"user_id": 1, "name": "Alice", "weight": 65.0}
        )

        mock_update.assert_called_once_with(1, name="Alice", weight=65.0)
        assert "Updated" in result or "updated" in result.lower()


def test_update_profile_field_profile_complete():
    """When all fields filled, is_setup_completed becomes True, returns ready message."""
    mock_user = mock.MagicMock()
    mock_user.id = 1
    mock_user.is_setup_completed = True

    with mock.patch(
        "nova.agent.tools.profile.update_user_profile_partial", return_value=mock_user
    ):
        result = update_profile_field.invoke(
            {
                "user_id": 1,
                "google_sheet_url": "https://docs.google.com/spreadsheets/d/1",
            }
        )

        assert "ready" in result.lower() or "complete" in result.lower()


def test_get_profile_status_returns_missing_fields():
    """get_profile_status returns structured summary with missing fields."""
    with (
        mock.patch("nova.agent.tools.profile.get_user_by_id") as mock_get_user,
        mock.patch(
            "nova.agent.tools.profile.get_missing_profile_fields",
            return_value=["weight", "height"],
        ),
    ):
        mock_user = mock.MagicMock()
        mock_get_user.return_value = mock_user
        result = get_profile_status.invoke({"user_id": 1})

        assert "weight" in result
        assert "height" in result


def test_check_setup_complete_complete():
    """check_setup_complete returns 'complete' when no fields missing."""
    with (
        mock.patch("nova.agent.tools.profile.get_user_by_id") as mock_get_user,
        mock.patch(
            "nova.agent.tools.profile.get_missing_profile_fields",
            return_value=[],
        ),
    ):
        mock_user = mock.MagicMock()
        mock_get_user.return_value = mock_user
        result = check_setup_complete.invoke({"user_id": 1})
        assert result == "complete"


def test_check_setup_complete_incomplete():
    """check_setup_complete returns missing fields when profile incomplete."""
    with (
        mock.patch("nova.agent.tools.profile.get_user_by_id") as mock_get_user,
        mock.patch(
            "nova.agent.tools.profile.get_missing_profile_fields",
            return_value=["name", "weight"],
        ),
    ):
        mock_user = mock.MagicMock()
        mock_get_user.return_value = mock_user
        result = check_setup_complete.invoke({"user_id": 1})
        assert "incomplete" in result
        assert "name" in result
        assert "weight" in result
