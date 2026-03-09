# Tasks: Group Onboarding & Gamified Health Dashboard Integration

**Input**: Design documents from `/specs/005-group-onboarding-prompt/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Tests**: TDD methodology is mandated by the Project Constitution. All test tasks MUST be completed and fail before implementation begins.

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

- [ ] T001 Initialize project with `gspread` and `google-auth` dependencies in `pyproject.toml`
- [ ] T002 Add Google Sheets API credentials config in `src/nova/core/config.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T003 Update `User` model to include `google_sheet_url` and `google_sheet_credentials` in `src/nova/database/models.py`
- [ ] T004 Create `DailyMetric` model in `src/nova/database/models.py`
- [ ] T005 [P] Create `GoogleSheetsService` base class in `src/nova/services/sheets.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Graceful Group Onboarding Redirection (Priority: P1) 🎯 MVP

**Goal**: When an unknown/unregistered user attempts to trigger the bot in a group chat, direct them to DM instead of exposing health data publicly.

**Independent Test**: Have a new user type `/nova hello` in a group chat, verify bot replies asking them to DM to register instead of prompting for name/weight.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T006 [US1] Unit test for group onboarding redirection in `tests/unit/test_handlers.py`

### Implementation for User Story 1

- [ ] T007 [US1] Implement group chat check and DM redirection logic in `src/nova/bot/handlers.py`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Gamified Dashboard Initialization via Onboarding (Priority: P1)

**Goal**: When setting up profiles in private DM, prompt users for Google Sheets API credentials/link, validate access, and ensure "Dashboard" and "Daily Logs" tabs exist.

**Independent Test**: Complete private onboarding, verify bot asks for Google Sheet ID, validates access, and updates the database.

### Tests for User Story 2 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T008 [P] [US2] Unit test for Google Sheet URL collection during onboarding in `tests/unit/test_handlers.py`
- [ ] T009 [P] [US2] Unit test for Google Sheet validation and tab check in `tests/unit/test_sheets.py`

### Implementation for User Story 2

- [ ] T010 [US2] Implement `verify_sheet_structure` method in `src/nova/services/sheets.py`
- [ ] T011 [US2] Add states to `ConversationHandler` to ask for sheet URL in `src/nova/bot/handlers.py`
- [ ] T012 [US2] Update user profile creation to save `google_sheet_url` securely in `src/nova/bot/handlers.py`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Daily Stat Tracking (Weight) (Priority: P1)

**Goal**: Report daily stats (e.g., "today I weigh 74 kilo"), save to SQLite (source of truth), and update the "Daily Logs" tab of the Google Sheet.

**Independent Test**: Send "I weigh 74kg today", verify bot confirms, saves to SQLite, and updates the corresponding date row in the Google Sheet.

### Tests for User Story 3 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T013 [US3] Unit test for `sync_daily_log` in `tests/unit/test_sheets.py`
- [ ] T014 [US3] Unit test for background sheet sync trigger in `tests/unit/test_graph.py` (or equivalent location)

### Implementation for User Story 3

- [ ] T015 [P] [US3] Implement `sync_daily_log` method using `gspread` in `src/nova/services/sheets.py`
- [ ] T016 [US3] Extract metric from LLM response and save to SQLite `daily_metrics` table in `src/nova/bot/graph.py`
- [ ] T017 [US3] Trigger `GoogleSheetsService.sync_daily_log` after SQLite commit in `src/nova/bot/graph.py`

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T018 [P] Ensure all Google API errors are handled gracefully without crashing the bot in `src/nova/services/sheets.py`
- [ ] T019 [P] Code cleanup, type checking, and linting with Ruff and Black
- [ ] T020 Run quickstart.md validation to ensure setup steps work

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can proceed sequentially (US1 → US2 → US3) or in parallel if isolated properly.
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2)
- **User Story 2 (P1)**: Can start after Foundational (Phase 2)
- **User Story 3 (P1)**: Can start after Foundational (Phase 2), but benefits from US2 being complete so the Google Sheet exists.

### Within Each User Story

- Tests MUST be written and FAIL before implementation (TDD).
- Story complete before moving to next priority.

### Parallel Opportunities

- All tests for a user story marked [P] can run in parallel
- `GoogleSheetsService` logic (US3: T015) can be developed in parallel to LangGraph integration (US3: T016)

---

## Parallel Example: User Story 2

```bash
# Launch all tests for User Story 2 together:
Task: "Unit test for Google Sheet URL collection during onboarding in tests/unit/test_handlers.py"
Task: "Unit test for Google Sheet validation and tab check in tests/unit/test_sheets.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently
3. Add User Story 2 → Test independently
4. Add User Story 3 → Test independently
5. Polish and finalize error handling.