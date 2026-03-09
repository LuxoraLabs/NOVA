# Feature Specification: Friendlier Prompts and Clear Google Sheet Setup Instructions

**Feature Branch**: `010-friendly-prompts-sheet-setup`  
**Created**: 2026-03-09  
**Status**: Draft  
**Input**: User description: "I want prompts to be more friendly. This agent is a friendly health tracker you can add a little bit persona to prompts just a little bit. Also when setting up google connection it should provide more clear instructions from creating a sheet to the giving edit permission to the service user which is stored in the settings."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Friendlier Agent Persona (Priority: P1)

A user interacts with the health-tracking agent and experiences a warmer, more personable tone. The agent feels like a friendly health companion rather than a transactional system. All prompts and responses—including profile setup, daily tracking, and general conversation—convey a light, supportive personality while remaining brief and helpful.

**Why this priority**: Tone impacts user engagement and retention. A friendly persona makes the agent more approachable and encourages continued use.

**Independent Test**: Interact with the agent across profile setup and typical health-tracking messages; verify tone feels warm and supportive without being verbose.

**Acceptance Scenarios**:

1. **Given** a user starting profile setup, **When** the agent prompts for their name or other details, **Then** the language is warm and encouraging (e.g., "Let's get to know you!" or similar).
2. **Given** a user during routine health tracking, **When** the agent responds to inputs, **Then** responses feel personable and supportive while staying concise.
3. **Given** a user who has missed a goal or had an off day, **When** the agent responds, **Then** the tone is reassuring and non-judgmental.

---

### User Story 2 - Clear Google Sheet Setup Instructions (Priority: P1)

A user needs to connect a Google Sheet for data tracking. The agent provides clear, step-by-step instructions that cover: (1) creating a new blank spreadsheet, (2) sharing the sheet with the correct service account, and (3) granting Editor permission. When the service account email is available in settings, the instructions explicitly state that email so the user knows exactly whom to share with.

**Why this priority**: Unclear setup instructions cause frustration and abandonment. Clear instructions reduce support burden and improve completion rates.

**Independent Test**: Reach the Google Sheet setup step (in profile setup or equivalent flow); verify instructions are step-by-step, unambiguous, and include the service account email when configured.

**Acceptance Scenarios**:

1. **Given** a user who has reached the Google Sheet setup step, **When** the agent presents instructions, **Then** the steps are ordered (e.g., Step 1, Step 2, Step 3) and easy to follow.
2. **Given** the service account email is configured in settings, **When** the user sees the setup instructions, **Then** the instructions explicitly include the service account email and state to share the sheet with that email as Editor.
3. **Given** the service account email is not configured, **When** the user sees the setup instructions, **Then** the instructions still clearly describe how to create a blank sheet and share it with Editor permission, using a fallback phrase (e.g., "our secure service account").
4. **Given** a user following the instructions, **When** they complete the setup, **Then** they understand what URL to provide and where to find it (e.g., from the browser address bar).

---

### Edge Cases

- What happens when the user provides an invalid or non-Google Sheet URL? The agent should respond in a friendly way and ask for a valid sheet URL.
- How does the agent handle a user who asks for help mid-setup? Instructions should be re-statable or linkable without overwhelming the user.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: All agent prompts and responses MUST use a friendly, supportive tone appropriate for a health-tracking companion.
- **FR-002**: Agent persona MUST be warm and personable while keeping responses brief and to the point.
- **FR-003**: When prompting for Google Sheet connection, the system MUST provide step-by-step instructions covering: creating a blank spreadsheet, sharing the sheet, and granting Editor permission.
- **FR-004**: When the service account email is stored in settings, the Google Sheet setup instructions MUST explicitly include that email and instruct the user to share the sheet with it as Editor.
- **FR-005**: When the service account email is not configured, the system MUST still provide complete setup instructions using a generic reference (e.g., "our secure service account").
- **FR-006**: Setup instructions MUST be easy to follow and unambiguous for users unfamiliar with Google Sheets sharing.

### Key Entities

- **Service Account Email**: Stored in system settings; used in setup instructions when available to tell users exactly whom to share the sheet with.
- **Agent Persona**: The tone and personality conveyed through all prompts and responses (friendly health tracker).

## Assumptions & Dependencies

- **Assumptions**: The service account email (when configured) is stored in system settings and accessible when generating setup instructions. The agent already has profile setup and health-tracking flows in place.
- **Dependencies**: Existing profile/setup flow; existing settings or configuration storage for the service account email.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete Google Sheet setup on first attempt when following the provided instructions (measurable via reduced repeat setup attempts or support requests).
- **SC-002**: Agent responses are perceived as friendly and supportive in user testing or feedback.
- **SC-003**: Setup instructions include all necessary steps (create sheet, share, grant Editor, provide URL) without requiring external documentation.
- **SC-004**: When service account email is configured, 100% of setup prompts show that email in the instructions.
