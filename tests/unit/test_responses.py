from unittest import mock
from nova.agent.persona import NOVA_SYSTEM_PROMPT
from nova.agent.nodes.llm import invoke_llm
from nova.agent.state import AgentState
from nova.database.models import User


def test_persona_enforces_brevity():
    """Assert the prompt contains explicit instructions against filler and for brevity."""
    prompt_lower = NOVA_SYSTEM_PROMPT.lower()

    # Must explicitly demand short responses
    assert "short" in prompt_lower or "brief" in prompt_lower

    # Must explicitly forbid conversational filler
    assert "filler" in prompt_lower or "conversational filler" in prompt_lower


def test_invoke_llm_appends_system_prompt():
    """Verify invoke_llm passes the system prompt correctly to the LLM."""
    user = User(name="TestOperator", weight=70, height=170)
    state = AgentState(user=user, current_message="Hi")

    with mock.patch("nova.agent.nodes.llm.ChatOpenAI") as mock_chat_openai:
        mock_llm_instance = mock.MagicMock()
        mock_chat_openai.return_value = mock_llm_instance

        # mock bind_tools
        mock_llm_with_tools = mock.MagicMock()
        mock_llm_instance.bind_tools.return_value = mock_llm_with_tools

        mock_response = mock.MagicMock()
        mock_response.content = "Test response"
        mock_llm_with_tools.invoke.return_value = mock_response

        result = invoke_llm(state)

        assert result["messages"][0].content == "Test response"

        # Verify it was invoked
        mock_llm_with_tools.invoke.assert_called_once()

        # Extract the messages sent to the LLM
        messages = mock_llm_with_tools.invoke.call_args[0][0]

        # The first message must be a SystemMessage containing the NOVA persona
        assert messages[0].type == "system"
        assert NOVA_SYSTEM_PROMPT in messages[0].content
