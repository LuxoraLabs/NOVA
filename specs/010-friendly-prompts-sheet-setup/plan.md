# Implementation Plan: Friendlier Prompts and Clear Google Sheet Setup

**Branch**: `010-friendly-prompts-sheet-setup` | **Date**: 2026-03-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification + user constraint: all user responses go to LLM; no manual field parsing; LLM handles everything; groups listen to /nova only.

## Summary

1. **Friendlier persona**: Update agent prompts (NOVA_SYSTEM_PROMPT, SETUP_MODE_PROMPT) to convey a warmer, more personable tone—a friendly health tracker—while keeping brevity.
2. **Clear sheet setup**: When the agent prompts for Google Sheet connection, inject step-by-step instructions (create sheet → share with service account → grant Editor → provide URL). Use `google_service_account_email` from settings when configured.
3. **Architectural constraint**: No manual message handling or field parsing. All user input flows to the LLM; the LLM reads history, infers intent, and calls tools. Groups: only `/nova` triggers the bot.

## Technical Context

**Language/Version**: Python 3.12+  
**Primary Dependencies**: `python-telegram-bot`, `langgraph`, `langchain-openai`  
**Storage**: SQLite (SQLAlchemy); no schema changes  
**Testing**: `pytest`  
**Target Platform**: Linux server  
**Project Type**: Telegram bot with LangGraph agent  
**Constraints**: Prompt-only changes; no new handlers or manual parsing. Service account email from `Settings.google_service_account_email`.  
**Scale/Scope**: Prompt updates; sheet instructions injected at runtime.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **TDD**: Tests before implementation (Pass—prompt tests verify expected content)
- **Modularity**: Prompts in persona module (Pass)
- **Logging**: `get_logger` (Pass)
- **Formatting**: Black, Ruff (Pass)

## Project Structure

### Documentation (this feature)

```text
specs/010-friendly-prompts-sheet-setup/
├── plan.md
├── research.md
├── quickstart.md
└── checklists/
    └── requirements.md
```

### Source Code (no new files)

```text
src/nova/
├── agent/
│   ├── persona.py         # NOVA_SYSTEM_PROMPT, SETUP_MODE_PROMPT
│   └── nodes/
│       └── llm.py         # Inject sheet instructions + email at runtime
└── utils/
    └── config.py          # Already has google_service_account_email
```

**Structure Decision**: Prompt edits only. Sheet instructions are built in `invoke_llm` when in setup mode, using `get_settings().google_service_account_email`.

## Design Decisions (from user input)

- **LLM handles everything**: No manual handlers for weight/height/units. The agent reads chat history, parses natural language, and calls `update_profile_field` with extracted values.
- **Groups: /nova only**: Free text in groups is ignored; only `/nova` triggers the bot. (Already enforced in 008/009; verify in tests.)
- **Sheet instructions**: Provided by the system prompt when the agent is about to ask for the sheet URL—injected into SETUP_MODE_PROMPT or passed as context so the LLM can relay them.

## Complexity Tracking

No violations.
