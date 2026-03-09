# Quickstart: Friendlier Prompts and Clear Google Sheet Setup

## What Changed

1. **Persona**: Agent prompts are warmer and more supportive—"Let's get to know you!" style for setup, encouraging tone for tracking.
2. **Sheet setup**: When the agent asks for a Google Sheet URL, it provides step-by-step instructions: create a blank sheet, share with the service account as Editor, paste the URL. The service account email (when configured in `GOOGLE_SERVICE_ACCOUNT_EMAIL`) is included explicitly.

## Verification

1. **Persona**: Start a new user flow in private chat. Verify setup prompts feel warm (e.g., "Let's get to know you! What's your name?").
2. **Sheet instructions**: Reach the sheet URL step. Verify instructions are numbered, include the service account email when `GOOGLE_SERVICE_ACCOUNT_EMAIL` is set, and describe Share → Editor.
3. **Groups**: In a group, send free text—no reply. Send `/nova hello`—bot replies. Confirms groups listen to /nova only.
