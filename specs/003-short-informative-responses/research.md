# Phase 0: Research & Decisions

## Decision: Test-Driven Development (TDD) Adoption
- **Decision**: Fully adopt TDD across all existing and new features, writing `pytest` tests before implementation. This requires scanning existing specs (001, 002, 003) and creating retroactive test plans to ensure comprehensive coverage, enforcing TDD going forward.
- **Rationale**: The newly updated project constitution strictly mandates a TDD approach. Tests must fail before functionality is confirmed.
- **Alternatives considered**: None. Mandated by the user and the constitution.

## Decision: Strict Environment Variables
- **Decision**: Update `src/nova/utils/config.py` to remove default empty string assignments (`""`) for credentials. Keys MUST be strictly mapped to `TELEGRAM_BOT_TOKEN` and `OPENAI_API_KEY`. `python-dotenv` and `pydantic-settings` will raise a configuration error immediately upon boot if the keys are missing from the environment or `.env` file.
- **Rationale**: User explicitly demanded "NEVER STORE IMPORTANT CREDENTIALS IN THE CODE", required environment variable injection, and specified using standard names (`OPENAI_API_KEY`).
- **Alternatives considered**: Using `os.getenv` directly. Rejected because `pydantic-settings` already provides superior validation and `.env` parsing out of the box.

## Decision: Short & Informative Prompts
- **Decision**: Update the LLM system prompt inside the agent context to explicitly constrain the bot to short, informative, and dense responses without conversational filler.
- **Rationale**: Meets the user requirement to provide short but informative responses without long-winded paragraphs.