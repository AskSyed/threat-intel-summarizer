from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Threat Intelligence Summarizer"
    environment: str = "local"
    database_url: str = "sqlite:///./threat_intel.db"

    class Config:
        env_file = ".env"


settings = Settings()
