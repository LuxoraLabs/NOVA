# Research: Modular Handler Structure

## Handler Splitting Pattern

**Decision**: Use a `handlers/` package with one module per responsibility (onboarding, nova, text, fallback, core).

**Rationale**: 
- Constitution §4 mandates "Divide long scripts into multiple smaller scripts, each responsible for a specific, single task."
- python-telegram-bot handlers are plain async functions; no framework-specific grouping required.
- Clear file names (`onboarding.py`, `nova.py`, `text.py`) make navigation predictable.

**Alternatives considered**:
- Single file with sections: Rejected—file already ~315 lines and will grow with 008 changes.
- One module per conversation state: Overkill; onboarding is one cohesive flow.
- Class-based handlers: Rejected—PTB uses functions; consistency with existing codebase.

## Shared Logic Placement

**Decision**: Extract `_process_and_reply` to `core.py`; import from `nova.py` and `text.py`.

**Rationale**: Both `/nova` and direct-text handlers perform the same flow (lookup user, process message, reply). Centralizing avoids duplication.

## Registration Pattern

**Decision**: Keep `register_handlers(app: Application)` in `handlers/__init__.py`; it imports handler functions from submodules and wires them to the Application.

**Rationale**: Single entry point for the platform layer; clear separation between "what handles what" (modules) and "how handlers are registered" (init).
