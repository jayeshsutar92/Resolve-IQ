from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    app_name: str = Field(default="AI Complaint Management API")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=False)
    
    database_url: str = Field(..., description="PostgreSQL async connection URL")
    
    groq_api_key: str = Field(..., description="API key for Groq")
    groq_model_name: str = Field(default="llama-3.1-8b-instant", description="Groq model to use")
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
