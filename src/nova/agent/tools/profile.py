"""Profile setup tools for AI-driven onboarding. Contract: specs/009-nova-profile-flow/contracts/profile-tools.md"""

from langchain_core.tools import tool

from nova.database.repository import (
    update_user_profile_partial,
    get_missing_profile_fields,
    get_user_by_id,
)
from nova.utils.logging import get_logger
from nova.utils.urls import normalize_google_sheet_url

logger = get_logger(__name__)


@tool
def update_profile_field(
    user_id: int,
    name: str | None = None,
    weight: float | None = None,
    height: float | None = None,
    google_sheet_url: str | None = None,
) -> str:
    """Update the user's profile fields. Pass only the fields you want to update.
    Use this when the user provides name, weight, height, or Google Sheet URL.
    After updating, is_setup_completed is recomputed automatically.
    Returns a status message (e.g. 'Updated name and weight' or 'Profile complete. You are ready to use.').
    """
    kwargs: dict = {}
    if name is not None:
        kwargs["name"] = str(name).strip() if name else None
    if weight is not None:
        kwargs["weight"] = float(weight)
    if height is not None:
        kwargs["height"] = float(height)
    if google_sheet_url is not None:
        raw = str(google_sheet_url).strip() if google_sheet_url else None
        kwargs["google_sheet_url"] = (
            normalize_google_sheet_url(raw) if raw else None
        )

    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    if not kwargs:
        return "No valid fields to update."

    logger.info(f"Updating profile for user_id={user_id}: {list(kwargs.keys())}")
    updated = update_user_profile_partial(user_id, **kwargs)
    if not updated:
        return "Error: User not found."

    if updated.is_setup_completed:
        return "Profile complete. You are ready to use."
    updated_names = ", ".join(kwargs.keys())
    return f"Updated {updated_names}."


@tool
def check_setup_complete(user_id: int) -> str:
    """Call this FIRST at the start of every interaction. Returns whether profile setup is complete.
    Returns: 'complete' if all fields set, or 'incomplete: missing X, Y' where X,Y are field names.
    Use the result to decide how to respond—no fixed responses."""
    user = get_user_by_id(user_id)
    if not user:
        return "User not found."
    missing = get_missing_profile_fields(user_id)
    if not missing:
        return "complete"
    return f"incomplete: missing {', '.join(missing)}"


@tool
def get_profile_status(user_id: int) -> str:
    """Get the user's profile status: which fields are filled and which are missing.
    Call check_setup_complete first. Use this for details when guiding setup.
    """
    user = get_user_by_id(user_id)
    if not user:
        return "Error: User not found."
    missing = get_missing_profile_fields(user_id)
    if not missing:
        return "Profile is complete. All required fields (name, weight, height, google_sheet_url) are set."
    filled = [
        f for f in ["name", "weight", "height", "google_sheet_url"] if f not in missing
    ]
    parts = []
    if filled:
        parts.append(f"Filled: {', '.join(filled)}.")
    parts.append(f"Missing: {', '.join(missing)}.")
    return " ".join(parts)
