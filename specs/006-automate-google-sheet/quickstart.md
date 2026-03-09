# Quickstart: Automate Google Sheet Setup

## Overview

This feature transforms the onboarding process by eliminating the need for the user to manually build out their gamified tracking spreadsheet. It introduces a Planner-based LangGraph agent that can invoke discrete tools, specifically a tool that connects to a user's blank Google Sheet via the `gspread` API and automatically formats it with the required "Dashboard" and "Daily Logs" tabs.

## Prerequisites

- You must have a GCP account with the Google Sheets API enabled and a Service Account JSON key (from the previous `005` sprint).
- The `gspread` library must be installed.

## Testing the Automated Setup Flow

1. Create a completely **blank** Google Sheet in your personal Google Drive. Ensure it only has the default "Sheet1" tab and no formatting.
2. Share this blank sheet with the email address of your bot's Google Service Account, granting it **Editor** access.
3. Start the bot locally (`nova`).
4. In Telegram, send the `/start` command to trigger the onboarding flow.
5. Provide your details as requested (Name, Weight, Height).
6. When prompted for the Google Sheet URL, provide the link to the completely blank sheet you created in step 1.
7. Observe the bot's response. It should invoke the planner, execute the sheet setup tool, verify success, and report back that your sheet has been initialized.
8. Open your blank Google Sheet. You should now see:
   - A "Dashboard" tab.
   - A "Daily Logs" tab with "Date" and "Weight (kg)" headers in cells A1 and B1.