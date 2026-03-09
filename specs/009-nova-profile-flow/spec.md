# Feature Specification: Nova Profile Setup Flow (Group & Private)

**Feature Branch**: `009-nova-profile-flow`  
**Created**: 2026-03-09  
**Status**: Draft  
**Input**: User description: "Ok so every conversation in a group happens under /nova command we dont have any other commands so flow should be like this. If a user messaged privately first time let it know you need to setup profile please start by entering your name. and then continue with the process. If a user triggered bot with /nova command in any group and has no profile let it know in that group you need to setup your profile first and then message that user in private dm to let it know we are ready to setup please enter your name and continue with rest of the setup"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - First-Time User Messages Privately (Priority: P1)

A user with no profile messages the bot in a private chat for the first time. The bot informs them they need to set up their profile, asks them to start by entering their name, and continues the onboarding flow (name → weight → height → sheet URL) in that same private conversation.

**Why this priority**: Direct private onboarding is the simplest path and must work before the group flow.

**Independent Test**: Send a first message in private as an unregistered user; verify the bot asks for name and proceeds through the full setup.

**Acceptance Scenarios**:

1. **Given** the user has no profile, **When** they send any message in a private chat, **Then** the bot replies "You need to set up your profile. Please start by entering your name."
2. **Given** the user has no profile and just received the name prompt, **When** they reply with their name, **Then** the bot continues with weight, then height, then sheet URL until registration is complete.

---

### User Story 2 - First-Time User Uses /nova in Group (Priority: P1)

A user with no profile triggers the bot with `/nova` in a group, channel, or topic. The bot replies in that group that they need to set up their profile first, then sends a private DM saying the bot is ready to set up and asks them to enter their name. The full onboarding flow (name, weight, height, sheet URL) continues in the private DM.

**Why this priority**: Enables discovery from group contexts while keeping profile setup private.

**Independent Test**: Send `/nova` in a group as an unregistered user; verify in-group reply plus DM that starts the name prompt and completes setup in DM.

**Acceptance Scenarios**:

1. **Given** the user has no profile, **When** they send `/nova` in a group, **Then** they see an in-group reply: "You need to set up your profile first."
2. **Given** the user has no profile and just used `/nova` in a group, **When** the bot sends the DM, **Then** the DM says the bot is ready to set up and asks them to enter their name, and the rest of the flow (weight, height, sheet) continues in the DM.

---

### User Story 3 - Group Conversation Only via /nova (Priority: P2)

In groups, channels, and topics, the only way to interact with the bot is via the `/nova` command. There are no other commands; free text is ignored.

**Why this priority**: Keeps group behavior simple and predictable.

**Independent Test**: In a group, free text is ignored; `/nova &lt;message&gt;` is processed.

**Acceptance Scenarios**:

1. **Given** a registered user in a group, **When** they send free text, **Then** the bot does not respond.
2. **Given** a registered user in a group, **When** they send `/nova &lt;message&gt;`, **Then** the bot processes and replies in that group.

---

### Edge Cases

- What happens if the bot cannot send a DM (e.g., user has blocked the bot or restricted DMs)?
- How does the bot behave when a first-time private user sends a command like `/nova` vs plain text?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: In groups, channels, and topics, the system MUST process only `/nova` commands; free text MUST be ignored.
- **FR-002**: When a first-time user (no profile) messages in private chat, the system MUST tell them to set up their profile, ask for their name first, and continue the full onboarding flow in that private chat.
- **FR-003**: When a first-time user sends `/nova` in a group, the system MUST reply in the group that they need to set up their profile first, then send a DM stating the bot is ready to set up and asking for their name, and continue the onboarding flow (name, weight, height, sheet URL) in the DM.
- **FR-004**: Profile setup (name, weight, height, sheet URL) MUST occur exclusively in private messaging.
- **FR-005**: In private chat, registered users MAY send free text; no `/nova` required.

### Key Entities

- **Profile / User**: A registered user who has completed onboarding (name, weight, height, sheet URL).
- **Onboarding Flow**: The sequence name → weight → height → sheet URL; always runs in private chat.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of first-time private messages receive the profile setup prompt and can complete onboarding inline.
- **SC-002**: 100% of first-time `/nova` in groups receive the in-group notice plus a DM that starts the setup flow and allows completion in DM.
- **SC-003**: Zero free-text messages in groups trigger a bot response; only `/nova` does.
