# Tasks: Short Informative Responses & TDD Migration

**Input**: Design documents from `/specs/003-short-informative-responses/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, test-plan.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/` and `tests/` at repository root

---

## Phase 1: Setup (Test Infrastructure)

**Purpose**: Project initialization and configuring `pytest` environments.

- [x] T001 Update `pyproject.toml` to include `pytest-asyncio` as a dependency and configure `pytest` standard behaviors.
- [x] T002 [P] Create `tests/conftest.py` with standard mocked environments (e.g., mocked SQLite DB or mock Telegram bot application).
- [x] T003 [P] Create scaffold test files `tests/unit/test_config.py`, `tests/unit/test_db.py`, `tests/unit/test_handlers.py`, `tests/unit/test_onboarding.py`, `tests/unit/test_responses.py`.

---

## Phase 2: Foundational (TDD: Configuration Hardening)

**Purpose**: Test and enforce the new configuration standards (No credentials in code).

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [x] T004 Write unit tests in `tests/unit/test_config.py` verifying `pydantic` throws `ValidationError` if `OPENAI_API_KEY` and `TELEGRAM_BOT_TOKEN` are missing.
- [x] T005 Run `pytest` to ensure T004 tests fail.
- [x] T006 Implement configuration changes in `src/nova/utils/config.py` explicitly requiring `OPENAI_API_KEY` and `TELEGRAM_BOT_TOKEN` (removing default fallbacks).
- [x] T007 Run `pytest` to ensure T004 tests pass.

**Checkpoint**: Core config is securely tested.

---

## Phase 3: Retroactive TDD Coverage (Spec 001 & 002)

**Purpose**: Test coverage for previous logic before moving onto the new requirements.

### Database Models & Operations
- [x] T008 Write tests in `tests/unit/test_db.py` for creating and fetching `User`, `Message`, and `GraphState`. Ensure they fail.
- [x] T009 Refactor/Verify `src/nova/database/repository.py` until tests pass.

### Onboarding & Private/Group Routing
- [x] T010 [P] Write tests in `tests/unit/test_onboarding.py` verifying `/start` captures Name, Weight, Height and saves to DB.
- [x] T011 [P] Write tests in `tests/unit/test_handlers.py` verifying `handle_text_message` ignores group chat messages missing `@bot_username`.
- [x] T012 Run tests and verify existing logic from Spec 001 and 002 passes successfully. Fix any bugs.

**Checkpoint**: Historical features are now fully test-covered.

---

## Phase 4: User Story 1 - Concise Conversational Output (Priority: P1)

**Goal**: Update the LLM system prompt to enforce short, dense responses.

**Independent Test**: Prompt tests verify presence of brevity rules. Mock LLM requests verify history concatenation.

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T013 [US1] Write test in `tests/unit/test_responses.py` asserting `NOVA_SYSTEM_PROMPT` contains rules explicitly forbidding conversational filler and demanding short length.
- [x] T014 [US1] Write test in `tests/unit/test_responses.py` asserting `invoke_llm` appends the system prompt correctly when provided a mock `AgentState`.
- [x] T015 Run `pytest tests/unit/test_responses.py` and verify tests fail.

### Implementation for User Story 1

- [x] T016 [US1] Update `src/nova/agent/persona.py` to rewrite `NOVA_SYSTEM_PROMPT` to enforce strict brevity (e.g. "Keep responses extremely short and dense. Do not use filler text like 'As an AI' or 'Here is your update'.").
- [x] T017 [US1] Run `pytest` and verify tests now pass.

**Checkpoint**: At this point, the system prompt actively prevents long-winded answers, verified via TDD.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T018 Code cleanup and formatting using `black` and `ruff`.
- [x] T019 Run full `pytest` suite ensuring 100% pass rate.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Must run first.
- **Foundational (Phase 2)**: Depends on Setup.
- **Retroactive TDD (Phase 3)**: Depends on Foundational completion.
- **User Story 1 (Phase 4)**: Depends on Phase 3.
- **Polish (Final Phase)**: Depends on Phase 4 completion.