"""
App-wide configuration loaded from environment variables.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """All settings are read from .env or real environment variables."""

    # Database
    DATABASE_URL: str = "sqlite:///./flowbot.db"

    # LLM
    OPENAI_API_KEY: str = "sk-placeholder"
    OPENAI_MODEL: str = "gpt-3.5-turbo"

    # App
    LOG_LEVEL: str = "INFO"
    APP_ENV: str = "development"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Single shared instance — import this everywhere
settings = Settings()
