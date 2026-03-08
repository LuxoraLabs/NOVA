# Implementation Plan: Short Informative Responses & TDD Migration

**Branch**: `003-short-informative-responses` | **Date**: 2026-03-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-short-informative-responses/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

This iteration enforces extreme brevity and high information density on the N.O.V.A bot's responses by updating the system prompt. Concurrently, it addresses two critical technical directives:
1. Hard-enforcing `pydantic-settings` to require API keys strictly from `.env` or environment variables without default fallbacks. Specifically, we will strictly use the standard names `OPENAI_API_KEY` for the LLM and `TELEGRAM_BOT_TOKEN` for the Telegram API.
2. Adopting a strict Test-Driven Development (TDD) methodology across the entire repository. This involves creating a comprehensive suite of tests (`pytest`) covering specifications 001, 002, and 003 before implementing new logic.

## Technical Context

**Language/Version**: Python 3.12+
**Primary Dependencies**: `typer`, `python-telegram-bot`, `langgraph`, `langchain-openai`, `pydantic-settings`, `rich`, `python-dotenv`, `sqlalchemy`, `pytest`
**Storage**: SQLite (via SQLAlchemy)
**Testing**: `pytest` with `pytest-asyncio` and `unittest.mock`
**Target Platform**: Any OS supporting Python 3.12+
**Project Type**: CLI Application / Telegram Bot
**Performance Goals**: Prompt brevity should reduce token generation time, speeding up overall response times.
**Constraints**: Zero hardcoded credentials. Tests must fail before code passes.
**Scale/Scope**: System prompt update, configuration hardening, and extensive retrofitting of testing infrastructure.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Typer CLI**: Passes. Unchanged.
- **Unified Logging**: Passes. Unchanged.
- **Code Quality**: Passes.
- **Testing & Methodology**: Passes. The new constitution mandate requires TDD; this plan is specifically engineered to introduce `pytest` across all existing components to meet the new requirement.

## Project Structure

### Documentation (this feature)

```text
specs/003-short-informative-responses/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── test-plan.md         # A holistic review of test specs for TDD migration
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
src/nova/
├── ... (Existing application code)
tests/
├── conftest.py          # Pytest fixtures and mock setups
├── unit/
│   ├── test_config.py   # Tests enforcing no-credential rules
│   ├── test_persona.py  # Tests LLM constraint parsing (mocked)
│   ├── test_db.py       # Tests SQLAlchemy logic (in-memory sqlite)
│   ├── test_onboarding.py # Tests User Onboarding flow (spec 001, US3)
│   ├── test_handlers.py # Tests private/group chat routing logic (spec 002, US1 & US2)
│   └── test_responses.py # Tests prompt updates for short responses (spec 003, US1)
```

**Structure Decision**: A dedicated `tests/` folder is scaffolded at the root directory alongside `src/` to house unit and integration tests. This folder maps directly to all logic established in specs 001, 002, and 003.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No complexity violations. TDD is fully aligned with the Constitution update.