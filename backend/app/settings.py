from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    GROQ_API_KEY: str = Field(..., env="GROQ_API_KEY")
    GROQ_MODEL: str = Field("llama-3.3-70b-versatile", env="GROQ_MODEL")
    GROQ_TEMPERATURE: float = Field(0.7, env="GROQ_TEMPERATURE")
    APP_NAME: str = Field("Resume Agent", env="APP_NAME")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

def get_settings() -> Settings:
    """Return app settings (singleton style)"""
    return Settings()

# Why: Pydantic settings centralize environment config and are required in BRD