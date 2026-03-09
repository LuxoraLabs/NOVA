# Quickstart: 008 Nova-Only + Modular Handlers

## What Changed

- `/start` no longer triggers onboarding.
- Only `/nova` triggers the bot in groups, channels, and topics.
- In private chat, users can message the bot directly (no `/nova` required).
- Unregistered users receive a DM to set up their profile.
- Handlers are split into `nova/bot/handlers/` by responsibility.

## Handler Layout

```
nova/bot/handlers/
├── __init__.py     # register_handlers(app)
├── core.py         # Shared process-and-reply logic
├── onboarding.py   # Profile setup (DM-only)
├── nova.py         # /nova command
├── text.py         # Direct messages (private only)
└── fallback.py     # Non-text fallback
```

## Verification

1. Run `uv run pytest tests/unit/test_handlers.py`—handler tests must pass.
2. Start bot: `uv run cli bot run`
3. As unregistered user, send `/nova` in a group → receive "check your DMs" + DM with setup.
4. Complete setup in DM.
5. In private: send free text → bot replies.
6. In group: send `/nova <message>` → bot replies; free text → ignored.
