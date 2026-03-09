"""
Google Sheets API Service
"""

import base64
import json
import logging

import gspread
from google.oauth2.service_account import Credentials

logger = logging.getLogger(__name__)


class GoogleSheetsService:
    def __init__(self, credentials_json: str | None = None):
        """Initialize the Google Sheets service."""
        self.credentials_json = credentials_json
        self.client: gspread.Client | None = None
        self._authenticate()

    def _authenticate(self) -> None:
        """Authenticate with Google Sheets API."""
        if not self.credentials_json:
            logger.warning("No Google Sheets credentials provided.")
            return

        try:
            scopes = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive",
            ]

            # Check if it's base64 encoded or a valid JSON string
            try:
                creds_data = json.loads(self.credentials_json)
            except json.JSONDecodeError:
                # Try decoding base64
                decoded = base64.b64decode(self.credentials_json).decode("utf-8")
                creds_data = json.loads(decoded)

            creds = Credentials.from_service_account_info(creds_data, scopes=scopes)
            self.client = gspread.authorize(creds)
            logger.info("Successfully authenticated with Google Sheets API.")
        except Exception as e:
            logger.error(f"Failed to authenticate with Google Sheets: {e}")

    def verify_sheet_structure(self, sheet_url: str) -> bool:
        """Verify that the provided Google Sheet URL has the required structure."""
        if not self.client:
            logger.error("Not authenticated with Google Sheets API.")
            return False

        try:
            spreadsheet = self.client.open_by_url(sheet_url)
            worksheets = [ws.title for ws in spreadsheet.worksheets()]

            # Required tabs
            if "Dashboard" not in worksheets or "Daily Logs" not in worksheets:
                logger.warning(f"Sheet {sheet_url} is missing required tabs.")
                return False

            return True
        except Exception as e:
            logger.error(f"Failed to verify sheet structure for {sheet_url}: {e}")
            return False

    def sync_daily_log(self, sheet_url: str, date_str: str, weight: float) -> bool:
        """Sync a daily weight log to the 'Daily Logs' tab."""
        if not self.client:
            logger.error("Not authenticated with Google Sheets API.")
            return False

        try:
            spreadsheet = self.client.open_by_url(sheet_url)
            worksheet = spreadsheet.worksheet("Daily Logs")

            # Find the row for this date
            cell = worksheet.find(date_str)
            if cell:
                # If found, update the weight (column B, which is index 2)
                worksheet.update_cell(cell.row, 2, weight)
                logger.info(
                    f"Updated weight for {date_str} to {weight} in Google Sheet."
                )
            else:
                # If not found, append a new row
                worksheet.append_row([date_str, weight])
                logger.info(
                    f"Appended new weight log for {date_str}: {weight} in Google Sheet."
                )

            return True
        except Exception as e:
            logger.error(f"Failed to sync daily log to {sheet_url}: {e}")
            return False

    def initialize_sheet_structure(self, sheet_url: str) -> tuple[bool, str]:
        """Automatically create required tabs and headers for a blank sheet."""
        if not self.client:
            logger.error("Not authenticated with Google Sheets API.")
            return False, "Not authenticated with Google Sheets API."

        try:
            spreadsheet = self.client.open_by_url(sheet_url)
            worksheets = [ws.title for ws in spreadsheet.worksheets()]

            # Check for existing required tabs
            if "Dashboard" in worksheets or "Daily Logs" in worksheets:
                logger.warning(f"Sheet {sheet_url} already has required tabs.")
                return (
                    False,
                    "Tabs 'Dashboard' or 'Daily Logs' already exist. Please provide a completely blank sheet to avoid overwriting your data.",
                )

            # Create Dashboard tab
            spreadsheet.add_worksheet(title="Dashboard", rows=100, cols=20)
            logger.info("Created Dashboard tab.")

            # Create Daily Logs tab and format headers
            daily_logs = spreadsheet.add_worksheet(
                title="Daily Logs", rows=1000, cols=10
            )
            daily_logs.update([["Date", "Weight (kg)"]], "A1:B1")
            logger.info("Created Daily Logs tab and initialized headers.")

            return True, "Successfully initialized the N.O.V.A Data Vault structure."

        except gspread.exceptions.APIError as e:
            logger.error(f"API Error during sheet initialization: {e}")
            return (
                False,
                "Failed to initialize sheet due to an API permissions error. Please ensure the sheet is shared with the bot's service account as an Editor.",
            )
        except Exception as e:
            logger.error(f"Failed to initialize sheet structure for {sheet_url}: {e}")
            return False, f"Failed to setup the sheet: {str(e)}"
