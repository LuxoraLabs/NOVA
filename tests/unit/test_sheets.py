import json
import os
import tempfile

import pytest
from unittest import mock
from nova.services.sheets import GoogleSheetsService, _load_credentials


def test_load_credentials_from_file_path():
    """Credentials can be loaded from a file path (fixes UTF-8 decode error)."""
    creds = {"type": "service_account", "project_id": "test", "private_key_id": "x"}
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    ) as f:
        json.dump(creds, f)
        path = f.name
    try:
        result = _load_credentials(path)
        assert result == creds
    finally:
        os.unlink(path)


@pytest.fixture
def mock_service():
    with mock.patch("nova.services.sheets.GoogleSheetsService._authenticate"):
        service = GoogleSheetsService('{"dummy": "json"}')
        service.client = mock.MagicMock()
        return service


def test_verify_sheet_structure_success(mock_service):
    """Test that a sheet with the correct structure passes verification."""
    mock_spreadsheet = mock.MagicMock()

    mock_dashboard = mock.MagicMock()
    mock_dashboard.title = "Dashboard"

    mock_daily_logs = mock.MagicMock()
    mock_daily_logs.title = "Daily Logs"

    mock_spreadsheet.worksheets.return_value = [mock_dashboard, mock_daily_logs]
    mock_service.client.open_by_url.return_value = mock_spreadsheet

    result = mock_service.verify_sheet_structure(
        "https://docs.google.com/spreadsheets/d/123/edit"
    )

    assert result is True
    mock_service.client.open_by_url.assert_called_once_with(
        "https://docs.google.com/spreadsheets/d/123/edit"
    )


def test_verify_sheet_structure_missing_tabs(mock_service):
    """Test that missing required tabs fails verification."""
    mock_spreadsheet = mock.MagicMock()

    mock_dashboard = mock.MagicMock()
    mock_dashboard.title = "Wrong Tab"

    mock_spreadsheet.worksheets.return_value = [mock_dashboard]
    mock_service.client.open_by_url.return_value = mock_spreadsheet

    result = mock_service.verify_sheet_structure(
        "https://docs.google.com/spreadsheets/d/123/edit"
    )

    assert result is False


def test_verify_sheet_structure_invalid_url(mock_service):
    """Test that an invalid URL returns False."""

    mock_service.client.open_by_url.side_effect = Exception("Not found")

    result = mock_service.verify_sheet_structure("invalid_url")
    assert result is False


def test_sync_daily_log(mock_service):
    """Test syncing a daily log to the Google Sheet."""
    mock_spreadsheet = mock.MagicMock()
    mock_worksheet = mock.MagicMock()

    # Return cell object when finding date
    mock_cell = mock.MagicMock()
    mock_cell.row = 2
    mock_worksheet.find.return_value = mock_cell

    mock_spreadsheet.worksheet.return_value = mock_worksheet
    mock_service.client.open_by_url.return_value = mock_spreadsheet

    result = mock_service.sync_daily_log(
        "https://docs.google.com/spreadsheets/d/123/edit", "2026-03-08", 74.5
    )

    assert result is True
    # Should update cell in column B (Weight) on the found row
    mock_worksheet.update_cell.assert_called_once_with(2, 2, 74.5)


def test_sync_daily_log_new_row(mock_service):
    """Test syncing a daily log when date doesn't exist."""
    mock_spreadsheet = mock.MagicMock()
    mock_worksheet = mock.MagicMock()

    # Simulate date not found
    mock_worksheet.find.return_value = None

    mock_spreadsheet.worksheet.return_value = mock_worksheet
    mock_service.client.open_by_url.return_value = mock_spreadsheet

    result = mock_service.sync_daily_log(
        "https://docs.google.com/spreadsheets/d/123/edit", "2026-03-09", 75.0
    )

    assert result is True
    # Should append a new row
    mock_worksheet.append_row.assert_called_once_with(["2026-03-09", 75.0])


def test_initialize_sheet_structure(mock_service):
    """Test initializing a completely blank sheet."""
    mock_spreadsheet = mock.MagicMock()
    mock_service.client.open_by_url.return_value = mock_spreadsheet

    # Simulate an empty sheet with just "Sheet1"
    mock_sheet1 = mock.MagicMock()
    mock_sheet1.title = "Sheet1"
    mock_spreadsheet.worksheets.return_value = [mock_sheet1]

    # Mock add_worksheet
    mock_dashboard = mock.MagicMock()
    mock_daily_logs = mock.MagicMock()

    def add_worksheet_side_effect(title, *args, **kwargs):
        if title == "Dashboard":
            return mock_dashboard
        elif title == "Daily Logs":
            return mock_daily_logs
        return mock.MagicMock()

    mock_spreadsheet.add_worksheet.side_effect = add_worksheet_side_effect

    success, message = mock_service.initialize_sheet_structure(
        "https://docs.google.com/spreadsheets/d/123/edit"
    )

    assert success is True
    assert "successfully" in message.lower()

    # Verify Dashboard was created
    mock_spreadsheet.add_worksheet.assert_any_call(title="Dashboard", rows=100, cols=20)

    # Verify Daily Logs was created and formatted
    mock_spreadsheet.add_worksheet.assert_any_call(
        title="Daily Logs", rows=1000, cols=10
    )
    mock_daily_logs.update.assert_called_once_with([["Date", "Weight (kg)"]], "A1:B1")


def test_initialize_sheet_structure_already_exists(mock_service):
    """Test initializing a sheet that already has the required tabs."""
    mock_spreadsheet = mock.MagicMock()
    mock_service.client.open_by_url.return_value = mock_spreadsheet

    mock_dashboard = mock.MagicMock()
    mock_dashboard.title = "Dashboard"
    mock_daily_logs = mock.MagicMock()
    mock_daily_logs.title = "Daily Logs"

    mock_spreadsheet.worksheets.return_value = [mock_dashboard, mock_daily_logs]

    success, message = mock_service.initialize_sheet_structure(
        "https://docs.google.com/spreadsheets/d/123/edit"
    )

    # Should fail safely because the tabs already exist
    assert success is False
    assert "already exist" in message.lower()
    mock_spreadsheet.add_worksheet.assert_not_called()
