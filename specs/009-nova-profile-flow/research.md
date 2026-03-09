# Research: AI-Driven Profile Setup

## Tool Design for Profile Updates

**Decision**: Provide `update_profile_field` (or `update_profile_fields`) and `get_profile_status` tools. The AI can call `get_profile_status` to see what's missing, then `update_profile_field(name=..., weight=..., height=..., google_sheet_url=...)` with any subset of fields.

**Rationale**: Single tool with optional kwargs allows partial updates and multi-field updates in one call. Matches "user enters more data in single message → AI updates correct fields."

**Alternatives considered**:
- One tool per field: More calls, more token usage; rejected.
- Single `complete_profile` tool with all-or-nothing: Less flexible; rejected.

## Required vs Optional Fields

**Decision**: Required for `is_setup_completed`: `name`, `weight`, `height`, `google_sheet_url`. Optional: `goals` (if added).

**Rationale**: Aligns with 009 spec and existing onboarding. Goals can be a future addition.

## Migration Strategy

**Decision**: Add `is_setup_completed` as nullable boolean; backfill existing users: if name, weight, height, google_sheet_url are all non-null → True, else False.

**Rationale**: Non-breaking for existing data; Alembic or ad-hoc migration.
