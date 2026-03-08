# Tasks: N.O.V.A. MVP Comm Link

**Input**: Design documents from `/specs/001-health-bot-mvp/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/` at repository root
- As specified in `plan.md`, the structure is strictly isolated within `src/nova/`.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Initialize Python project, configure pyproject.toml, and install base dependencies (typer, python-telegram-bot, langgraph, langchain, rich, pydantic-settings, tomllib)
- [x] T002 [P] Create initial directory structure under `src/nova/` as defined in the plan
- [x] T003 [P] Configure linting/formatting tools (Black, isort, Ruff, MyPy) with an 88-character line limit and strict mode in pyproject.toml

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Implement unified logging setup in `src/nova/utils/logging.py` (using `setup_unified_logging` and `get_logger`)
- [x] T005 [P] Setup environment configuration management using pydantic-settings in `src/nova/utils/config.py`
- [x] T006 Implement core Typer CLI entrypoint in `src/nova/cli.py` calling the logging setup
- [x] T007 [P] Create SQLite connection pool, initialization logic, and base table creation in `src/nova/database/db.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 3 - New User Onboarding (Priority: P1) 🎯 MVP First Step

**Goal**: Establish the onboarding prompt to collect physical details and save them, allowing the AI to calculate HP/Stamina later.
*(Note: Ordered first because US1 conversation depends on the user profile existing.)*

**Independent Test**: Messaging the bot from a new account triggers the account creation menu.

### Implementation for User Story 3

- [x] T008 [P] [US3] Create `User` Pydantic model and entities in `src/nova/models/domain.py`
- [x] T009 [P] [US3] Implement SQLite repository functions for `User` CRUD operations in `src/nova/database/repository.py`
- [x] T010 [US3] Create the core Telegram bot wrapper and basic message polling logic in `src/nova/bot/platform.py`
- [x] T011 [US3] Implement the `/start` command and onboarding conversation flow (requesting Name, Weight, Height) in `src/nova/bot/handlers.py`
- [x] T012 [US3] Wire the bot handlers into the Typer CLI `run` command in `src/nova/cli.py`

**Checkpoint**: New users can message the bot, trigger the onboarding flow, and their profile is successfully stored in the SQLite database.

---

## Phase 4: User Story 1 - Establish Basic Conversation (Priority: P1)

**Goal**: Establish bidirectional text communication using LangGraph and the LLM adopting the N.O.V.A persona.

**Independent Test**: Sending a message to the bot returns a N.O.V.A persona response, and follow-ups retain conversation memory.

### Implementation for User Story 1

- [x] T013 [P] [US1] Create `Message` and `GraphState` Pydantic models in `src/nova/models/domain.py`
- [x] T014 [P] [US1] Implement SQLite repository functions for `Message` and `GraphState` in `src/nova/database/repository.py`
- [x] T015 [P] [US1] Write the system prompt enforcing the N.O.V.A persona in `src/nova/agent/persona.py`
- [x] T016 [US1] Implement the LangGraph agent orchestrator (LLM integration and state updating) in `src/nova/agent/graph.py`
- [x] T017 [US1] Create standard text message handler in `src/nova/bot/handlers.py` that delegates to `graph.py` instead of the onboarding flow if the user exists.
- [x] T018 [US1] Add graceful fallback handler for non-text messages (e.g., photos/stickers) in `src/nova/bot/handlers.py`

**Checkpoint**: At this point, fully registered users can have a multi-turn conversation with the AI, and their graph state is persisted in SQLite.

---

## Phase 5: User Story 2 - Omnichannel Profile Sync (Priority: P1)

**Goal**: Ensure the bot replies in the specific channel or DM it was messaged from, while syncing context to a single global profile.

**Independent Test**: Mentioning the bot in a group chat utilizes the same `GraphState` and replies directly in the group chat.

### Implementation for User Story 2

- [x] T019 [US2] Update `src/nova/bot/handlers.py` to extract the `chat_id` and determine if the context is a private DM or a channel.
- [x] T020 [US2] Update the Telegram response dispatch logic in `src/nova/bot/platform.py` to route the LLM output explicitly to the originating `chat_id` rather than defaulting to the `user_id` DM.
- [x] T021 [US2] Verify `src/nova/database/repository.py` fetches the user's `GraphState` uniquely by `telegram_id` regardless of the originating `chat_id`.

**Checkpoint**: All user stories are independently functional. The bot operates in group chats seamlessly.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T022 [P] Clean up `print()` statements ensuring 100% compliance with `get_logger()` across all files
- [x] T023 Code cleanup, PEP 8 enforcement, and MyPy strict validation execution

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - US3 must be executed before US1 so that the user profile database exists.
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 3 (Onboarding)**: First feature logic implemented to populate the `User` database.
- **User Story 1 (Basic Conversation)**: Depends on US3 (requires `User` in DB).
- **User Story 2 (Omnichannel)**: Depends on US1 (modifies the messaging routing logic established in US1).

### Parallel Opportunities

- Initialization of the Database (T007), Configuration (T005), and initial Data Models (T008) can all be built in parallel.
- All repository/database CRUD operations (T009, T014) can be developed independently of the LangGraph/LLM logic (T015, T016).