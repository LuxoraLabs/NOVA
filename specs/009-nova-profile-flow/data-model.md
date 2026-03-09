# Data Model: AI-Driven Profile Setup

## User Model Changes

### New Fields

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `is_setup_completed` | `Boolean` | No (default False) | True when all required profile fields are filled. |

### Required Fields for Setup Completion

- `name` (str, not null/empty)
- `weight` (float, not null)
- `height` (float, not null)
- `google_sheet_url` (str, not null/empty)

### Optional Fields (future)

- `goals` (str, nullable) — user-entered goals; does not affect `is_setup_completed`.

### State Transitions

```
is_setup_completed = False
    → User created or any required field is null
    → AI updates fields via tools
    → When all required fields filled: set is_setup_completed = True
```

## Repository Additions

- `update_user_profile_partial(user_id: int, **kwargs) -> User`: Update only provided fields (name, weight, height, google_sheet_url).
- `get_missing_profile_fields(user_id: int) -> list[str]`: Return list of required field names that are null/empty.
- `recompute_setup_completed(user_id: int) -> bool`: Set `is_setup_completed` based on current field values; return new value.
