# Tasks: Automate Google Sheet Setup

**Input**: Design documents from `/specs/006-automate-google-sheet/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Tests**: TDD methodology is mandated by the Project Constitution. All test tasks MUST be completed and fail before implementation begins. Furthermore, `@pytest.mark.skipif` must be used for any tests requiring live API keys.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Define tool node state and routing structure in `src/nova/agent/builder.py`
- [x] T002 Update `AgentState` to support tool messages and internal steps in `src/nova/agent/state.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Refactor LLM node to act as a "Planner" in `src/nova/agent/nodes/llm.py`
- [x] T004 Create LangGraph `ToolNode` execution wrapper in `src/nova/agent/nodes/tools.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Provide Setup Guide to User (Priority: P1) 🎯 MVP

**Goal**: When a user begins the onboarding process, provide a clear guide explaining how to create a sheet and obtain API keys.

**Independent Test**: Trigger the onboarding flow and verify the bot replies with the setup guide.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T005 [P] [US1] Unit test for setup guide prompt state in `tests/unit/test_handlers.py`

### Implementation for User Story 1

- [x] T006 [US1] Update `handle_height` in `src/nova/bot/handlers.py` to send the comprehensive setup guide before asking for the sheet URL.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Automated Google Sheet Formatting (Priority: P1)

**Goal**: Automatically connect to the user's provided sheet via API, create "Dashboard" and "Daily Logs" tabs, and populate headers.

**Independent Test**: Provide a blank Google Sheet URL to the bot, verify it successfully creates tabs and headers.

### Tests for User Story 2 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T007 [US2] Unit test for sheet formatting logic (`initialize_sheet_structure`) in `tests/unit/test_sheets.py`
- [x] T008 [US2] Unit test for the LangGraph tool wrapper in `tests/unit/test_agent_tools.py`

### Implementation for User Story 2

- [x] T009 [P] [US2] Implement `initialize_sheet_structure` method using `gspread.add_worksheet` and `update` in `src/nova/services/sheets.py`
- [x] T010 [P] [US2] Create `@tool` decorated `setup_google_sheet` wrapper function in `src/nova/agent/tools/sheet_setup.py`
- [x] T011 [US2] Register `setup_google_sheet` tool with the Planner LLM in `src/nova/agent/nodes/llm.py`
- [x] T012 [US2] Add conditional edge routing from Planner to Tools node in `src/nova/agent/builder.py`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T013 [P] Ensure errors from `setup_google_sheet` are returned as strings so the Planner can explain failures to the user.
- [x] T014 Run quickstart.md validation to ensure setup steps work
- [x] T015 Run `ruff check .` and `black .`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Integrates heavily with the foundational graph modifications.

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Services before tools
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- `initialize_sheet_structure` logic (T009) can be developed independently from the `@tool` wrapper (T010).