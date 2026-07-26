"""
config.py
Loads configuration from environment variables using Pydantic Settings.
Keeps our app configuration centralized and type-safe.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    app_name: str = Field(default="AI Complaint Management API")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=False)
    
    # Database
    database_url: str = Field(..., description="PostgreSQL async connection URL")
    
    # LLM (Groq)
    groq_api_key: str = Field(..., description="API key for Groq")
    groq_model_name: str = Field(default="gemma2-9b-it", description="Groq model to use")
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

# Global settings instance
settings = Settings()
