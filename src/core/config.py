# src\core\config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DEBUG: bool = False
    LOG_LEVEL: str = "ERROR"
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        case_sensitive=True,
        extra="allow"  # Allow extra fields
    )

settings = Settings()