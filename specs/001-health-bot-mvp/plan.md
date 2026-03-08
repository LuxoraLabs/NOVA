# Implementation Plan: N.O.V.A. MVP Comm Link

**Branch**: `001-health-bot-mvp` | **Date**: 2026-03-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-health-bot-mvp/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Establish a bidirectional text pipeline between Telegram, LangGraph, and a text-only LLM. We will build a CLI entrypoint using `typer`, implement a global unified logging strategy via `get_logger`, parse all global settings (including API keys) from TOML/ENV variables via a `get_settings` accessor, and use a simple `sqlite3` database file to persist Users, Messages, and their conversational `GraphState`.

## Technical Context

**Language/Version**: Python 3.12+ (latest)
**Primary Dependencies**: `typer` (CLI), `python-telegram-bot` (Telegram API), `langgraph` & `langchain` (LLM Orchestration), `rich` (Console), `pydantic-settings` / `tomllib` (Configuration), `sqlite3` (Database)
**Storage**: SQLite (simple `.db` file)
**Testing**: `pytest`
**Target Platform**: Any OS supporting Python 3.12+
**Project Type**: CLI Application / Long-running Telegram Bot Service
**Performance Goals**: Fast response routing (<5s as per spec)
**Constraints**: Requires unified user profile syncing regardless of message origin (Private DM vs. Channel). No framework-level standard `print()` allowed.
**Scale/Scope**: MVP Foundation for MVP Comm Link.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Typer CLI**: Passes. The main entry point will be structured using `typer.Typer()`.
- **Unified Logging**: Passes. Completely restricted to using `setup_unified_logging` and `get_logger` for all operations. Native `print()` and `typer.echo()` are banned.
- **Code Quality**: Passes. Black (88 character limit), isort, MyPy (strict), and Ruff will be enforced. Strict PEP 8 and docstrings are mandatory.
- **Simplicity**: Passes. The use of a simple SQLite `.db` file prevents complex database deployments for an MVP.

## Project Structure

### Documentation (this feature)

```text
specs/001-health-bot-mvp/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
src/nova/
├── cli.py               # Typer CLI entry point and setup
├── bot/
│   ├── handlers.py      # Telegram bot message routing
│   └── platform.py      # Core Telegram platform logic
├── agent/
│   ├── graph.py         # LangGraph conversational orchestrator
│   └── persona.py       # Core prompts & N.O.V.A persona enforcement
├── database/
│   ├── db.py            # SQLite connection pool and init
│   └── repository.py    # Queries for User, Message, GraphState
├── utils/
│   ├── config.py        # Central configuration (get_settings)
│   └── logging.py       # Unified logging (get_logger)
└── models/
    └── domain.py        # Shared data entities / Pydantic models
```

**Structure Decision**: A modular, single-project layout under a primary Python namespace (`src/nova`). It logically separates configuration/utils, bot interface, AI reasoning (agent), and data persistence (database).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No complexity violations. The simple SQLite approach and direct CLI structure directly align with constitution principles.