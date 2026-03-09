from unittest import mock
from nova.agent.persona import NOVA_SYSTEM_PROMPT, SETUP_MODE_PROMPT
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


def test_persona_friendly_tone():
    """Assert the prompt conveys a friendly, supportive persona."""
    prompt_lower = NOVA_SYSTEM_PROMPT.lower()
    setup_lower = SETUP_MODE_PROMPT.lower()

    # Main persona: supportive, gentle, encouraging
    assert (
        "supportive" in prompt_lower
        or "encouraging" in prompt_lower
        or "gentle" in prompt_lower
    )

    # Setup mode: warm opener (e.g. "Let's get to know you")
    assert "friendly" in setup_lower or "let's" in setup_lower or "warm" in setup_lower


def test_invoke_llm_appends_system_prompt():
    """Verify invoke_llm passes the system prompt correctly to the LLM."""
    user = User(
        id=1,
        telegram_id=12345,
        name="TestOperator",
        weight=70,
        height=170,
        is_setup_completed=True,
    )
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


def test_invoke_llm_setup_mode_includes_sheet_instructions():
    """When user has is_setup_completed=False, system prompt includes sheet setup instructions."""
    user = User(
        id=1,
        telegram_id=12345,
        name=None,
        weight=None,
        height=None,
        is_setup_completed=False,
    )
    state = AgentState(user=user, current_message="Hi")

    with (
        mock.patch("nova.agent.nodes.llm.ChatOpenAI") as mock_chat_openai,
        mock.patch("nova.agent.nodes.llm.get_settings") as mock_get_settings,
    ):
        mock_settings = mock.MagicMock()
        mock_settings.openai_api_key = "test-key"
        mock_settings.google_service_account_email = (
            "nova@project.iam.gserviceaccount.com"
        )
        mock_get_settings.return_value = mock_settings

        mock_llm_instance = mock.MagicMock()
        mock_chat_openai.return_value = mock_llm_instance
        mock_llm_with_tools = mock.MagicMock()
        mock_llm_instance.bind_tools.return_value = mock_llm_with_tools
        mock_response = mock.MagicMock()
        mock_response.content = "Let's get started!"
        mock_llm_with_tools.invoke.return_value = mock_response

        invoke_llm(state)

        messages = mock_llm_with_tools.invoke.call_args[0][0]
        system_content = messages[0].content

        # Sheet setup instructions must be present
        assert (
            "sheet" in system_content.lower() or "spreadsheet" in system_content.lower()
        )
        assert "share" in system_content.lower() or "editor" in system_content.lower()
        # Service account email when configured
        assert "nova@project.iam.gserviceaccount.com" in system_content
