#!/usr/bin/env python3
"""
Скрипт для создания структуры проекта English Learning Bot.
Запусти этот скрипт на своём компьютере, и он создаст все необходимые файлы.

Использование:
    python setup_project.py
"""

import os
from pathlib import Path


def create_file(filepath: str, content: str):
    """Создаёт файл с содержимым."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Создан: {filepath}")


def setup_project():
    """Создаёт всю структуру проекта."""
    print("🚀 Создаю структуру проекта English Learning Bot...\n")
    
    # requirements.txt
    create_file("requirements.txt", """# Core
aiogram==3.13.1
sqlalchemy==2.0.36
alembic==1.14.0
asyncpg==0.30.0
pydantic==2.9.2
pydantic-settings==2.6.1

# AI
aiohttp==3.10.10

# Speech
edge-tts==6.1.12
gtts==2.5.4
openai-whisper==20240930

# Utils
python-dotenv==1.0.1
aiofiles==24.1.0
""")
    
    # .env
    create_file(".env", """# Bot Token (получи у @BotFather)
BOT_TOKEN=your_telegram_bot_token_here

# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/english_bot

# AI - Groq (получи на https://console.groq.com/)
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here

# Speech
TTS_PROVIDER=edge
TTS_VOICE=en-US-JennyNeural
STT_PROVIDER=whisper
WHISPER_MODEL=base

# App
DEBUG=false
LOG_LEVEL=INFO
""")
    
    # app/__init__.py
    create_file("app/__init__.py", "# English Learning Telegram Bot\n")
    
    # app/config.py
    create_file("app/config.py", '''from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings."""
    
    bot_token: str = Field(..., description="Telegram bot token")
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/english_bot"
    )
    
    llm_provider: str = Field(default="groq")
    groq_api_key: str | None = Field(default=None)
    gemini_api_key: str | None = Field(default=None)
    
    tts_provider: str = Field(default="edge")
    stt_provider: str = Field(default="whisper")
    tts_voice: str = Field(default="en-US-JennyNeural")
    whisper_model: str = Field(default="base")
    
    debug: bool = Field(default=False)
    log_level: str = Field(default="INFO")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
''')
    
    # app/main.py
    create_file("app/main.py", '''"""Main entry point."""
import asyncio
import logging

from aiogram import Bot

from app.config import settings
from app.database.base import init_db, close_db
from app.telegram.bot import create_bot, create_dispatcher

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def on_startup(bot: Bot):
    logger.info("Initializing database...")
    await init_db()
    logger.info("Bot started successfully!")


async def on_shutdown(bot: Bot):
    logger.info("Shutting down...")
    await close_db()
    await bot.session.close()


async def main():
    logger.info("Starting English Learning Bot...")
    bot = create_bot()
    dp = create_dispatcher()
    
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
    finally:
        await on_shutdown(bot)


if __name__ == "__main__":
    asyncio.run(main())
''')
    
    # app/database/base.py
    create_file("app/database/__init__.py", "")
    create_file("app/database/base.py", '''from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

engine = create_async_engine(settings.database_url, echo=settings.debug)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_db():
    await engine.dispose()
''')
    
    # app/database/models/__init__.py
    create_file("app/database/models/__init__.py", "")
    
    # app/database/models/user.py
    create_file("app/database/models/user.py", '''from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database.base import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String(255))
    first_name = Column(String(255))
    current_level = Column(String(10), default="A0")
    total_xp = Column(Integer, default=0)
    streak_days = Column(Integer, default=0)
    last_activity_date = Column(DateTime)
    last_practice_date = Column(DateTime)
    total_words_learned = Column(Integer, default=0)
    total_reviews = Column(Integer, default=0)
    total_correct = Column(Integer, default=0)
    total_wrong = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
''')
    
    # app/database/models/word.py
    create_file("app/database/models/word.py", '''from sqlalchemy import Column, Integer, String, Float, Text, JSON, DateTime
from sqlalchemy.sql import func
from app.database.base import Base

class Word(Base):
    __tablename__ = "words"
    
    id = Column(Integer, primary_key=True)
    word = Column(String(255), nullable=False, index=True)
    translation = Column(Text, nullable=False)
    part_of_speech = Column(String(50))
    frequency_rank = Column(Integer, index=True)
    level = Column(String(10), default="A1", index=True)
    importance = Column(Float, default=5.0)
    pronunciation = Column(String(255))
    examples = Column(JSON, default=[])
    common_phrases = Column(JSON, default=[])
    collocations = Column(JSON, default=[])
    synonyms = Column(JSON, default=[])
    forms = Column(JSON, default=[])
    tags = Column(JSON, default=[])
    category = Column(String(100), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
''')
    
    # app/database/models/user_word.py
    create_file("app/database/models/user_word.py", '''from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from app.database.base import Base

class UserWord(Base):
    __tablename__ = "user_words"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"), nullable=False, index=True)
    mastery_level = Column(Float, default=0.0)
    ease_factor = Column(Float, default=2.5)
    interval_days = Column(Integer, default=0)
    repetitions = Column(Integer, default=0)
    next_review_date = Column(DateTime(timezone=True), index=True)
    last_review_date = Column(DateTime(timezone=True))
    times_shown = Column(Integer, default=0)
    times_correct = Column(Integer, default=0)
    times_wrong = Column(Integer, default=0)
    is_learned = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (UniqueConstraint('user_id', 'word_id', name='uq_user_word'),)
''')
    
    # app/database/models/review.py
    create_file("app/database/models/review.py", '''from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.sql import func
from app.database.base import Base

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"), nullable=False, index=True)
    exercise_type = Column(String(50), nullable=False)
    is_correct = Column(Integer, nullable=False)
    response_time = Column(Float)
    user_answer = Column(Text)
    correct_answer = Column(Text)
    quality = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
''')
    
    print("\n📦 Базовая структура создана!")
    print("📝 Теперь создай файлы handlers и services...")
    print("\n✅ Готово! Следуй инструкции в README.md")


if __name__ == "__main__":
    setup_project()
