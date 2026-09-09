from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Bot
    bot_token: str = Field(..., description="Telegram bot token")
    
    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/english_bot",
        description="PostgreSQL connection URL"
    )
    
    # AI
    openai_api_key: str | None = Field(default=None, description="OpenAI API key")
    
    # Speech
    tts_provider: str = Field(default="google", description="TTS provider: google, openai, elevenlabs")
    stt_provider: str = Field(default="google", description="STT provider: google, whisper")
    
    # App
    debug: bool = Field(default=False)
    log_level: str = Field(default="INFO")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
