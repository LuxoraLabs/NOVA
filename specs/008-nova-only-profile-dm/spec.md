# Feature Specification: Nova-Only Commands with Profile Setup via DM

**Feature Branch**: `008-nova-only-profile-dm`  
**Created**: 2026-03-09  
**Status**: Draft  
**Input**: User description: "i only want to send bot a message using /nova command. I no longer want /start command in the bot. If I message using nova and user has no profile yet it should let user know you need to setup your profile we send you a message privetly check that and create a profile. And then conversation should continue in private messaging."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Unregistered User Uses /nova (Priority: P1)

An unregistered user sends `/nova` (in a group or privately). The bot informs them they must set up a profile first, tells them a private message was sent, and instructs them to check their DMs to create a profile. The bot also sends a direct message to the user with a clear way to begin profile setup.

**Why this priority**: Without this flow, unregistered users cannot onboard. It is the first interaction most new users will have.

**Independent Test**: Can be tested by sending `/nova` as an unregistered user and verifying the public/private reply plus the DM containing the setup trigger.

**Acceptance Scenarios**:

1. **Given** the user has no profile, **When** they send `/nova` in a group chat, **Then** they see a reply instructing them to check their private messages to create a profile, and they receive a DM with instructions to begin setup.
2. **Given** the user has no profile, **When** they send `/nova` in a private chat, **Then** they receive instructions to create a profile (either inline or via a DM they already have).

---

### User Story 2 - Remove /start Command (Priority: P1)

The bot no longer responds to `/start`. Profile setup is initiated exclusively through the flow provided in the DM when an unregistered user uses `/nova`.

**Why this priority**: Core requirement to simplify entry point to `/nova` only.

**Independent Test**: Sending `/start` yields no onboarding behavior; setup is triggered only via the DM flow from Story 1.

**Acceptance Scenarios**:

1. **Given** any user, **When** they send `/start`, **Then** the bot does not start onboarding (no name/weight/height prompts).
2. **Given** an unregistered user, **When** they complete profile setup via the DM flow, **Then** they have a created profile and can interact with the bot (direct messages in private chat; `/nova` in groups, channels, or topics).

---

### User Story 3 - Registered User Interacts with Bot (Priority: P2)

Once a user has a profile, interaction differs by context:

- **Private chat**: The user can message the bot directly (free text); no `/nova` command is required.
- **Group, channel, or topic**: The user MUST use the `/nova` command to interact with the bot. Direct messages are ignored.

The bot processes the request and replies in the same context where it was sent.

**Why this priority**: Private chat allows natural conversation; groups/channels/topics require explicit invocation to avoid noise and accidental triggers.

**Independent Test**: Registered user sends free text in private chat and receives a reply; registered user sends `/nova` in a group/channel/topic and receives a reply in that context.

**Acceptance Scenarios**:

1. **Given** a registered user, **When** they send a direct message (free text) in a private chat, **Then** the bot processes the message and replies.
2. **Given** a registered user, **When** they send `/nova` in a group chat, **Then** the bot processes the message and replies in that group.
3. **Given** a registered user, **When** they send `/nova` in a channel or topic thread, **Then** the bot processes the message and replies in that channel or thread.
4. **Given** a registered user, **When** they send a direct message (free text) in a group, channel, or topic, **Then** the bot ignores the message (does not respond).

---

### Edge Cases

- What happens if the bot cannot send a DM to the user (e.g., user has blocked the bot or has restricted DMs)?
- How does the bot behave if `/nova` is sent without any message text (e.g., `/nova` alone)?
- Free text in groups, channels, or topics is ignored (no reply).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: In private chat, the system MUST process direct messages (free text) from registered users. In groups, channels, or topics, the system MUST process messages only when prefixed with the `/nova` command; direct messages in those contexts MUST be ignored.
- **FR-002**: System MUST NOT respond to `/start` with onboarding flows.
- **FR-003**: When an unregistered user sends `/nova`, the system MUST inform them that a private message was sent and they must create a profile.
- **FR-004**: The system MUST send a direct message to the unregistered user with a clear way to begin profile setup. Profile registration MUST occur exclusively in private messaging.
- **FR-005**: Once a user has a profile, the system MUST process direct messages in private chat and `/nova` commands in groups, channels, or topics, replying in the same context.

### Key Entities

- **Profile / User**: Represents a registered user who has completed setup (name, weight, height, sheet URL).
- **Onboarding Flow**: The sequence of collecting name, weight, height, and sheet URL; triggered from the DM sent to unregistered users (not from `/start`). Registration MUST occur in private messaging only.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of unregistered users who use `/nova` receive both an in-context reply and a DM with profile setup instructions.
- **SC-002**: Zero onboarding flows are triggered by `/start`.
- **SC-003**: Registered users can interact with the bot in private chat via direct messages, and in groups/channels/topics via `/nova`, with responses delivered within 5 seconds under normal load.
