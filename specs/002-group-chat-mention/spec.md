# Feature Specification: Group Chat Mention Requirement

**Feature Branch**: `002-group-chat-mention`  
**Created**: 2026-03-08  
**Status**: Draft  
**Input**: User description: "Ok so whenever a user messages privetly respond to them direclt but if user is in a group channel or a topic user must mention the bot first to create a response."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Private Message Direct Response (Priority: P1)

Users interacting with the AI bot in a private 1-on-1 direct message should receive a response to every message they send, without needing to explicitly mention the bot's name or handle.

**Why this priority**: Private direct messaging is the primary and most intimate way users will interact with their health agent. Expecting them to mention the bot in a private chat creates unnecessary friction.

**Independent Test**: Can be tested by sending a standard text message (without a mention) to the bot in a private chat and verifying that the bot responds.

**Acceptance Scenarios**:

1. **Given** a user is in a private direct message with the bot, **When** they send a message like "I just ran 5km", **Then** the bot responds normally based on its persona.
2. **Given** a user is in a private direct message with the bot, **When** they send a message mentioning the bot like "@NovaMaxHP_bot I just ran 5km", **Then** the bot responds normally based on its persona and does not throw an error.

---

### User Story 2 - Group Chat Explicit Mention Requirement (Priority: P1)

Users interacting with the AI bot in a group chat or a topic-based channel must explicitly mention the bot (e.g., using `@bot_handle`) for the bot to read, process, and respond to the message. Messages in group chats that do not mention the bot should be completely ignored.

**Why this priority**: In a group chat, multiple people are talking to each other. If the bot responds to every message, it creates massive spam, ruins the group experience, and rapidly depletes API credits.

**Independent Test**: Can be tested by adding the bot to a group chat, sending a message without mentioning it (verifying silence), and then sending a message explicitly mentioning it (verifying a response).

**Acceptance Scenarios**:

1. **Given** the bot is present in a group chat, **When** User A sends a message "How are you guys doing?" without mentioning the bot, **Then** the bot ignores the message and does not respond.
2. **Given** the bot is present in a group chat, **When** User A sends a message "@NovaMaxHP_bot what is my current HP?" **Then** the bot processes the message and replies specifically to User A in the group chat.

### Edge Cases

- What happens if a user mentions the bot in a group chat, but the message only contains the mention and no actual command/text (e.g., just "@NovaMaxHP_bot")?
  - *Assumption*: The bot will respond with a friendly, persona-aligned greeting asking how it can assist the operator.
- What happens if the bot is mentioned in a forwarded message or a reply within a group chat?
  - *Assumption*: As long as the bot's handle is present in the text payload of the event it receives, it will process the text.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST evaluate the context (private vs. group/channel) of every incoming message.
- **FR-002**: If the context is a private direct message, the system MUST process and respond to the message automatically.
- **FR-003**: If the context is a group chat or channel, the system MUST check the message text for the bot's explicit @mention handle.
- **FR-004**: In group chats, if the bot's handle is NOT found in the message text, the system MUST drop/ignore the message without saving it or invoking the LLM.
- **FR-005**: In group chats, if the bot's handle IS found, the system MUST strip the mention handle from the text (to avoid confusing the LLM) before processing and responding.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of messages sent in private DMs without mentions successfully trigger a bot response.
- **SC-002**: 100% of messages sent in group chats without mentioning the bot are successfully ignored (0 LLM invocations, 0 DB writes for these events).
- **SC-003**: 100% of messages sent in group chats that explicitly mention the bot trigger a successful, contextual response.