# Tasks: Topic Mention Response Support

**Input**: Design documents from `/specs/004-topic-mention/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/` and `tests/` at repository root

---

## Phase 1: Setup

**Purpose**: Project initialization and basic structure

- [x] T001 Verify project structure and dependencies match the implementation plan. No new dependencies are required for this feature.

---

## Phase 2: Foundational

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T002 Update `tests/unit/test_handlers.py` to ensure all existing tests pass and fixtures are ready for topic-based message modifications. 
- [x] T003 Update `src/nova/bot/handlers.py` with `logger.debug` tracing to capture incoming raw message payloads, helping with manual testing of topic `message_thread_id` parameters.

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: User Story 1 - Mention Response in Group Topics (Priority: P1) 🎯 MVP

**Goal**: Users interacting with the AI bot inside a specific Topic (Thread) within a Group channel must receive a direct reply inside that exact same Topic when they explicitly mention the bot.

**Independent Test**: Can be tested by creating a Topic in a Telegram Group, mentioning the bot within that Topic, and verifying that the bot's response is threaded correctly into that exact Topic (rather than failing or dropping into a different topic).

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T004 [US1] Create a new test case in `tests/unit/test_handlers.py` that mocks a group chat message originating from a specific `message_thread_id` and explicitly mentioning the bot. Assert that `context.bot.send_message` is called with that exact `message_thread_id`.
- [x] T005 [US1] Run `pytest` and verify the new test in `tests/unit/test_handlers.py` fails before modifying the handler.

### Implementation for User Story 1

- [x] T006 [US1] Modify `handle_text_message` in `src/nova/bot/handlers.py` to extract `update.message.message_thread_id`.
- [x] T007 [US1] Update the `await context.bot.send_message` call in `handle_text_message` in `src/nova/bot/handlers.py` to pass the extracted `message_thread_id` as a keyword argument (falling back to `None` or omitted if not present).
- [x] T008 [US1] Add `logger.debug` trace in `src/nova/bot/handlers.py` right before `send_message` to log the target `chat_id` and `message_thread_id`.
- [x] T009 [US1] Run `pytest` to ensure all unit tests (including the new topic test) pass successfully.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T010 Run `black` and `ruff` formatting tools on the codebase.
- [x] T011 Run the full `pytest` suite to ensure no regressions were introduced.

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

- Tests MUST be written and FAIL before implementation
- Implementation logic completed
- Verify tests pass
