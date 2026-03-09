import pytest
from unittest import mock
from nova.agent.tools.sheet_setup import setup_google_sheet


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
