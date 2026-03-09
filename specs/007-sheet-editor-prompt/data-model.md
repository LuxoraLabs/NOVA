# Data Model: Google Sheet Service Account Prompt

## Configuration Changes

The existing application configuration model will be extended to include the new service account email.

### `Settings` (pydantic-settings model in `src/nova/utils/config.py`)

**New Field:**
- `google_service_account_email`: `str | None`
  - **Description**: The email address for the Google Service Account used to access user sheets.
  - **Default**: `None`
  - **Environment Variable**: `GOOGLE_SERVICE_ACCOUNT_EMAIL`
  - **Purpose**: Used to instruct users which email they need to invite as an "Editor" to their Google Sheet during the setup phase.
