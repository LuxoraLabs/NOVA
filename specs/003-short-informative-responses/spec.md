# Feature Specification: Short Informative Responses

**Feature Branch**: `003-short-informative-responses`  
**Created**: 2026-03-08  
**Status**: Draft  
**Input**: User description: "I want agent to give short but informative responses"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Concise Conversational Output (Priority: P1)

Users interacting with the AI bot should receive responses that are brief, direct, and dense with information, avoiding unnecessary fluff, long conversational preamble, or excessive markdown formatting unless explicitly requested.

**Why this priority**: Long-winded AI responses create friction in a mobile or chat-based environment like Telegram. Users tracking their health metrics need immediate, actionable feedback without having to scroll through paragraphs of conversational filler.

**Independent Test**: Can be tested by asking the bot a complex or open-ended question (e.g., "What should I eat after a workout?") and verifying that the response is structured concisely (e.g., under 3-4 sentences or a brief list) while still answering the core question.

**Acceptance Scenarios**:

1. **Given** a user asks a simple question like "Logged my 5k run", **When** the bot processes the message, **Then** it replies with a short, punchy acknowledgment and stat update (e.g., "Stamina drained, Max HP capacity increased. Good work, operator.") rather than a multi-paragraph explanation.
2. **Given** a user asks for advice like "What's a good post-workout meal?", **When** the bot processes the message, **Then** it provides a brief, bulleted list of 2-3 actionable items without a lengthy introduction or conclusion.

### Edge Cases

- What happens if the user explicitly asks for a "long explanation" or "detailed breakdown"?
  - *Assumption*: The bot should respect the user's explicit request for detail, overriding the default brevity constraint for that specific interaction.
- What happens if the bot needs to explain a complex medical or nutritional concept?
  - *Assumption*: The bot will provide a high-level summary (the "TL;DR") first, and optionally invite the user to ask for more details if they want to dig deeper.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST constrain the AI's response length by default, aiming for brevity and information density.
- **FR-002**: The system MUST instruct the AI to omit conversational filler phrases (e.g., "As an AI...", "I understand you want to...", "Here is the information you requested").
- **FR-003**: The system MUST allow the AI to bypass the brevity constraint ONLY IF the user explicitly requests a long, detailed, or comprehensive explanation in their prompt.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Average word count of the assistant's standard responses is reduced compared to baseline, ideally staying under 50-75 words for standard interactions.
- **SC-002**: 100% of test queries result in responses that lack generic AI preamble or filler text.
- **SC-003**: User satisfaction (qualitatively measured during testing) remains high because the core question is still answered despite the shorter length.