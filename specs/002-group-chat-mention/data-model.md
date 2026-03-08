# Data Model

*Note: Migrating to SQLAlchemy Declarative Models.*

## Key Entities

### User (`users` table)
Represents an individual using the N.O.V.A. system.
- `id`: Integer, Primary Key
- `telegram_id`: Integer, Unique, Not Null
- `name`: String, Nullable
- `weight`: Float, Nullable
- `height`: Float, Nullable
- `created_at`: DateTime, Default=UTC Now

### Message (`messages` table)
Records a single communication event.
- `id`: Integer, Primary Key
- `user_id`: Integer, ForeignKey(`users.id`), Not Null
- `content`: String, Not Null
- `role`: String, Not Null
- `chat_context`: String, Not Null
- `timestamp`: DateTime, Default=UTC Now

### GraphState (`graph_states` table)
Stores the LangGraph orchestration context for state persistence across interactions.
- `user_id`: Integer, ForeignKey(`users.id`), Primary Key
- `current_message`: String, Nullable
- `chat_history`: String (JSON Serialized), Nullable
- `current_step`: String, Nullable
- `updated_at`: DateTime, Default=UTC Now OnUpdate=UTC Now