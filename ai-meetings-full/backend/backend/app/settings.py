from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    ENABLE_GCAL: bool = False
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db/meetings"
    USE_LOCAL_WHISPER: bool = True  # False ⇒ use AssemblyAI
    ASSEMBLYAI_KEY: Optional[str] = None

    class Config:
        env_file = ".env"  # This file should exist in the same folder as settings.py or be correctly referenced

@lru_cache
def get_settings() -> Settings:
    return Settings()
