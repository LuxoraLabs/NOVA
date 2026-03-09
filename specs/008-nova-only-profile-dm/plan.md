# Implementation Plan: Nova-Only Commands + Modular Telegram Handlers

**Branch**: `008-nova-only-profile-dm` | **Date**: 2026-03-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification + handler modularization for readability

## Summary

1. **Feature**: Remove `/start`; use `/nova` only for groups/channels/topics; direct messages in private; unregistered users get DM with profile setup trigger.
2. **Refactor**: Split `handlers.py` into dedicated modules by responsibility for better readability.

## Technical Context

**Language/Version**: Python 3.12+  
**Primary Dependencies**: `python-telegram-bot`, `langgraph`, `pydantic-settings`  
**Storage**: SQLite (SQLAlchemy)  
**Testing**: `pytest`  
**Target Platform**: Linux server  
**Project Type**: Telegram Bot  
**Constraints**: Handler split must not change external behavior; registration must occur in private only.  
**Scale/Scope**: One handler package with 4–5 modules (~100–150 lines each vs ~315 lines in a single file).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Modularity** (Constitution §4): Split long scripts into smaller ones—handler split directly addresses this.
- **CLI/Bot**: Typer + python-telegram-bot (Pass)
- **Logging**: `get_logger` (Pass)
- **Formatting**: Black, isort, Ruff (Pass)
- **TDD**: pytest (Pass)

## Project Structure

### Documentation (this feature)

```text
specs/008-nova-only-profile-dm/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── contracts/
```

### Source Code – Handler Package Layout

```text
src/nova/bot/
├── __init__.py
├── platform.py              # (unchanged)
├── handlers/
│   ├── __init__.py          # register_handlers(), re-exports
│   ├── core.py              # _process_and_reply (shared logic)
│   ├── onboarding.py        # start_command, handle_name, weight, height, sheet_url, cancel
│   ├── nova.py              # handle_nova_command
│   ├── text.py              # handle_text_message (direct messages in private)
│   └── fallback.py           # handle_non_text_message
```

**Structure Decision**: Use a `handlers/` package. Each module has a single responsibility. `core.py` holds shared message-processing logic used by `nova.py` and `text.py`.

## Handler Module Responsibilities

| Module        | Handlers                          | Purpose                                |
|---------------|-----------------------------------|----------------------------------------|
| `onboarding.py` | start_command, handle_name, handle_weight, handle_height, handle_sheet_url, cancel_onboarding | Profile setup flow (DM-only after 008) |
| `nova.py`    | handle_nova_command               | `/nova` command in any context        |
| `text.py`    | handle_text_message               | Direct messages in private chat only   |
| `fallback.py`| handle_non_text_message           | Non-text message fallback              |
| `core.py`    | _process_and_reply                | Shared: DB lookup, LangGraph, reply    |

## Complexity Tracking

No violations.
