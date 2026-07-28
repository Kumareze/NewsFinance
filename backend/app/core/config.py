from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = Field(default="FinPulse API")
    APP_VERSION: str = Field(default="1.0.0")
    ENV: str = Field(default="development")
    
    # API Router Prefix
    API_V1_STR: str = "/api/v1"
    
    # Database Settings
    DATABASE_URL: str = Field(default="postgresql://postgres:postgres@localhost:5432/finpulse")
    
    # Scraper Settings
    SCRAPER_INTERVAL: int = Field(default=30)  # in minutes
    
    # Security Settings
    SECRET_KEY: str = Field(default="super-secret-development-key-change-in-production")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
