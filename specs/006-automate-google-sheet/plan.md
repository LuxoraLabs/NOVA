# Implementation Plan: Automate Google Sheet Setup

**Branch**: `006-automate-google-sheet` | **Date**: 2026-03-09 | **Spec**: [Link to Spec](./spec.md)
**Input**: Feature specification from `/specs/006-automate-google-sheet/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

This feature significantly improves user onboarding by automating the Google Sheet setup process. Instead of forcing users to manually create tabs and columns, the user provides a blank sheet URL and API keys. A newly introduced Planner agent node will iteratively call a discrete `setup_google_sheet` tool to programmatically generate the "Dashboard" and "Daily Logs" tabs, populate headers, and handle any permission errors gracefully.

## Technical Context

**Language/Version**: Python 3.12+
**Primary Dependencies**: `langgraph`, `gspread`, `langchain-openai`
**Storage**: SQLite (via SQLAlchemy), Google Sheets API
**Testing**: `pytest` (mocked APIs)
**Target Platform**: CLI/Server
**Project Type**: CLI / Telegram Bot
**Performance Goals**: <10s for automated sheet formatting via API
**Constraints**: Tools must be single-purpose. The graph must support iterative tool calling, evaluating success/failure before returning to the user.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Python CLI / typer**: Yes.
- **Unified Logging**: Yes, using `get_logger(__name__)` for tracking tool execution and sheet setup steps.
- **Strict TDD**: Yes, tests will be written and ensure failure before implementing the LangGraph tools.
- **Code Quality / Modularity**: Tools will be divided into small, single-purpose functions in `src/nova/agent/tools/` as requested in the constitution update.
- **Testing Framework**: `pytest` will be used exclusively (no `uv` or `mypy` commands).
- **API Key Handling in Tests**: `@pytest.mark.skipif` will be used to bypass any tests needing live keys (though we will primarily rely on mocking `gspread`).

## Project Structure

### Documentation (this feature)

```text
specs/006-automate-google-sheet/
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
│   ├── agent/
│   │   ├── builder.py      # Refactor to use LangGraph's standard ToolNode pattern for iteration
│   │   ├── nodes/
│   │   │   ├── llm.py      # Refactor into the 'Planner' node
│   │   │   └── tools.py    # NEW: LangGraph ToolNode execution wrapper
│   │   └── tools/
│   │       ├── __init__.py
│   │       └── sheet_setup.py # NEW: Discrete tool for formatting the Google Sheet
│   └── services/
│       └── sheets.py       # Extend GoogleSheetsService with `initialize_sheet_structure`
│
tests/
├── unit/
│   ├── test_agent_tools.py # NEW: Test tool calling and Planner iteration
│   └── test_sheets.py      # Update with tests for `initialize_sheet_structure`
```

**Structure Decision**: The single project structure is maintained. LangGraph logic is expanded to separate the "Planner" from the "Tools" node. Tools are compartmentalized into a new `src/nova/agent/tools/` directory, adhering strictly to the modularity constraints defined in the Project Constitution.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
