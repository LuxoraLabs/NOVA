# Research: Topic Mention Routing and Debug Logging

## Telegram Topic Routing

**Decision**: Use the `update.message.message_thread_id` attribute provided by `python-telegram-bot` to route responses.

**Rationale**: Telegram groups can be upgraded to "Forums" containing multiple "Topics". Under the hood, a Topic is just an integer `message_thread_id`. When a user messages a topic, this ID is populated. To reply to that topic, we simply pass `message_thread_id=update.message.message_thread_id` into `context.bot.send_message(...)`. If the message is from a private chat or a standard group chat without topics, this attribute is `None`, which is gracefully ignored by `send_message`. This allows a seamless, unified routing approach.

**Alternatives considered**: 
- Extracting the thread ID and storing it in the `GraphState`. *Rejected*: The spec specifically states that state should not be isolated by topic. Furthermore, since processing is currently synchronous, we only need the thread ID at the exact moment of dispatching the reply.

## Enhanced Debug Logging

**Decision**: Integrate `logger.debug` statements in `src/nova/bot/handlers.py` tracing the lifecycle of message reception, mention detection, and dispatch.

**Rationale**: The user explicitly requested increased debug logging for mentions and sent messages. Using the standard unified logging (`get_logger`), we can output debug statements like `logger.debug(f"Received message in chat {chat_id}, thread {thread_id}")` and `logger.debug("Mention detected, processing...")`. These logs will automatically surface if the application is run with `--log-level DEBUG`.