# Tasks: Friendlier Prompts and Clear Google Sheet Setup

**Input**: Design documents from `/specs/010-friendly-prompts-sheet-setup/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Organization**: Phase 2 (Foundational) is minimal; US1 and US2 are largely independent. Both are P1.

## Phase 1: Setup

**Purpose**: Verify project structure

- [x] T001 Verify `src/nova/agent/persona.py` and `src/nova/agent/nodes/llm.py` exist; no new files required

---

## Phase 2: Foundational (Blocking)

**Purpose**: Ensure config supports sheet instructions.

- [x] T002 Verify `src/nova/utils/config.py` exposes `google_service_account_email` (already present; confirm)

**Checkpoint**: Config ready for sheet instruction injection.

---

## Phase 3: User Story 1 – Friendlier Agent Persona (P1)

**Goal**: Agent prompts convey a warmer, more personable tone across setup and tracking.

**Independent Test**: Interact with agent during profile setup; verify prompts feel warm and encouraging (e.g., "Let's get to know you!") while staying brief.

### Tests for User Story 1 (TDD)

- [x] T003 [P] [US1] Add test in `tests/unit/test_responses.py` or `tests/unit/test_persona.py`: assert NOVA_SYSTEM_PROMPT contains friendly/warm persona phrases (e.g., supportive, gentle, encouraging)

### Implementation for User Story 1

- [x] T004 [US1] Update NOVA_SYSTEM_PROMPT in `src/nova/agent/persona.py` with friendlier tone per research.md (warm opener phrases, supportive framing, non-judgmental reassurance)
- [x] T005 [US1] Update SETUP_MODE_PROMPT in `src/nova/agent/persona.py` with friendlier tone (e.g., "Let's get to know you!" style)

**Checkpoint**: Persona feels warm and supportive; brevity preserved.

---

## Phase 4: User Story 2 – Clear Google Sheet Setup Instructions (P1)

**Goal**: When agent asks for sheet URL, provide step-by-step instructions including service account email when configured.

**Independent Test**: Reach sheet setup step; verify instructions are numbered, include create→share→Editor→URL, and show service account email when `GOOGLE_SERVICE_ACCOUNT_EMAIL` is set.

### Tests for User Story 2 (TDD)

- [x] T006 [P] [US2] Add test in `tests/unit/test_responses.py`: when user has `is_setup_completed=False`, system prompt contains sheet setup instructions; when `google_service_account_email` is set, instructions include that email

### Implementation for User Story 2

- [x] T007 [US2] In `src/nova/agent/nodes/llm.py`, when `user.is_setup_completed is False`, build and append step-by-step sheet instructions block to system prompt using `get_settings().google_service_account_email`
- [x] T008 [US2] Use research.md format: Step 1 create sheet, Step 2 share with email as Editor, Step 3 paste URL; when email not configured use fallback ("our secure service account" or similar)

**Checkpoint**: Sheet setup instructions clear, numbered, and include email when configured.

---

## Phase 5: Polish & Cross-Cutting

- [x] T009 Verify `src/nova/bot/handlers/text.py` ignores non-private messages (groups listen to /nova only); add or update test in `tests/unit/test_handlers.py` if needed
- [x] T010 Run `pytest`, `ruff check .`, `ruff format .` and fix issues
- [x] T011 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1**: No dependencies
- **Phase 2**: Depends on Phase 1
- **Phases 3–4**: Depend on Phase 2; US1 and US2 can proceed in parallel
- **Phase 5**: Depends on Phases 3–4

### Parallel Opportunities

- T003, T006 can run in parallel after Phase 2 (tests for US1 and US2)
- T004, T005 can run sequentially (same file)
- T007, T008 are sequential (same file, same logic)

---

## Implementation Strategy

### MVP First (US1)

1. Phase 1 → Phase 2
2. Phase 3 (US1: friendlier persona)
3. Validate: prompts feel warm and supportive

### Incremental Delivery

1. Phase 2 → Config confirmed
2. Phase 3 → Persona updated
3. Phase 4 → Sheet instructions clear
4. Phase 5 → Tests and polish
