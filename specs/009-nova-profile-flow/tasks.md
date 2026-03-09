# Tasks: AI-Driven Profile Setup + Nova Flow

**Input**: Design documents from `/specs/009-nova-profile-flow/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Organization**: Phase 2 (Foundational) blocks all user stories. US1 and US2 share the AI-driven setup flow.

## Phase 1: Setup

**Purpose**: Verify project structure

- [x] T001 Verify `src/nova/agent/tools/` exists and add `profile.py` stub if needed

---

## Phase 2: Foundational (Blocking)

**Purpose**: User model + repository; BLOCKS all user stories.

- [x] T002 Add `is_setup_completed: Mapped[bool]` to `User` in `src/nova/database/models.py` (default False)
- [x] T003 Add `update_user_profile_partial(user_id: int, **kwargs) -> User` in `src/nova/database/repository.py`
- [x] T004 Add `get_missing_profile_fields(user_id: int) -> list[str]` in `src/nova/database/repository.py`
- [x] T005 Add `recompute_setup_completed(user_id: int) -> bool` in `src/nova/database/repository.py`
- [x] T006 Add DB migration or init logic to create `is_setup_completed` column and backfill existing users in `src/nova/database/`

**Checkpoint**: User model and repository support profile updates and completion check.

---

## Phase 3: User Story 1 – First-Time Private (P1) 🎯 MVP

**Goal**: First-time user messages privately; bot uses AI + tools to complete profile inline.

**Independent Test**: Send first message in private as new user; bot asks for name, accepts multi-field input, completes setup, responds "you are ready to use."

### Tests for User Story 1 (TDD)

- [x] T007 [P] [US1] Add tests in `tests/unit/test_agent_tools.py`: `update_profile_field` updates provided fields and recomputes `is_setup_completed`; `get_profile_status` returns missing fields

### Implementation for User Story 1

- [x] T008 [US1] Create `update_profile_field` and `get_profile_status` tools in `src/nova/agent/tools/profile.py` per contracts/profile-tools.md
- [x] T009 [US1] Register profile tools in `src/nova/agent/builder.py` for users with `is_setup_completed=False`
- [x] T010 [US1] Add setup-mode system prompt/context in `src/nova/agent/builder.py` or persona: instruct AI to parse messages, call tools for name/weight/height/sheet_url, ask for missing fields, respond "you are ready to use" when complete
- [x] T011 [US1] In `src/nova/bot/handlers/core.py`: when user has no DB record, create `User(telegram_id, is_setup_completed=False)` and route to agent
- [x] T012 [US1] Ensure private messages from users with `is_setup_completed=False` are routed to agent (with profile tools) in `src/nova/bot/handlers/text.py` and `core.py`
- [x] T013 [US1] Remove or bypass ConversationHandler for onboarding; setup handled entirely by agent in `src/nova/bot/handlers/__init__.py`

**Checkpoint**: First-time private user completes profile via AI-driven flow.

---

## Phase 4: User Story 2 – First-Time /nova in Group (P1)

**Goal**: First-time user sends `/nova` in group; in-group reply + DM with setup; setup continues in DM via agent.

**Independent Test**: Send `/nova` in group as new user; see in-group notice + DM; complete setup in DM.

### Implementation for User Story 2

- [x] T014 [US2] In `src/nova/bot/handlers/nova.py`: when user has no profile, create `User(telegram_id, is_setup_completed=False)`, reply in group "You need to set up your profile first", send DM "We're ready to set up. Please enter your name." and route DM context to agent for setup
- [x] T015 [US2] Ensure DM from group-invited user is processed by agent (same flow as US1) when `is_setup_completed=False`

**Checkpoint**: First-time `/nova` in group → in-group notice + DM setup flow.

---

## Phase 5: User Story 3 – Group /nova Only (P2)

**Goal**: In groups, only `/nova` triggers the bot; free text ignored.

**Independent Test**: In group, free text → no reply; `/nova <msg>` → reply.

### Implementation for User Story 3

- [x] T016 [US3] Verify `src/nova/bot/handlers/text.py` ignores non-private messages (no-op for groups); confirm `/nova` is only entry point in groups

**Checkpoint**: Groups process only `/nova`.

---

## Phase 6: Polish & Cross-Cutting

- [x] T017 [P] Add unit tests for `update_user_profile_partial`, `get_missing_profile_fields`, `recompute_setup_completed` in `tests/unit/test_db.py` or new `tests/unit/test_repository.py`
- [x] T018 [P] Add additional unit tests for profile tools in `tests/unit/test_agent_tools.py` (if not covered in T007)
- [x] T019 Update handler tests for new create-user-on-first-contact and agent-driven setup flow in `tests/unit/test_handlers.py`
- [x] T020 Run `pytest`, `ruff check .`, `ruff format .` and fix issues
- [x] T021 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1**: No dependencies
- **Phase 2**: Depends on Phase 1 – BLOCKS Phases 3–5
- **Phases 3–5**: Depend on Phase 2
- **Phase 6**: Depends on Phases 3–5

### Parallel Opportunities

- T003–T005 can run in parallel after T002 (repository functions)
- T007 runs first in Phase 3 (TDD: tests before implementation)
- T017, T018 can run in parallel (repository + profile tool tests)

---

## Implementation Strategy

### MVP First (US1)

1. Phase 1 → Phase 2 (model + repository)
2. Phase 3 (US1: AI-driven private setup)
3. Validate: first-time private completes profile via agent

### Incremental Delivery

1. Phase 2 → Data model ready
2. Phase 3 → Private first-time flow works
3. Phase 4 → Group first-time flow works
4. Phase 5 → Verify group rules
5. Phase 6 → Tests and polish
