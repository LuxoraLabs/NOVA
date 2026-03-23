# Feature Specification: N.O.V.A. MVP Comm Link

**Feature Branch**: `001-health-bot-mvp`  
**Created**: 2026-03-08  
**Status**: Draft  
**Input**: User description: "Ok so i want to create a helth tracking personal ai asistant: ... Project: Telegram-based AI Fitness & Nutrition Agent (@NovaMaxHP_bot) ... Sprint v0.1: The Comm Link (MVP Foundation) ... Goal: Establish the bidirectional text pipeline between Telegram, LangGraph, and a text-only LLM. ... "

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Establish Basic Conversation (Priority: P1)

Users can send a text message to the AI assistant via the messaging platform and receive an immediate, contextual response in the N.O.V.A. persona.

**Why this priority**: This establishes the core foundation (Sprint v0.1) for bidirectional text communication. Without it, the assistant cannot deliver value or handle more advanced features.

**Independent Test**: Can be fully tested by sending a standard text greeting to the assistant's handle and verifying that it replies accurately embodying the gamified, health-focused N.O.V.A. persona.

**Acceptance Scenarios**:

1. **Given** a user has started a chat session with the assistant, **When** they send a standard text message, **Then** they receive a text reply from the AI in the N.O.V.A. persona.
2. **Given** an ongoing active conversation, **When** a user asks a follow-up question referencing a previous topic, **Then** the bot replies accurately incorporating context from the conversation history.

---

### User Story 2 - Omnichannel Profile Sync (Priority: P1)

Users can interact with the AI assistant in both private direct messages and group channels. The assistant always replies in the same location the message was sent from, while maintaining a single, synchronized user profile and memory across all locations.

**Why this priority**: Ensuring users can talk to the bot in their preferred context (private or public) without losing their health tracking history is core to a personal assistant's utility.

**Independent Test**: Can be tested by sending a message in a private chat that updates the user's state, then messaging the bot in a group channel and verifying the bot references the context from the private chat, and replies directly in the channel.

**Acceptance Scenarios**:

1. **Given** a user interacts with the bot in a private chat, **When** they later mention the bot in a group channel, **Then** the bot replies in the group channel and incorporates context from the private chat.
2. **Given** a user interacts in a channel, **When** the bot replies, **Then** the reply is sent to that specific channel, not as a private direct message.

---

### User Story 3 - New User Onboarding (Priority: P1)

When a user messages the bot for the very first time, they are greeted with an onboarding prompt that allows them to create an account by providing basic physical and personal details (e.g., name, weight, height). The assistant uses these details to personalize future interactions.

**Why this priority**: Without baseline physical data and a user profile, the AI cannot accurately calculate or track "HP" and "Stamina", which is the core functionality of the gamified health agent.

**Independent Test**: Can be tested by messaging the bot from a brand new account and verifying that it immediately initiates the account creation flow before allowing standard conversation.

**Acceptance Scenarios**:

1. **Given** a user who has never interacted with the bot, **When** they send their first message, **Then** the bot replies with a simple menu or prompt asking them to create an account.
2. **Given** a user in the onboarding flow, **When** they provide their name, weight, and height, **Then** the system saves this to their unified profile and transitions them to the standard active state.

### Edge Cases

- What happens when a user sends a non-text message (e.g., sticker, photo, voice recording)?
  - *Assumption*: The system will gracefully inform the user that only text messages are supported in this version.
- What happens if the AI processing engine times out or encounters an error?
  - *Assumption*: The system will provide a friendly, persona-aligned error message indicating temporary communication failure and suggesting the user try again.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST listen for and receive standard text messages from users via the designated messaging platform.
- **FR-002**: The system MUST maintain conversation state for each active user, securely storing their unique identifier, the current message, and the recent conversation history.
- **FR-003**: The system MUST process incoming messages using an AI engine instructed to adopt the N.O.V.A. persona (gentle, gamified, health and longevity focus, tracking HP and Stamina).
- **FR-004**: The system MUST route the generated AI response back to the correct user on the messaging platform.
- **FR-005**: The system MUST handle unsupported message types gracefully, sending a fallback text response.
- **FR-006**: The system MUST be capable of receiving and responding to messages in both private direct messages and group channels/chats.
- **FR-007**: The system MUST ensure that when responding, the reply is sent to the exact chat context (private or channel) from which the triggering message originated.
- **FR-008**: The system MUST maintain a single, synchronized global user profile and history for each unique user, regardless of whether they interact via private chat or a group channel.
- **FR-009**: The system MUST persist users, messages, and conversation graph states in a database. When a message is received, the orchestrator MUST fetch the user's graph state and profile information using their unique identifier (Telegram ID) to provide accurate context for the AI response.
- **FR-010**: The system MUST detect when a user is interacting for the first time and automatically trigger an onboarding flow (via a simple menu or prompt) to create an account.
- **FR-011**: The system MUST collect and store basic user details (e.g., name, weight, height) during the onboarding flow before permitting standard health tracking conversation.

### Key Entities

- **User**: Represents the individual interacting with the system, uniquely identified by their messaging platform ID (e.g., Telegram ID), storing their profile data (name, weight, height, etc.) and unified preferences.
- **Message**: Represents a single communication event (inbound or outbound), linked to a User, storing the content, timestamp, and chat context (private/channel).
- **Graph State / User State**: Represents the current conversational and orchestration context for a user, containing the `user_id`, `current_message`, `chat_history`, and current step in the AI flow.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The assistant successfully responds to 95% of text messages within 5 seconds of receipt.
- **SC-002**: Users can complete a multi-turn conversation (minimum of 3 back-and-forth exchanges) where the assistant demonstrably remembers context from the first message.
- **SC-003**: Manual test conversations show a 100% success rate of the AI responding in the defined N.O.V.A. persona (gentle, gamified, health-focused) rather than a generic AI response.