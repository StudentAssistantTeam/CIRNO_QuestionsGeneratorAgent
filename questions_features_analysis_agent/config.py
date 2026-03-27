from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# env file path config
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE_PATH = BASE_DIR / "questions_features_analysis_agent.env"


# Settings
class Settings(BaseSettings):
    # LLM config
    llm_model_name: str = ""
    llm_api_key: str = ""
    llm_base_url: str = ""

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        extra="allow"
    )


settings = Settings()
