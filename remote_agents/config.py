from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# env file path config
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE_PATH = BASE_DIR / "cirno_questions_generator_agent.env"


# Settings
class Settings(BaseSettings):
    science_and_math_agent_url: str = "http://localhost:4000"
    web_search_agent_url: str = "http://localhost:4002"

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        extra="allow",
        env_prefix="REMOTE_"
    )


settings = Settings()
