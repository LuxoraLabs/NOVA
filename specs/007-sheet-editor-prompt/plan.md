# Implementation Plan: Google Sheet Service Account Prompt

**Branch**: `007-sheet-editor-prompt` | **Date**: 2026-03-09 | **Spec**: [link](./spec.md)
**Input**: Feature specification from `/specs/007-sheet-editor-prompt/spec.md`

## Summary

Update the Google Sheet setup onboarding prompt to include the specific Google Service Account email that the user needs to add as an "Editor". The email will be retrieved from the application's configuration settings (read from an environment variable).

## Technical Context

**Language/Version**: Python 3.12+  
**Primary Dependencies**: `python-telegram-bot`, `pydantic-settings`  
**Storage**: N/A  
**Testing**: `pytest`  
**Target Platform**: Linux server / Docker  
**Project Type**: Telegram Bot  
**Performance Goals**: N/A  
**Constraints**: Fallback gracefully to generic instructions if the service account email is not configured.  
**Scale/Scope**: Updating one configuration model (`config.py`) and one prompt string (`handlers.py`).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **CLI/Bot Framework**: Built with Telegram Bot and Typer (Pass)
- **Unified Logging**: Uses existing logger (Pass)
- **Formatting**: Adheres to Black/isort and PEP 8 (Pass)
- **Type Hinting**: Fully typed with `pydantic-settings` (Pass)
- **Testing**: Using `pytest` and following TDD (Pass)

## Project Structure

### Documentation (this feature)

```text
specs/007-sheet-editor-prompt/
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
│   │   └── handlers.py  # Contains the onboarding prompt
│   └── utils/
│       └── config.py    # Settings model to add the service account email
tests/
└── unit/
    └── test_handlers.py # Update tests for the prompt logic
```

**Structure Decision**: Using existing project structure, modifying specific configuration and handler files.

## Complexity Tracking

No violations found.
