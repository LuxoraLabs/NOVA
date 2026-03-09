# Data Model: Automate Google Sheet Setup

*Note: This feature builds upon the existing database models (`users`, `daily_metrics`) and primarily focuses on augmenting the existing Google Sheets "Write-Only" schema via API automation.*

## SQLite Database Entities

No new SQLite models are required for this feature. We will continue utilizing the existing `User` model, specifically the `google_sheet_url` and `google_sheet_credentials` fields which were added in the previous iteration.

## LangGraph State Representation

The orchestration state (`AgentState`) will need to be capable of handling tool invocations, tracking the current step in the plan, and recording tool execution outputs.

- **`chat_history`**: (List of Messages) Must support `AIMessage` containing `tool_calls` and `ToolMessage` containing the result of the tool execution, allowing the Planner node to evaluate the outcome of the automated setup step.

## Google Sheets Target Schema (Automated Creation)

When the automated setup tool is executed, it guarantees the creation of the following layout in the user's provided sheet:

### Worksheet 1: "Dashboard"
- **Properties**: Created empty if it does not exist. (Users will customize their own charts here based on the data in the Daily Logs tab).
- **Tool Action**: `add_worksheet(title="Dashboard", rows=100, cols=20)`

### Worksheet 2: "Daily Logs"
- **Properties**: Created if it does not exist.
- **Headers**: Populated automatically upon creation.
  - Row 1, Column A: `Date`
  - Row 1, Column B: `Weight (kg)`
- **Tool Action**: `add_worksheet(title="Daily Logs")` followed by `update("A1:B1", [["Date", "Weight (kg)"]])`