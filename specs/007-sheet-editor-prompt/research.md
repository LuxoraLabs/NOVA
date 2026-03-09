# Research: Google Sheet Service Account Prompt

## Configuration Management

**Decision**: Add `google_service_account_email` to the existing `Settings` model in `src/nova/utils/config.py`.
**Rationale**: The user specifically requested a new field for the Google service user under settings to be read from the environment variable. Using `pydantic-settings` is consistent with the project's existing configuration approach.
**Alternatives considered**: 
- Extracting `client_email` directly from the `credentials.json` file. Rejected because the explicit environment variable approach gives more control and directly fulfills the user's request.

## Prompt Modification

**Decision**: Update the message template inside the bot handlers that instructs the user to configure their Google Sheet.
**Rationale**: The instruction must be clear and direct users to share the sheet with the specific email as an "Editor". If the email is missing from the configuration, it will fallback to a generic message without the explicit email.
**Alternatives considered**: N/A - directly addresses the feature requirement.
