# Implementation Plan: Group Onboarding & Gamified Health Dashboard Integration

**Branch**: `005-group-onboarding-prompt` | **Date**: 2026-03-08 | **Spec**: [Link to Spec](./spec.md)
**Input**: Feature specification from `/specs/005-group-onboarding-prompt/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

This feature resolves privacy issues by redirecting unregistered users in group chats to direct messages for onboarding. During the private onboarding flow, the bot collects a Google Sheets link to establish a "Gamified Dashboard." Daily metrics (like weight) are saved natively in the SQLite database (the single source of truth) and synchronized asynchronously to a "Daily Logs" tab in the user's Google Sheet, updating their visual dashboard.

## Technical Context

**Language/Version**: Python 3.12+
**Primary Dependencies**: `python-telegram-bot`, `langgraph`, `typer`, `gspread`, `google-auth`
**Storage**: SQLite (via SQLAlchemy)
**Testing**: `pytest`
**Target Platform**: CLI/Server
**Project Type**: CLI / Telegram Bot
**Performance Goals**: <2000ms response time for user commands
**Constraints**: Google Sheets is strictly write-only UI visualizer; SQLite is single source of truth; API failures must not crash the bot.
**Scale/Scope**: 1 Google Sheet mapping per user.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Python CLI / typer**: Yes, integrated via existing architecture.
- **Unified Logging**: Yes, we will use `get_logger(__name__)` for logging Google API sync status and errors instead of prints.
- **Strict TDD**: Yes, `pytest` tests will be written for onboarding redirects and Google Sheet sync service before implementation.
- **Code Quality**: Code will be formatted with Black, isorted, typed strictly, and linted with Ruff.

## Project Structure

### Documentation (this feature)

```text
specs/005-group-onboarding-prompt/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
src/
├── nova/
│   ├── bot/
│   │   ├── handlers.py     # Update to handle group chat vs private chat onboarding redirection
│   │   └── graph.py        # Update LangGraph to trigger Google Sheet sync
│   ├── core/
│   │   └── config.py       # Add Google Sheets API credentials config
│   ├── services/
│   │   └── sheets.py       # NEW: Dedicated service for Google Sheets API interactions (gspread)
│   └── database/
│       └── models.py       # Add new DailyMetric model and sheet URL to User profile

tests/
├── unit/
│   ├── test_handlers.py    # Tests for group chat redirections
│   └── test_sheets.py      # NEW: Tests for GoogleSheetsService (mocked API)
```

**Structure Decision**: A single project layout. The Google Sheets logic is extracted into a dedicated `services/sheets.py` file to maintain clean flow and readability, keeping API interactions decoupled from the core LangGraph logic and Telegram handlers.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
