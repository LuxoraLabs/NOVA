# Data Model: Gamified Dashboard Integration

## SQLite Source of Truth (Database Entities)

### 1. User Profile (`users` table)
Represents the registered user in the SQLite database. We need to add fields to store Google Sheets configurations securely.
- `id` (Integer, Primary Key)
- `telegram_id` (Integer, Unique)
- `name` (String)
- `weight` (Float) - Initial weight
- `height` (Float)
- `google_sheet_url` (String, Nullable) - The URL or ID of the user's dashboard sheet.
- `google_sheet_credentials` (String, Nullable) - OAuth tokens or access permissions (or service account linkage details).

### 2. Daily Metric (`daily_metrics` table)
Stores the raw daily statistics reported by the user. This is the source of truth that will be synced to the Google Sheet.
- `id` (Integer, Primary Key)
- `user_id` (Integer, Foreign Key to `users.id`)
- `date` (Date) - The calendar date of the metric (e.g., 2026-03-08)
- `metric_type` (String) - E.g., "weight", "calories", "water"
- `value` (Float) - The numerical value (e.g., 74.0)
- `created_at` (DateTime)
- `updated_at` (DateTime)

*Constraint*: A unique index or constraint on `(user_id, date, metric_type)` ensures that if the user updates their weight for today, we overwrite the existing row rather than creating duplicates.

---

## Google Sheets "Write-Only" Schema (UI Visualizer)

This is the required structure of the user's Google Sheet. The bot will expect these tabs to exist and will write to them.

### Tab 1: "Dashboard"
- **Purpose**: A visual landing page. Contains graphs, charts, and summary statistics.
- **Bot Interaction**: The bot DOES NOT write directly to this tab. This tab uses Google Sheets formulas (e.g., `=AVERAGE('Daily Logs'!B:B)`) and Charts referencing the "Daily Logs" tab.

### Tab 2: "Daily Logs"
- **Purpose**: Time-series raw data table.
- **Bot Interaction**: The bot appends or updates rows here.
- **Columns (Header Row)**:
  - `A: Date` (Format: YYYY-MM-DD)
  - `B: Weight (kg)`
  - `C: Notes` (Optional, if LLM extracts context)
- **Logic**: 
  - Find row by `Date`.
  - If exists -> Update column `B` with the new weight.
  - If not exists -> Append a new row with `Date` and `Weight`.