# Tasks: Google Sheet Service Account Prompt

**Input**: Design documents from `/specs/007-sheet-editor-prompt/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Verify active environment and project dependencies

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T002 Add placeholder `GOOGLE_SERVICE_ACCOUNT_EMAIL` to local `.env` file for development and testing

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - See Updated Sheet Setup Instructions (Priority: P1) 🎯 MVP

**Goal**: Users configuring their Google Sheet integration receive a prompt containing the specific service account email they need to add as an editor, eliminating guesswork.

**Independent Test**: Can be fully tested by triggering the sheet setup onboarding flow and verifying that the prompt contains the service account email read from the environment configuration.

### Tests for User Story 1 (TDD Required) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T003 [P] [US1] Add tests verifying the sheet setup prompt includes the `google_service_account_email` when set in `tests/unit/test_handlers.py`
- [x] T004 [P] [US1] Add tests verifying the sheet setup prompt gracefully falls back to generic text when `google_service_account_email` is missing in `tests/unit/test_handlers.py`

### Implementation for User Story 1

- [x] T005 [US1] Add `google_service_account_email: str | None = None` to `Settings` class in `src/nova/utils/config.py`
- [x] T006 [US1] Modify the sheet setup instruction message to explicitly instruct granting "Editor" access to the email from `settings.google_service_account_email` (with fallback logic) in `src/nova/bot/handlers.py`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T007 [P] Run `pytest` to ensure all tests pass and formatting is correct
- [x] T008 Run quickstart.md validation to ensure instructions are accurate

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- Foundational task (T002) can run alongside setup verification.
- All tests for User Story 1 (T003, T004) can run in parallel.
- Implementation of T005 and T006 are sequential (since the prompt depends on the config).

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Add tests verifying the sheet setup prompt includes the email in tests/unit/test_handlers.py"
Task: "Add tests verifying the sheet setup prompt gracefully falls back in tests/unit/test_handlers.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready
