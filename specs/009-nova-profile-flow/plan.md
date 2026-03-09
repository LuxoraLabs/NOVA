# Implementation Plan: AI-Driven Profile Setup + Nova Flow

**Branch**: `009-nova-profile-flow` | **Date**: 2026-03-09 | **Spec**: [spec.md](./spec.md)
**Input**: 009 spec + AI-driven profile completion with `is_setup_completed`, agent tools, and flexible field updates

## Summary

1. **009 flow**: First-time private → inline setup; first-time group `/nova` → in-group notice + DM setup; groups = `/nova` only.
2. **AI-driven profile**: Add `is_setup_completed` to User; replace rigid ConversationHandler with LangGraph agent that parses messages, calls tools to update profile fields, checks completeness, asks for missing fields, and responds "you are ready to use" when done.

## Technical Context

**Language/Version**: Python 3.12+  
**Primary Dependencies**: `python-telegram-bot`, `langgraph`, `langchain-openai`, `sqlalchemy`  
**Storage**: SQLite (SQLAlchemy)  
**Testing**: `pytest`  
**Target Platform**: Linux server  
**Project Type**: Telegram Bot with LangGraph agent  
**Constraints**: Profile updates must be atomic; tools must be idempotent where possible.  
**Scale/Scope**: User model + migration; new agent tools; onboarding flow refactor.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **TDD**: Tests before implementation (Pass)
- **Modularity**: Tools in dedicated modules (Pass)
- **Logging**: `get_logger` (Pass)
- **Formatting**: Black, Ruff (Pass)

## Project Structure

### Source Code

```text
src/nova/
├── database/
│   ├── models.py         # Add is_setup_completed, optional goals
│   └── repository.py     # update_user_profile_partial(), get_missing_fields()
├── agent/
│   ├── tools/
│   │   ├── profile.py    # update_profile_field, get_profile_status
│   │   └── ...
│   └── builder.py        # Wire profile tools for users with is_setup_completed=False
└── bot/
    └── handlers/         # Route setup-incomplete users to agent (no ConversationHandler)
```

## Design Decisions (from user input)

- **is_setup_completed**: Boolean on User; `True` only when all required fields (name, weight, height, google_sheet_url) are non-null.
- **Field updates**: AI parses messages and calls tools; support multi-field updates in one message.
- **Missing fields**: Agent checks profile, asks for missing fields, continues until complete.
- **Completion message**: "You are ready to use" or similar when `is_setup_completed` becomes true.

## Complexity Tracking

No violations.
