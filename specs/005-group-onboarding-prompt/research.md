# Research: Gamified Dashboard & Google Sheets Integration

## 1. Google Sheets API Integration Library

**Decision**: Use `gspread` with `google-auth` and `google-auth-oauthlib`.

**Rationale**: `gspread` is a highly intuitive, Pythonic wrapper around the Google Sheets API. It specifically excels at row-based operations (like finding a row by date and updating it), which is exactly what we need for the "Daily Logs" tab. It handles authentication gracefully when combined with `google-auth` and can be wrapped in asynchronous functions or run in a background thread to prevent blocking the Telegram bot's event loop. It simplifies the API calls significantly compared to the raw `google-api-python-client`.

**Alternatives considered**: 
- `google-api-python-client`: The official Google client library. While powerful, it requires verbose JSON payloads for simple operations (like finding and updating a row) which decreases code readability.
- `aiogoogle`: An async wrapper, but less maintained than `gspread`. We can use `gspread.agspread` (async version of gspread) or run synchronous `gspread` in an executor.

## 2. Code Structure for Readability and Clean Flow

**Decision**: Split the Google Sheets functionality into dedicated service files away from the main bot handlers and LangGraph nodes.

**Rationale**: The user explicitly requested dividing into multiple files based on tasks. We will create a `services/` directory (or module) to contain external API interactions.
- `src/nova/services/sheets.py`: Contains the `GoogleSheetsService` class. Handles authentication, finding the user's sheet by ID/URL, verifying "Dashboard" and "Daily Logs" tabs exist, and appending/updating rows.
- `src/nova/core/state.py` or `src/nova/bot/graph.py`: The LangGraph node that triggers the background sync will call `GoogleSheetsService.sync_daily_log()`.
- `src/nova/bot/handlers.py`: Only handles Telegram message intake and onboarding routing.

**Alternatives considered**:
- Putting all logic into the LangGraph nodes directly: This would make the node functions extremely bloated and difficult to unit test. By extracting to a `services/sheets.py` module, we can mock the Google Sheets API easily during TDD.

## 3. Graceful Handling and Background Sync

**Decision**: The Google Sheets sync will be implemented as a non-blocking background task or async task within the LangGraph flow (or after the graph completes). It will use a try-except block to catch API errors (e.g., `gspread.exceptions.APIError`) and log them using the unified logging system, ensuring the bot never crashes and the SQLite transaction still commits successfully.

**Rationale**: The requirement states SQLite is the source of truth and Google Sheets is just a write-only UI visualizer. If the sync fails (e.g., rate limit, lost permissions), the system must not interrupt the user's chat experience.

**Alternatives considered**:
- Synchronous write during the request: Rejected because Google API latency could cause the Telegram bot to respond slowly, violating the performance constraint (<2000ms).