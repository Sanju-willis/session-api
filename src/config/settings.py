# src\config\settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    LANGRAPH_DB_PATH: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    OPENAI_API_KEY: str

    # CORS settings - Fixed
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"
    CORS_CREDENTIALS: bool = True

    # API settings
    API_TITLE: str = "Session API"
    API_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    LOG_LEVEL: str = "ERROR"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")


settings = Settings()
