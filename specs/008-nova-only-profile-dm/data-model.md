# Data Model: 008 Nova-Only Profile DM

No new persistent entities. Existing models (User, Message, GraphState) remain unchanged.

## Handler Module Map

| Module         | Exports                                           |
|----------------|---------------------------------------------------|
| `core`         | `process_and_reply(update, context, text, user, chat_id, chat_context)` |
| `onboarding`   | `start_command`, `handle_name`, `handle_weight`, `handle_height`, `handle_sheet_url`, `cancel_onboarding`, `NAME`, `WEIGHT`, `HEIGHT`, `SHEET_URL` |
| `nova`         | `handle_nova_command`                             |
| `text`         | `handle_text_message`                             |
| `fallback`     | `handle_non_text_message`                         |

## Conversation State

Onboarding ConversationHandler states: `NAME`, `WEIGHT`, `HEIGHT`, `SHEET_URL` (unchanged).
