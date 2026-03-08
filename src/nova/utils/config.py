from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application configuration"""

    telegram_bot_token: str = Field(min_length=1)
    openai_api_key: str = Field(min_length=1)
    log_level: str = "INFO"
    db_path: str = "nova.db"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


def get_settings() -> Settings:
    """Return the application settings."""
    return Settings()
