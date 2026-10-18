from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Threat Intelligence Summarizer"
    environment: str = "local"
    database_url: str = "sqlite:///./threat_intel.db"
    openai_api_key: SecretStr

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
