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
    
    # AI - БЕСПЛАТНЫЕ провайдеры
    llm_provider: str = Field(default="groq", description="LLM provider: groq, gemini, openai")
    groq_api_key: str | None = Field(default=None, description="Groq API key (бесплатный)")
    gemini_api_key: str | None = Field(default=None, description="Google Gemini API key (бесплатный)")
    openai_api_key: str | None = Field(default=None, description="OpenAI API key (платный)")
    
    # Speech - БЕСПЛАТНЫЕ провайдеры
    tts_provider: str = Field(default="edge", description="TTS provider: edge (бесплатный), gtts (бесплатный)")
    stt_provider: str = Field(default="whisper", description="STT provider: whisper (бесплатный), vosk (бесплатный)")
    
    # TTS voices
    tts_voice: str = Field(default="en-US-JennyNeural", description="TTS voice for edge-tts")
    whisper_model: str = Field(default="base", description="Whisper model: tiny, base, small, medium, large")
    
    # App
    debug: bool = Field(default=False)
    log_level: str = Field(default="INFO")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
