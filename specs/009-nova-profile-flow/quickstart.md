# Quickstart: AI-Driven Profile Setup

## What Changed

- User model has `is_setup_completed`. New users start with `False`.
- Setup is driven by the LangGraph agent and tools, not the ConversationHandler.
- Users can provide multiple fields in one message (e.g. "I'm John, 80kg, 180cm"); the AI parses and updates.
- When all required fields are filled, `is_setup_completed` becomes True and the user sees "You are ready to use."

## Verification

1. Run migration or ensure `is_setup_completed` exists on User.
2. Create a user with `is_setup_completed=False`, send "My name is Alice, I weigh 65kg and I'm 170cm" in private.
3. Verify profile updated and AI asks for sheet URL (or similar missing field).
4. Provide sheet URL; verify `is_setup_completed` becomes True and response includes "you are ready to use."
