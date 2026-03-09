# Feature Specification: Google Sheet Service Account Prompt

**Feature Branch**: `007-sheet-editor-prompt`  
**Created**: 2026-03-09  
**Status**: Draft  
**Input**: User description: "user should also be able to enter the servie accont to their google sheets as an editor so update the prompt that guides people how to setup google sheet and mention that they should add a user as an editor. FOr that user read that from env var under config. basically create a new field for google service user under settings nad update the prompt to guide the user better and contine from the last spec(007) dont create a new 001 spec @specs"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - See Updated Sheet Setup Instructions (Priority: P1)

Users configuring their Google Sheet integration receive a prompt containing the specific service account email they need to add as an editor, eliminating guesswork.

**Why this priority**: Without adding the service account as an editor, the bot cannot write to the user's sheet. Providing the exact email to add is critical for the integration to function.

**Independent Test**: Can be fully tested by triggering the sheet setup onboarding flow and verifying that the prompt contains the service account email read from the environment configuration.

**Acceptance Scenarios**:

1. **Given** the system is configured with a service account email, **When** the user reaches the Google Sheet setup step in onboarding, **Then** they see a prompt instructing them to share their sheet with that specific email address as an "Editor".

### Edge Cases

- What happens when the service account email is not configured in the environment variables? (Should the system fallback to a default message, or prevent the onboarding flow?)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST read the Google Service Account Email from environment variables/configuration settings.
- **FR-002**: System MUST include the configured service account email in the Google Sheet setup instructions prompt.
- **FR-003**: System MUST explicitly instruct the user to grant "Editor" access to the provided service account email.
- **FR-004**: System MUST gracefully handle the scenario where the service account email is not configured in the environment variables.

### Key Entities

- **Configuration Settings**: Stores the `GOOGLE_SERVICE_ACCOUNT_EMAIL` read from environment variables.
- **Setup Prompt**: The message template used to guide users through the Google Sheet integration.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of users reaching the Google Sheet setup step are provided with the exact service account email to add as an editor.
- **SC-002**: Reduce user confusion/errors related to Google Sheet permission issues by 80%.
