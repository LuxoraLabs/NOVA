# Research: Automate Google Sheet Setup

## 1. LangGraph Architecture (Planner & Tools)

**Decision**: Implement a dynamic agent architecture using a Planner node (orchestrator) and a unified Tools node. The agent will iteratively route between the Planner (which decides the next tool to call based on the user's intent or previous tool results) and the Tools node (which executes the chosen tool and returns the result).

**Rationale**: The user explicitly requested an architecture where a single "planner node" determines the sequence of tasks, executes single-purpose tools individually, verifies their success, and loops back to the planner or reports errors to the user. This is best achieved using LangGraph's standard `bind_tools` + `ToolNode` pattern.

**Alternatives considered**: 
- A static linear graph (Node A -> Node B -> Node C): Rejected because the user requested dynamic planning where the agent evaluates success iteratively.
- Sequential hardcoded tools: Rejected for the same reason. 

## 2. Google Sheets API - Automated Tab & Header Creation

**Decision**: Extend the existing `gspread` integration (`GoogleSheetsService`) to include methods for adding new worksheets and populating header rows. 

**Rationale**: `gspread` supports `add_worksheet(title, rows, cols)` and `update(range_name, values)` natively. Since the bot already has the user's credentials and sheet URL, the automated setup tool can easily check for existing tabs (handling the edge case) and create the required structure ("Dashboard" and "Daily Logs" with "Date" and "Weight" columns) gracefully.

**Alternatives considered**:
- `google-api-python-client` (raw API): Overly complex for simple tab creation when `gspread` is already installed and proven.
- Asking users to duplicate a template manually: Rejected as it violates the core requirement: "Let nova create everything".

## 3. Tool Modularity & Error Handling

**Decision**: Create discrete, single-purpose Python functions decorated with `@tool` inside a new `src/nova/agent/tools/` directory. Each tool will wrap the underlying service logic in try/except blocks to return clear string responses (e.g., "Success: Created tabs" or "Error: Insufficient permissions") rather than throwing exceptions that crash the LangGraph.

**Rationale**: The user requested that tools be "basic and simple and be responsible for one thing only", and that errors should be reported back to the user iteratively by the planner.

**Alternatives considered**:
- One monolithic setup tool: Rejected as it violates the single-responsibility requirement.
- Throwing exceptions directly into the graph: Rejected because it crashes the graph instead of allowing the planner to evaluate the error and report it gracefully.