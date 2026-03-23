# Data Model

## Key Entities

### User
Represents an individual using the N.O.V.A. system.
- `id`: Internal Primary Key
- `telegram_id`: Unique identifier from the Telegram platform (String/Integer).
- `name`: User's preferred name (from onboarding).
- `weight`: Physical weight metric.
- `height`: Physical height metric.
- `created_at`: Timestamp of account creation.

### Message
Records a single communication event (both inbound and outbound).
- `id`: Internal Primary Key
- `user_id`: Foreign Key to `User.id`
- `content`: Text content of the message.
- `role`: Enum ("user" or "assistant").
- `chat_context`: String ("private" or the specific "channel" ID).
- `timestamp`: Time the message was sent/received.

### GraphState
Stores the current orchestration context for the LangGraph agent to resume processing seamlessly.
- `user_id`: Foreign Key to `User.id` (Unique, One-to-One)
- `current_message`: The latest text payload intended for processing.
- `chat_history`: Serialized JSON payload containing previous conversational turns for context.
- `current_step`: String tracking the current state within the LangGraph flow (e.g., "waiting_for_input", "processing_llm").