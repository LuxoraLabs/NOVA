from langgraph.prebuilt import ToolNode
from nova.agent.tools.sheet_setup import setup_google_sheet

# Combine all tools here
tools = [setup_google_sheet]

# Create the ToolNode wrapper
tool_node = ToolNode(tools)
