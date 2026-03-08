# Feature Specification: Topic Mention Response Support

**Feature Branch**: `004-topic-mention`  
**Created**: 2026-03-08  
**Status**: Draft  
**Input**: User description: "Ok so whenever I mention a bot in a topic it does not respond it should be able to respond whenever it is tagged like it is privetly messaged wheter in a group channel under a topic anyhthing"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Mention Response in Group Topics (Priority: P1)

Users interacting with the AI bot inside a specific Topic (Thread) within a Group channel must receive a direct reply inside that exact same Topic when they explicitly mention the bot.

**Why this priority**: Telegram group chats frequently use Topics (Forums) to organize conversations. If the bot cannot respond within the specific topic it was mentioned in, its utility in group settings is severely broken and confusing to users.

**Independent Test**: Can be tested by creating a Topic in a Telegram Group, mentioning the bot within that Topic, and verifying that the bot's response is threaded correctly into that exact Topic (rather than failing or dropping into a different topic).

**Acceptance Scenarios**:

1. **Given** a user is inside a specific Topic of a Telegram group, **When** they send a message explicitly mentioning the bot (e.g., "@NovaMaxHP_bot what is my HP?"), **Then** the bot processes the request and sends the response back to that exact same Topic.
2. **Given** a user is in a standard group chat (without topics), **When** they explicitly mention the bot, **Then** the bot responds normally in the group chat (preserving existing functionality).

### Edge Cases

- What happens if the bot is mentioned in a topic, but lacks permission to write to that specific topic?
  - *Assumption*: The system will log a permission error and degrade gracefully without crashing.
- Does the bot remember conversation history uniquely per-topic or per-user?
  - *Assumption*: The bot continues to track history based on the User's unified profile (as established in previous features), not isolated by the topic itself.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST detect when a message mentioning the bot originates from a sub-topic (message thread) within a group chat.
- **FR-002**: When responding to a message from a topic, the system MUST route the response back to the specific thread identifier it originated from.
- **FR-003**: The system MUST continue to enforce the explicit mention requirement for all group/topic interactions (ignoring unmentioned messages).
- **FR-004**: The system MUST preserve standard private direct message routing and standard (non-topic) group routing.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of messages explicitly mentioning the bot inside a Group Topic trigger a successful response routed back to the exact same Topic.
- **SC-002**: 0 regressions in existing routing: Private DMs and standard group chats continue to function as expected.
