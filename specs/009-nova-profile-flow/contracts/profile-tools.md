# Profile Tools Contract

## update_profile_field

**Signature** (conceptual):

```
update_profile_field(
  user_id: int,
  name: str | None = None,
  weight: float | None = None,
  height: float | None = None,
  google_sheet_url: str | None = None
) -> str
```

**Behavior**: Updates only the provided non-None fields for the user. Recomputes `is_setup_completed` after update. Returns a status message (e.g. "Updated name and weight" or "Profile complete. You are ready to use.").

**Preconditions**: User exists.

## get_profile_status

**Signature** (conceptual):

```
get_profile_status(user_id: int) -> str
```

**Behavior**: Returns a structured summary of the user's profile: which fields are filled, which are missing. Used by the AI to decide what to ask next.

**Preconditions**: User exists.
