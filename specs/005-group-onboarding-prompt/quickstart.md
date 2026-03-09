# Quickstart: Gamified Dashboard Integration

## Overview

This feature integrates a write-only Google Sheet dashboard that acts as a gamified health tracker UI for the user. It also modifies the onboarding flow to correctly handle group chats (redirecting to DMs) and securely collect Google Sheets credentials during private onboarding.

## Prerequisites

- You need a Google Cloud Platform account with the **Google Sheets API** and **Google Drive API** enabled.
- You must generate a Service Account JSON key or OAuth 2.0 Client credentials to authenticate the bot with Google APIs.
- Set the credentials in your `.env` file (e.g., `GOOGLE_APPLICATION_CREDENTIALS=path/to/service_account.json` or as a base64 encoded string).

## Setup Steps

1. **Install new dependencies:**
   ```bash
   poetry add gspread google-auth
   ```
2. **Apply Database Changes:**
   Ensure Alembic or your SQLite schema scripts are updated to add the new `google_sheet_url` to the `users` table and to create the new `daily_metrics` table.
3. **Template Sheet Creation:**
   Create a master Google Sheet template containing:
   - A `Dashboard` tab (with charts).
   - A `Daily Logs` tab (Columns: Date, Weight).
   Make this template accessible so new users can duplicate it and link it to the bot.

## Testing

1. Start the bot locally.
2. In a Telegram group chat, type `/nova hello`. You should receive a prompt to DM the bot.
3. In a DM, send `/start` to begin onboarding. Provide your name, weight, height, and the URL/ID of your duplicated Google Sheet.
4. After onboarding, message the bot: "Today I weigh 74.5 kg."
5. Check your Google Sheet's `Daily Logs` tab. A new row for today's date should appear with the value `74.5`, automatically updating your `Dashboard` charts.