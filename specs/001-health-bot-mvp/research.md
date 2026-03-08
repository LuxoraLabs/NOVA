# Phase 0: Research & Decisions

## Decision: Python CLI & Configuration
- **Decision**: Use `typer` for the main CLI entry point. Use TOML and environment variables for configuration management, exposing all settings via a single `get_settings()` accessor.
- **Rationale**: The user explicitly requested `typer` and an approach reading configuration globally (like API keys) through a single access point.
- **Alternatives considered**: Standard `argparse` or basic `sys.argv`. Discarded per user request to use `typer` and the constitution requirements.

## Decision: Unified Logging Strategy
- **Decision**: Use a centralized logging configuration as provided by the user. All output and debug info must route through a unified `get_logger(name)` function. `typer.echo`, `print()`, and direct `rich` printing are strictly forbidden.
- **Rationale**: Strict adherence to the `constitution.md` core principles and user instructions.
- **Alternatives considered**: Direct `print()` (explicitly disallowed by constitution).

## Decision: Database and Storage
- **Decision**: Use `sqlite3` to create a simple `.db` file containing tables for Users, Messages, and Graph States. 
- **Rationale**: The user requested a simple SQLite database file. This perfectly aligns with an MVP application and provides full local querying without deploying heavy infrastructure.
- **Alternatives considered**: PostgreSQL (too complex for MVP), JSON files (difficult to sync concurrently and query efficiently).

## Decision: Multi-channel Synchronization
- **Decision**: Store the unique Telegram User ID inside the `User` entity. Whether the message originates from a private DM or a group channel, the orchestrator retrieves the specific user's `GraphState` via their Telegram User ID.
- **Rationale**: Ensures the conversational memory is globally synced regardless of interaction context (private vs channel) as dictated by the spec.