# Tasks: Nova-Only Commands + Modular Handlers

**Input**: Design documents from `/specs/008-nova-only-profile-dm/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Organization**: Tasks are grouped by user story. Phase 2 (Handler Split) is foundational and blocks all user stories.

## Phase 1: Setup

**Purpose**: Create handler package structure

- [x] T001 Create `src/nova/bot/handlers/` directory and empty `__init__.py` stub

---

## Phase 2: Foundational – Handler Split (Blocking)

**Purpose**: Split monolithic handlers.py into modules. Preserve current behavior. BLOCKS all user stories.

- [x] T002 [P] Extract `_process_and_reply` to `src/nova/bot/handlers/core.py` as `process_and_reply`
- [x] T003 [P] Extract onboarding handlers (start_command, handle_name, handle_weight, handle_height, handle_sheet_url, cancel_onboarding) and states to `src/nova/bot/handlers/onboarding.py`
- [x] T004 [P] Extract `handle_nova_command` to `src/nova/bot/handlers/nova.py`
- [x] T005 [P] Extract `handle_text_message` to `src/nova/bot/handlers/text.py`
- [x] T006 [P] Extract `handle_non_text_message` to `src/nova/bot/handlers/fallback.py`
- [x] T007 Implement `register_handlers` in `src/nova/bot/handlers/__init__.py` importing from submodules and wiring to Application
- [x] T008 Update imports in `tests/unit/test_handlers.py` to use `nova.bot.handlers` package submodules where needed
- [x] T009 Delete `src/nova/bot/handlers.py` after migration

**Checkpoint**: All existing tests pass; behavior unchanged.

---

## Phase 3: User Story 1 – Unregistered User Uses /nova (P1) 🎯 MVP

**Goal**: Unregistered user sending `/nova` receives in-context reply + DM with profile setup trigger.

**Independent Test**: Send `/nova` as unregistered user; verify reply and DM with setup instructions.

### Tests for User Story 1 (TDD)

- [x] T010 [P] [US1] Add tests in `tests/unit/test_handlers.py`: unregistered `/nova` in group → in-context reply + DM with setup text
- [x] T011 [P] [US1] Add tests in `tests/unit/test_handlers.py`: unregistered `/nova` in private → setup flow or DM with /setup

### Implementation for User Story 1

- [x] T012 [US1] In `src/nova/bot/handlers/nova.py`: when user has no profile, reply in-context "Check your private messages to create a profile" and send DM "Send /setup to begin profile setup"
- [x] T013 [US1] Add `/setup` as ConversationHandler entry point in `src/nova/bot/handlers/__init__.py` (only for private chat; onboarding runs in DM)
- [x] T014 [US1] Update `start_command` in `src/nova/bot/handlers/onboarding.py` to be the handler for `/setup`; ensure it only runs in private chat

**Checkpoint**: Unregistered `/nova` → reply + DM; `/setup` in private starts onboarding.

---

## Phase 4: User Story 2 – Remove /start Command (P1)

**Goal**: `/start` no longer triggers onboarding; setup triggered only via `/setup` from DM.

**Independent Test**: Send `/start` → no onboarding; `/setup` in private → onboarding starts.

### Tests for User Story 2 (TDD)

- [x] T015 [P] [US2] Add test in `tests/unit/test_handlers.py`: `/start` does not start onboarding (no name/weight prompts)

### Implementation for User Story 2

- [x] T016 [US2] Remove `/start` from ConversationHandler entry_points in `src/nova/bot/handlers/__init__.py`
- [x] T017 [US2] Add handler for `/start` that returns short "Use /nova to interact" in `src/nova/bot/handlers/onboarding.py` (optional; or leave unhandled)

**Checkpoint**: `/start` yields no onboarding; `/setup` is the only entry.

---

## Phase 5: User Story 3 – Registered User Context Rules (P2)

**Goal**: Private = direct messages; Group/channel/topic = only `/nova`; free text ignored in non-private.

**Independent Test**: Registered user: free text in private → reply; free text in group → ignored; `/nova` anywhere → reply.

### Tests for User Story 3 (TDD)

- [x] T018 [P] [US3] Add test in `tests/unit/test_handlers.py`: registered user free text in private → processed
- [x] T019 [P] [US3] Add test in `tests/unit/test_handlers.py`: registered user free text in group → ignored (no reply)

### Implementation for User Story 3

- [x] T020 [US3] In `src/nova/bot/handlers/text.py`: process only when `chat.type == "private"`; remove reply-to-bot logic for groups (return early if not private)
- [x] T021 [US3] Verify `src/nova/bot/handlers/nova.py` processes `/nova` in any context (group, channel, topic, private) for registered users

**Checkpoint**: Private chat accepts direct messages; groups/channels/topics require `/nova`.

---

## Phase 6: Polish & Cross-Cutting

- [x] T022 [P] Run `pytest`, `ruff check .`, `ruff format .` and fix any issues
- [x] T023 Update `tests/unit/test_handlers.py` for new flows (unregistered DM, /start no-op, text private-only)
- [x] T024 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1**: No dependencies
- **Phase 2**: Depends on Phase 1 – BLOCKS Phases 3–5
- **Phases 3–5**: Depend on Phase 2; US2 depends on US1 (shared onboarding); US3 depends on US1/US2
- **Phase 6**: Depends on Phases 3–5

### Parallel Opportunities

- T002–T006 can run in parallel (different files)
- T010–T011 (US1 tests), T018–T019 (US3 tests) can run in parallel

---

## Implementation Strategy

### MVP First (US1)

1. Phase 1 → Phase 2 (handler split)
2. Phase 3 (US1: unregistered /nova → DM + /setup)
3. Validate: unregistered flow works end-to-end

### Incremental Delivery

1. Phase 2 → Handler structure ready
2. Phase 3 → Unregistered users can onboard via DM
3. Phase 4 → /start removed
4. Phase 5 → Context rules (private vs group)
5. Phase 6 → Polish
