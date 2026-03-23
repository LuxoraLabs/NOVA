# Comprehensive TDD Plan (Retrospective & Active)

This document maps all user stories and requirements from previous specifications into concrete `pytest` test tasks to fulfill the TDD methodology adopted in version 1.1.0 of the project constitution.

## Spec 001: N.O.V.A. MVP Comm Link
### Tested Under: `tests/unit/test_onboarding.py` & `tests/unit/test_db.py`

**User Story 3 - New User Onboarding**
- **Test 1**: Verify `/start` command sent by an unknown user creates a conversation state asking for a Name.
- **Test 2**: Verify the completion of the conversation flow accurately saves the `User` object (with Name, Weight, Height) into the SQLite database.
- **Test 3**: Verify database retrieval methods correctly construct Pydantic-like / SQLAlchemy User objects.

**User Story 1 - Establish Basic Conversation**
- **Test 4**: Ensure standard text messages invoke the LangGraph orchestrator (mocked LLM) and successfully append new `Message` rows in the database.
- **Test 5**: Verify `chat_history` strings correctly serialize/deserialize in the `GraphState`.

## Spec 002: Group Chat Mention Requirement
### Tested Under: `tests/unit/test_handlers.py`

**User Story 1 - Private Message Direct Response**
- **Test 6**: Verify `handle_text_message` processes incoming messages immediately if `chat.type == "private"`, without requiring the bot's username.

**User Story 2 - Group Chat Explicit Mention Requirement**
- **Test 7**: Verify `handle_text_message` immediately returns (ignores) if `chat.type != "private"` and the bot's handle is missing from the text.
- **Test 8**: Verify `handle_text_message` strips the `@bot_handle` from the text string before passing it into `process_message` when a mention occurs in a group chat.
- **Test 9**: Verify the outgoing bot response uses `context.bot.send_message(chat_id=...)` to direct the reply to the exact channel it was summoned from, avoiding a private DM leak.

## Spec 003: Short Informative Responses
### Tested Under: `tests/unit/test_persona.py` & `tests/unit/test_config.py`

**Configuration Enforcement**
- **Test 10**: Verify `get_settings()` raises a `ValidationError` from pydantic if `OPENAI_API_KEY` or `TELEGRAM_BOT_TOKEN` are absent.

**User Story 1 - Concise Conversational Output**
- **Test 11**: Assert the `NOVA_SYSTEM_PROMPT` contains specific directives prohibiting conversational filler, enforcing short responses, and retaining information density. (Tests the prompt text itself).
- **Test 12**: Mock the LangChain `ChatOpenAI` invocation to verify the system prompt successfully pre-pends to the chat history array before dispatching the request.