# Research: Friendlier Prompts and Clear Google Sheet Setup

## Persona Tone

**Decision**: Add a light, friendly persona to prompts—warm opener phrases, supportive framing, non-judgmental reassurance—while preserving the existing brevity rule.

**Rationale**: The spec asks for "a little bit" of persona. Avoid overdoing it; keep responses short. Use phrases like "Let's get to know you!" for setup, "You've got this!" for encouragement, and "No worries—every day is a fresh start" for missed goals.

**Alternatives considered**:
- Heavy persona (lots of emoji, long intros): Rejected—spec says "just a little bit" and brevity is constitution.
- No persona change: Rejected—spec explicitly requests friendlier tone.

## Google Sheet Instruction Format

**Decision**: Provide a structured, step-by-step block in the setup prompt. When `google_service_account_email` is set, include it explicitly. Format:

```
**Google Sheet setup**:
1. Create a new blank spreadsheet at sheets.google.com
2. Click "Share" and add [SERVICE_ACCOUNT_EMAIL] as Editor
3. Copy the URL from your browser's address bar and paste it here
```

When email is not configured, use "our service account email (you'll receive it when you start)" or similar generic phrasing—avoid lying; if truly missing, say "Share with the email we'll provide" or rely on a fallback instruction.

**Rationale**: Clear ordering and explicit email reduce confusion. The agent relays these when asking for the sheet URL.

**Alternatives considered**:
- Separate tool that returns instructions: Adds complexity; prompt injection is simpler for this feature.
- Link to external doc: Rejected—spec says "without requiring external documentation."

## Where to Inject Sheet Instructions

**Decision**: Inject the step-by-step block into the system prompt in `invoke_llm` when `user.is_setup_completed is False`. Append after SETUP_MODE_PROMPT, before the user_id line. Use `get_settings().google_service_account_email` to build the block.

**Rationale**: The LLM needs these instructions in context when it asks for the sheet URL. System prompt is the right place; no new tools or handlers.
