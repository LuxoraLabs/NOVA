<!--
Sync Impact Report:
- Version Change: 1.0.0 -> 1.1.0
- Added Sections: "5. Testing & Methodology" (TDD enforcement)
- Modified Principles: None
- Removed Sections: None
- Templates Requiring Updates: None explicitly flagged; agents will respect TDD from here on.
-->
# Project Constitution

## 1. Core Principles
- This is a Python CLI project built using `typer`.
- All command-line interfaces must be built with `typer`, leveraging Python type hints for argument parsing and validation.
- Maintain a unified logging strategy across the entire application to ensure consistent observability.

## 2. CLI Guidelines (`typer`)
- Use `typer.Typer()` for creating modular CLI groups.
- Rely on standard Python type hints (`int`, `str`, `bool`, `Optional`, etc.) for defining CLI arguments and options.
- Use `typer.Option` and `typer.Argument` explicitly when metadata (like help text, short names, or defaults) is needed.
- Avoid using `print()`, `typer.echo()`, or direct `rich` print calls. Use the unified logging setup via `get_logger` exclusively for all terminal output and logging.

## 3. Unified Logging
- Use the project's custom unified logging setup exclusively. Avoid `print()` and other logging frameworks.
- **`setup_unified_logging()`**: Call this early in the application lifecycle (e.g., `main.py` or `cli.py`) to configure the root logger, silence noisy third-party logs, and set up `RichHandler` for console and `RotatingFileHandler` for files.
- **`get_logger(name)`**: Use this function to obtain a named logger instance for your current module (e.g., `logger = get_logger(__name__)`).

## 4. Code Quality & Formatting
- **Formatting:** ALWAYS use **Black** (88 character limit) and **isort** (Black profile) to format code.
- **Type Hinting:** ALWAYS include type hints for all parameters and return types. Verify with **MyPy** (strict mode) statically, but NEVER use `mypy` or `uv` commands as part of the test runner execution.
- **Docstrings:** ALWAYS include PEP 257 docstrings for modules, classes, and functions.
- **Style & Naming:** Follow **PEP 8** strictly (`snake_case` for variables/functions, `PascalCase` for classes).
- **Linting:** Use **Ruff** for linting. All linting and type errors must be fixed before committing.
- **Modularity:** Divide long scripts into multiple smaller scripts, each responsible for a specific, single task to simplify logic and maintain readability.
- **Best Practices:** Use `is`/`is not` for `None` comparisons, `isinstance()` for type checks, and focused, single-purpose functions.

## 5. Testing & Methodology
- **Test-Driven Development (TDD):** Development MUST follow a strict TDD approach. Tests must be written and ensured to fail *before* the implementation of any associated functionality.
- **Testing Framework:** Use `pytest` exclusively for all unit, integration, and contract tests. NEVER use `uv` or `mypy` commands to run or orchestrate tests.
- **Coverage:** All functional logic must be covered by tests. Each user story should ideally have independent tests verifying its specific acceptance criteria.
- **API Key Handling in Tests:** If a test requires an API key or specific environment variables (e.g., `OPENAI_API_KEY`, `GOOGLE_APPLICATION_CREDENTIALS`), use `@pytest.mark.skipif` to automatically skip the test when those keys are not set, preventing CI/CD pipelines or local runs from failing due to missing secrets.
