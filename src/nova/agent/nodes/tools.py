from langgraph.prebuilt import ToolNode
from nova.agent.tools.sheet_setup import setup_google_sheet
from nova.agent.tools.profile import (
    update_profile_field,
    get_profile_status,
    check_setup_complete,
)

# All tools the agent may call (ToolNode must have full list)
tools = [setup_google_sheet, update_profile_field, get_profile_status, check_setup_complete]

# Create the ToolNode wrapper
tool_node = ToolNode(tools)


def get_tools_for_user(is_setup_completed: bool) -> list:
    """Return tools available for the user. Profile tools only when setup incomplete."""
    if is_setup_completed:
        return [setup_google_sheet]
    return [
        setup_google_sheet,
        update_profile_field,
        get_profile_status,
        check_setup_complete,
    ]
