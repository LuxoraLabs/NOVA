# Handler Registration Contract

## Function

```python
def register_handlers(app: Application) -> None:
    """Register all bot handlers with the application."""
```

## Preconditions

- `app` is a valid `telegram.ext.Application` instance.
- Application has not started (no `run_polling` / `run_webhook` yet).

## Postconditions

- All command handlers (`/nova`, `/start` or `/setup`, `/cancel`) registered.
- Message handlers (text, non-text) registered.
- Onboarding ConversationHandler registered with appropriate states.

## Usage

Called from `platform.py` (or equivalent) during bot startup:

```python
from nova.bot.handlers import register_handlers
register_handlers(application)
```
