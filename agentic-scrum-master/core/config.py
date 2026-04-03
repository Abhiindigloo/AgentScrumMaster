from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Centralized application configuration loaded from environment variables."""

    APP_NAME: str = "AgentScrumMaster"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    DATABASE_URL: str = "sqlite:///./agentscrummaster.db"

    JIRA_BASE_URL: str = ""
    JIRA_API_TOKEN: str = ""
    JIRA_EMAIL: str = ""

    SLACK_BOT_TOKEN: str = ""
    SLACK_SIGNING_SECRET: str = ""

    LLM_PROVIDER: str = "openai"
    LLM_MODEL: str = "gpt-4"
    LLM_API_KEY: str = ""
    LLM_TEMPERATURE: float = 0.3
    LLM_MAX_TOKENS: int = 1024

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


@lru_cache()
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
