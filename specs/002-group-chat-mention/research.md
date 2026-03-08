# Phase 0: Research & Decisions

## Decision: Package Management & CLI Execution
- **Decision**: Switch from `uv` and `hatchling` back to native standard tools: standard Python (`pip install -e .` with a `pyproject.toml` or `setup.py` fallback if necessary), allowing developers to run the `nova` CLI directly after editable installation. Remove `uv` centric toolchains from deployment assumptions.
- **Rationale**: User explicitly requested to stop using `uv`, to utilize standard TOML with `pip3 install . -e`, and to ensure lightweight standard tools.
- **Alternatives considered**: `poetry`, `hatch`. Discarded because `pip` with `pyproject.toml` is the lowest common denominator and natively supported per user request.

## Decision: Agent Architecture Splitting
- **Decision**: Refactor `src/nova/agent/graph.py` into a robust modular folder structure.
  - `src/nova/agent/builder.py`: For compiling the LangGraph workflow.
  - `src/nova/agent/state.py`: For fetching, saving, and managing graph state specifically.
  - `src/nova/agent/orchestrator.py`: For executing the graph and running the LangGraph application.
  - `src/nova/agent/nodes/`: Directory containing specific node functions.
  - `src/nova/agent/tools/`: Directory containing specific tools the LLM can use.
- **Rationale**: User requested that the agent code be divided into multiple files based on responsibility (building graph, managing state, orchestrating) and explicitly requested folders for nodes and tools for future scalability and simplicity.
- **Alternatives considered**: Keep in a single file (rejected, violates user requirement for splitting files by responsibility).

## Decision: Configuration Management
- **Decision**: Use `python-dotenv` natively or configure `pydantic-settings` to explicitly read `.env` files in `src/nova/utils/config.py`.
- **Rationale**: User explicitly requested: "read api keys from the env vars in the @src/nova/utils/config.py so get from dot_env".
- **Alternatives considered**: TOML config parsing only (rejected, user explicitly requested `.env`).

## Decision: Database ORM Strategy
- **Decision**: Migrate from raw SQLite queries (`sqlite3`) to **SQLAlchemy** declarative models for database mapping.
- **Rationale**: The user explicitly requested "use sqlalchemy modes for database models".
- **Alternatives considered**: Raw SQL strings (rejected per user request), other ORMs like Tortoise ORM or Peewee (rejected, SQLAlchemy is explicitly requested and industry standard).

## Decision: Simplification & Dependency Pruning
- **Decision**: Remove caching mechanisms (specifically instructed: "dont use mypycache"), delete unnecessary heavy dependencies, and strictly maintain a lean `pyproject.toml`.
- **Rationale**: User explicitly asked to delete useless dependencies, stay lightweight, and avoid `mypycache`.