from langchain_core.tools import tool

from nova.services.sheets import GoogleSheetsService
from nova.utils.config import get_settings
from nova.utils.logging import get_logger

logger = get_logger(__name__)


@tool
def setup_google_sheet(sheet_url: str) -> str:
    """Automates the setup of a Google Sheet by creating necessary tabs ("Dashboard" and "Daily Logs") and headers.
    Use this tool whenever a user provides a new blank Google Sheet URL to initialize their Data Vault.
    Returns a success message or an error description.
    """
    logger.info(f"Setting up Google Sheet: {sheet_url}")
    settings = get_settings()

    if not settings.google_application_credentials:
        error_msg = "Error: Google Sheets credentials are not configured in the system."
        logger.error(error_msg)
        return error_msg

    try:
        sheets_service = GoogleSheetsService(settings.google_application_credentials)
        success, message = sheets_service.initialize_sheet_structure(sheet_url)

        if success:
            return message
        else:
            return f"Error: {message}"
    except Exception as e:
        logger.error(f"Unexpected error in setup_google_sheet tool: {e}")
        return f"Error: An unexpected system error occurred: {str(e)}"
