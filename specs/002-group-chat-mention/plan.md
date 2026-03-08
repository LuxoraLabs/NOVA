# Implementation Plan: Group Chat Mention Requirement & Refactoring

**Branch**: `002-group-chat-mention` | **Date**: 2026-03-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-group-chat-mention/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

This feature enforces explicit @mentions for bot responses in group chats to prevent spam, while leaving private direct messages unaffected. Alongside this functionality, significant architectural refactoring is required based on user instruction:
1. Shift from `uv` back to standard `pip install -e .` using a clean `pyproject.toml` definition.
2. Refactor the LangGraph agent logic into multiple specialized files (builder, orchestrator, state) and folders (nodes, tools).
3. Introduce `SQLAlchemy` for ORM-based database operations, replacing raw SQLite commands.
4. Enhance `config.py` to strictly load via `python-dotenv`.
5. Prune all unused dependencies and `.mypy_cache`.

## Technical Context

**Language/Version**: Python 3.12+ (latest)
**Primary Dependencies**: `typer`, `python-telegram-bot`, `langgraph`, `langchain-openai`, `pydantic-settings`, `rich`, `python-dotenv`, `sqlalchemy` (NEW)
**Storage**: SQLite (via SQLAlchemy)
**Testing**: `pytest`
**Target Platform**: Any OS supporting Python 3.12+
**Project Type**: CLI Application / Telegram Bot
**Performance Goals**: Fast response routing (<5s) with 0 API requests on ignored group chat messages.
**Constraints**: Avoid `mypycache`, avoid `uv`, keep lightweight.
**Scale/Scope**: Group chat interaction filtering and internal refactoring.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Typer CLI**: Passes. We retain Typer.
- **Unified Logging**: Passes. All structural updates will continue to utilize `get_logger()`.
- **Code Quality**: Passes. Refactoring improves structure. We will ensure Black/isort remain active but without heavy `.mypy_cache`.
- **Simplicity**: Passes. Transitioning to SQLAlchemy models and breaking down large files aligns with the modularity principle.

## Project Structure

### Documentation (this feature)

```text
specs/002-group-chat-mention/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
src/nova/
├── cli.py               
├── bot/
│   ├── handlers.py      # Updated to filter mentions based on chat context
│   └── platform.py      
├── agent/
│   ├── builder.py       # (NEW) Defines and compiles the StateGraph
│   ├── orchestrator.py  # (NEW) Runs the graph and processes messages
│   ├── state.py         # (NEW) Defines AgentState and serialization
│   ├── persona.py       
│   ├── nodes/           # (NEW FOLDER) Contains execution nodes
│   │   └── llm.py       # (NEW) The LLM invoker node
│   └── tools/           # (NEW FOLDER) Contains tool definitions
├── database/
│   ├── db.py            # Updated to initialize SQLAlchemy engines
│   ├── models.py        # (NEW) SQLAlchemy declarative bases
│   └── repository.py    # Updated to use SQLAlchemy sessions
├── utils/
│   ├── config.py        # Updated to leverage python-dotenv
│   └── logging.py       
└── models/
    └── domain.py        # Migrated mostly to database/models.py, kept for pure schemas if needed
```

**Structure Decision**: The agent architecture is being intentionally fractured into `builder.py`, `orchestrator.py`, `state.py`, `nodes/`, and `tools/` as requested. The database layer adopts `SQLAlchemy` necessitating a new `models.py` file.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| SQLAlchemy introduction | Explicitly requested by user. | Raw SQLite is simpler but user specifically requested ORM. |
| Multi-file Agent Splitting | Explicitly requested by user. | Single file is simpler but user specifically requested file separation for clarity. |
