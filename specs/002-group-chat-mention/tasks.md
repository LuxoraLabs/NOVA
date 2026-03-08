# Tasks: Group Chat Mention Requirement & Refactoring

**Input**: Design documents from `/specs/002-group-chat-mention/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/nova/` at repository root

---

## Phase 1: Setup (Refactoring Preparation)

**Purpose**: Shift away from `uv` to a standard pip/SQLAlchemy architecture.

- [x] T001 Update `pyproject.toml` to remove `uv`/`hatchling` configs, simplify dependencies, and add `sqlalchemy` and `python-dotenv`.
- [x] T002 Update `src/nova/utils/config.py` to properly load environment variables using `python-dotenv` natively or via Pydantic.
- [x] T003 Delete `.mypy_cache` if present and ensure it is ignored in `.gitignore`.
- [x] T004 [P] Scaffold new agent directories: `src/nova/agent/nodes/` and `src/nova/agent/tools/`.

---

## Phase 2: Foundational (SQLAlchemy Migration)

**Purpose**: Migrate the raw SQLite commands to SQLAlchemy ORM models. This must be complete before updating bot logic.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 [P] Create SQLAlchemy declarative base models for `User`, `Message`, and `GraphState` in `src/nova/database/models.py` referencing the updated data-model.md.
- [x] T006 Update `src/nova/database/db.py` to initialize a SQLAlchemy `Engine` and create tables using `Base.metadata.create_all`.
- [x] T007 Refactor `src/nova/database/repository.py` to perform all CRUD operations using SQLAlchemy sessions instead of raw SQL strings.

**Checkpoint**: Foundation ready - Database is fully ORM-based and configuration relies on dotenv.

---

## Phase 3: Foundational (Agent Architecture Splitting)

**Purpose**: Break the monolithic LangGraph application into modular files.

- [x] T008 [P] Move the AgentState schema and history serialization logic into `src/nova/agent/state.py`.
- [x] T009 [P] Extract the LLM execution node function into `src/nova/agent/nodes/llm.py`.
- [x] T010 Create `src/nova/agent/builder.py` to compile the `StateGraph` pulling the schema from `state.py` and the node from `nodes/llm.py`.
- [x] T011 Create `src/nova/agent/orchestrator.py` containing the `process_message` function that interfaces between the database and the graph builder.
- [x] T012 Delete the old, monolithic `src/nova/agent/graph.py` and fix imports in `src/nova/bot/handlers.py` to use `orchestrator.py`.

**Checkpoint**: Agent structure is successfully compartmentalized.

---

## Phase 4: User Story 1 - Private Message Direct Response (Priority: P1)

**Goal**: Ensure private DMs continue to work normally and do not require mentions.

**Independent Test**: Messaging the bot in a private DM returns a response.

### Implementation for User Story 1

- [x] T013 [US1] In `src/nova/bot/handlers.py`, ensure the `handle_text_message` function identifies private chats (`update.effective_chat.type == "private"`) and routes them directly to the orchestrator without checking for mentions.

**Checkpoint**: Private messages work flawlessly.

---

## Phase 5: User Story 2 - Group Chat Explicit Mention Requirement (Priority: P1)

**Goal**: Ignore messages in group chats unless they contain the bot's @handle.

**Independent Test**: In a group chat, messages without the handle are ignored, messages with the handle receive a reply.

### Implementation for User Story 2

- [x] T014 [P] [US2] Update `src/nova/bot/handlers.py` to retrieve the bot's username dynamically (e.g., via `context.bot.username`).
- [x] T015 [US2] In `src/nova/bot/handlers.py`, for non-private chats, verify the bot's `@username` is present in `update.message.text`. If missing, `return` early.
- [x] T016 [US2] In `src/nova/bot/handlers.py`, if the mention exists, strip the `@username` from the text before sending it to `process_message` so the LLM doesn't read its own mention.

**Checkpoint**: All user stories are independently functional. Spam in group chats is prevented.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T017 [P] Code cleanup, PEP 8 enforcement (Black/Ruff), and MyPy strict validation execution (without generating `.mypy_cache`).

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational DB (Phase 2)**: Depends on Phase 1 completion.
- **Foundational Agent (Phase 3)**: Can be run somewhat parallel to Phase 2 but relies on DB completion for full integration.
- **User Stories (Phase 4 & 5)**: Depends on Phase 3 completion.
- **Polish (Final Phase)**: Depends on all user stories being complete.

### User Story Dependencies

- **User Story 1 & 2**: Can be implemented within the exact same function block (`handle_text_message`) sequentially. US1 sets the baseline, US2 adds the exclusion gate.