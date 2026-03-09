# Feature Specification: Group Onboarding & Gamified Health Dashboard Integration

**Feature Branch**: `005-group-onboarding-prompt`
**Created**: 2026-03-08
**Status**: Draft
**Input**: User descriptions: 
1. "When I trigger bot using /nova and user is not created account it should let user know that in order to create a new account you should message privately or something like that"
2. "Ok so we have a sql database that should be our main source of truth and google sheet is basically a user interface. A data visualizer kind of... When setting up the user profile user should also enter the google sheet api and its credentials."
3. "Ok so I want this app to be a video game style health tracker so I will use google sheets to display graphs, visualize data etc etc. for now lets just track basic info about me like daily weight... I want a dashboard that displays my goals and current stats."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Graceful Group Onboarding Redirection (Priority: P1)

When an unknown/unregistered user attempts to trigger the bot in a group chat or topic using the `/nova` command, the bot should explicitly instruct them to send a direct message (DM) to the bot to complete the onboarding process, rather than attempting to onboard them publicly in the group.

**Why this priority**: Attempting to onboard a user in a public group chat exposes their personal health data (weight, height, name) to everyone in the channel, violating privacy. Standard onboarding uses a `ConversationHandler` which can easily break or cross-contaminate in a multi-user group chat.

**Independent Test**: Can be tested by having a brand new user (who has never messaged the bot) type `/nova hello` in a group chat, and verifying the bot replies with a message asking them to DM the bot to register, instead of asking for their name/weight publicly.

**Acceptance Scenarios**:

1. **Given** an unregistered user is in a group chat, **When** they send `/nova what is my HP?`, **Then** the bot replies tagging the user, stating they are not recognized and providing a link or instruction to DM the bot to create an account.
2. **Given** an unregistered user is in a private direct message with the bot, **When** they send a message, **Then** the bot initiates the standard private onboarding flow (asking for name, weight, height, and Google Sheets credentials).

### User Story 2 - Gamified Dashboard Initialization via Onboarding (Priority: P1)

When users are setting up their profile in a private DM, they should be prompted to provide Google Sheets API credentials/link. The system will use this sheet as a "video game style health tracker" UI. The sheet must have a standardized structure starting with a "Dashboard" tab (displaying goals, current stats, and progress graphs) and a "Daily Logs" tab for raw data tracking.

**Why this priority**: The gamified aspect relies on a visual dashboard. Setting up the correct tabs ("Dashboard", "Daily Logs") ensures the user has immediate visual feedback on their stats and goals, and credentials must be collected securely during private onboarding.

**Independent Test**: Can be tested by completing private onboarding and verifying that the bot asks for a Google Sheet ID, successfully validates access, and pushes data to populate the "Dashboard" and adding an initial row in "Daily Logs".

**Acceptance Scenarios**:

1. **Given** a user is creating a new profile in a DM, **When** they reach the sheet setup step, **Then** the bot asks them to provide their Google Sheet connection details.
2. **Given** a user provides their Google Sheet details, **When** the bot verifies access, **Then** it confirms the connection, saves the configuration in the SQLite database, and ensures the required tabs ("Dashboard" and "Daily Logs") exist.

### User Story 3 - Daily Stat Tracking (Weight) (Priority: P1)

Users should be able to report their daily stats, starting with weight (e.g., "today I weigh 74 kilo"). The bot will update the SQLite database (the source of truth) and then update that specific day's row in the "Daily Logs" tab of the Google Sheet. 

**Why this priority**: Tracking daily metrics in a time-series format (one row per day) is the foundation of the health tracker, allowing the Google Sheet to generate graphs and visualize progress on the Dashboard.

**Independent Test**: Can be tested by sending "I weigh 74kg today" to the bot, verifying the bot confirms it, and then checking the Google Sheet's "Daily Logs" tab to see a new or updated row for today's date with the value "74".

**Acceptance Scenarios**:

1. **Given** a user reports a daily stat like weight, **When** the bot processes the message, **Then** it saves the data to the SQLite database and writes/updates the row corresponding to today's date in the "Daily Logs" Google Sheet tab.
2. **Given** the "Daily Logs" tab is updated, **When** the user opens their Google Sheet, **Then** the "Dashboard" tab's graphs and current stats automatically reflect the new data.

### Edge Cases

- What happens if the user clicks the bot's handle from the group chat to DM it?
  - *Assumption*: Telegram handles this natively. Once in the DM, they will need to send `/start` or a regular message, which triggers the existing private onboarding flow.
- Does the bot try to "save" the command they attempted in the group chat for after they register?
  - *Assumption*: No. The bot drops the original command. The user must re-issue their query after registration.
- What happens if the user reports their weight multiple times in one day?
  - *Assumption*: The bot should update/overwrite the existing row for that specific date in the "Daily Logs" tab, rather than creating duplicate rows for the same day.
- What happens if the user's sheet doesn't have the "Dashboard" or "Daily Logs" tabs?
  - *Assumption*: Every user MUST have the exact same tabs and page structures. The bot should alert the user if their sheet is missing the required gamified template.
- What if the Google Sheets API is temporarily down when writing an update?
  - *Assumption*: The bot should log the sync failure but MUST NOT crash. SQLite remains the source of truth, and the sheet can be synced later.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST detect if the user invoking the `/nova` command in a group or topic has a registered profile in the SQLite database.
- **FR-002**: If the user is NOT registered, and the context is a group or topic, the system MUST reply with a public message directing the user to private message the bot to register, and MUST NOT initiate the data-entry prompt.
- **FR-003**: The system MUST prompt for and securely store user-specific Google Sheet details/credentials exclusively during the private profile setup/onboarding flow.
- **FR-004**: The system MUST treat the SQLite database as the sole source of truth for all read operations, memory, and LLM context injections.
- **FR-005**: The system MUST NEVER read data from the Google Sheet for determining bot behavior or answering user questions.
- **FR-006**: The system MUST enforce a standardized sheet template across all users, consisting of at least:
  - **"Dashboard" (Tab 1)**: Visualizes goals, current stats, and progress (graphs/charts).
  - **"Daily Logs" (Tab 2)**: A time-series data table where each row represents a single day (Columns: Date, Weight, etc.).
- **FR-007**: The system MUST write updates to the "Daily Logs" tab when a user reports a daily metric, matching the row by the current date (inserting a new row if it's the first report of the day, or updating the existing row).

### Key Entities

- **Gamified Dashboard (UI Visualizer)**: The external Google Sheet acting strictly as a read-only visual interface. It features a main "Dashboard" for stats/graphs and a "Daily Logs" tab for raw daily metrics.
- **Daily Metric**: A measurement (e.g., Weight) recorded for a specific date. Stored in SQLite and synced to the corresponding date row in the Google Sheet.
- **SQLite Database**: The core relational database acting as the primary source of truth for all bot operations, state, and context.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of unregistered users attempting to use `/nova` in a group receive a redirection message instead of a data-entry prompt.
- **SC-002**: 100% of read operations for user state/profile variables are executed against the SQLite database.
- **SC-003**: Reporting a daily weight via chat successfully adds or updates a row for the current date in the "Daily Logs" tab of the user's Google Sheet.
- **SC-004**: The Google Sheet effectively serves as a one-way visualizer, where the "Dashboard" tab automatically reflects the latest data written to the "Daily Logs" tab.
- **SC-005**: Users manually changing their Google Sheets data does not affect the bot's internal memory or responses (validating the write-only architecture).