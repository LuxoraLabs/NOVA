import pytest
from pydantic import ValidationError
import os
from unittest import mock


# Remove env vars if they exist to test the isolated behavior
@pytest.fixture(autouse=True)
def clean_env():
    with mock.patch.dict(os.environ, clear=True):
        yield


def test_settings_requires_telegram_bot_token():
    with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
        with pytest.raises(ValidationError) as excinfo:
            from nova.utils.config import Settings

            Settings()

        assert "telegram_bot_token" in str(excinfo.value)


def test_settings_requires_openai_api_key():
    with mock.patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": "test_token"}):
        with pytest.raises(ValidationError) as excinfo:
            from nova.utils.config import Settings

            Settings()

        assert "openai_api_key" in str(excinfo.value)


def test_settings_successful_initialization():
    with mock.patch.dict(
        os.environ, {"TELEGRAM_BOT_TOKEN": "test_token", "OPENAI_API_KEY": "test_key"}
    ):
        from nova.utils.config import Settings

        settings = Settings()
        assert settings.telegram_bot_token == "test_token"
        assert settings.openai_api_key == "test_key"
