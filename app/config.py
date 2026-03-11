"""
App-wide configuration loaded from environment variables.
"""

import os
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()


class Settings:
    """All settings are read from .env or real environment variables."""

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./flowbot.db")

    # LLM
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "sk-placeholder")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    # App
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    APP_ENV: str = os.getenv("APP_ENV", "development")


# Single shared instance — import this everywhere
settings = Settings()
