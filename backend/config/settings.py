from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    GROQ_API_KEY: str
    GROQ_MODEL_NAME: str
    ENVIRONMENT: str = "development"
    PORT: int = 8000

    # Add these if you are using them in your code
    resume_data_path: str = str(Path(__file__).parent.parent / "data/resumes")
    jd_data_path: str = str(Path(__file__).parent.parent / "data/jds")
    memory_file: str = str(Path(__file__).parent.parent / "data/memory_store.json")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        # Allow extra fields in .env (optional)
        extra = "allow"

settings = Settings()