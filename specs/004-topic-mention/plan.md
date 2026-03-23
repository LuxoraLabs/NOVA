# Implementation Plan: Topic Mention Response Support

**Branch**: `004-topic-mention` | **Date**: 2026-03-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-topic-mention/spec.md`

## Summary

This feature updates the message routing logic to support Telegram Group Topics. It ensures that when the bot is explicitly mentioned in a topic (thread), the system detects the `message_thread_id` and uses it to route the response back to that exact topic. Additionally, we will enhance the unified logging to output debug-level trace logs whenever a message is parsed, a mention is detected, or a response is sent.

## Technical Context

**Language/Version**: Python 3.12+  
**Primary Dependencies**: `python-telegram-bot`, `typer`  
**Storage**: SQLite (via SQLAlchemy) - No schema changes required  
**Testing**: `pytest` with `pytest-asyncio` and `unittest.mock`  
**Target Platform**: Any OS supporting Python 3.12+
**Project Type**: CLI Application / Telegram Bot  
**Performance Goals**: N/A (Standard Telegram API latency)  
**Constraints**: Zero hardcoded credentials. Maintain single unified profile context.  
**Scale/Scope**: Local routing updates within Telegram bot handlers.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Typer CLI**: Passes. Unchanged.
- **Unified Logging**: Passes. The new debug logs will explicitly use the `get_logger(__name__)` pattern instead of print statements.
- **Code Quality**: Passes.
- **Testing & Methodology**: Passes. Test-Driven Development (TDD) will be enforced. We will update `tests/unit/test_handlers.py` to assert the `message_thread_id` is passed correctly before modifying `handlers.py`.

## Project Structure

### Documentation (this feature)

```text
specs/004-topic-mention/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
src/nova/
├── bot/
│   └── handlers.py      # Core changes: thread routing and debug logging
tests/
└── unit/
    └── test_handlers.py # Test updates for thread routing assertions
```

**Structure Decision**: We will stick to the existing project structure and modify `handlers.py` to inspect `update.message.message_thread_id` and pass it down to `send_message`.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No complexity violations. The updates cleanly map to the existing architecture.