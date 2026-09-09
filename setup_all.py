#!/usr/bin/env python3
"""
ENGLISH LEARNING BOT — АВТОМАТИЧЕСКАЯ УСТАНОВКА

КАК ИСПОЛЬЗОВАТЬ:
1. Скопируй ВЕСЬ этот файл
2. В PyCharm создай файл setup_all.py в корне проекта
3. Вставь код и сохрани
4. Запусти: python setup_all.py
5. Скрипт создаст все файлы автоматически!
"""

import os
from pathlib import Path


def create_file(filepath: str, content: str):
    """Создаёт файл с содержимым."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    if path.exists() and path.stat().st_size > 0:
        print(f"⏭️  Пропущен: {filepath}")
        return
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Создан: {filepath}")


def setup():
    """Создаёт все файлы проекта."""
    
    print("=" * 60)
    print("🚀 English Learning Bot — Установка")
    print("=" * 60)
    print()
    
    # requirements.txt
    create_file("requirements.txt", """aiogram==3.13.1
sqlalchemy==2.0.36
alembic==1.14.0
asyncpg==0.30.0
pydantic==2.9.2
pydantic-settings==2.6.1
aiohttp==3.10.10
edge-tts==6.1.12
gtts==2.5.4
python-dotenv==1.0.1
aiofiles==24.1.0
""")
    
    # .env
    create_file(".env", """# Telegram Bot Token (от @BotFather)
BOT_TOKEN=your_telegram_bot_token_here

# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/english_bot

# AI - Groq (бесплатно: https://console.groq.com/)
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
    
    # docker-compose.yml
    create_file("docker-compose.yml", """version: '3.8'

services:
  bot:
    build: .
    container_name: english-bot
    restart: unless-stopped
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
    networks:
      - bot-network

  db:
    image: postgres:16-alpine
    container_name: english-bot-db
    restart: unless-stopped
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: english_bot
    volumes:
      - postgres-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - bot-network

volumes:
  postgres-data:

networks:
  bot-network:
    driver: bridge
""")
    
    # app/__init__.py
    create_file("app/__init__.py", "# English Learning Telegram Bot\n")
    
    # app/config.py
    create_file("app/config.py", '''from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    bot_token: str = Field(..., description="Telegram bot token")
    database_url: str = Field(default="postgresql+asyncpg://postgres:postgres@localhost:5432/english_bot")
    llm_provider: str = Field(default="groq")
    groq_api_key: str | None = Field(default=None)
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
    create_file("app/main.py", '''import asyncio
import logging
from aiogram import Bot
from app.config import settings
from app.database.base import init_db, close_db
from app.telegram.bot import create_bot, create_dispatcher

logging.basicConfig(level=getattr(logging, settings.log_level.upper()), format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
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
    
    # app/database/
    create_file("app/database/__init__.py", "from app.database.base import Base, engine, async_session, init_db, close_db\n")
    
    create_file("app/database/base.py", '''from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

engine = create_async_engine(settings.database_url, echo=settings.debug)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_db():
    await engine.dispose()
''')
    
    create_file("app/database/models/__init__.py", "from app.database.models.user import User\nfrom app.database.models.word import Word\nfrom app.database.models.user_word import UserWord\nfrom app.database.models.review import Review\n")
    
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
    total_words_learned = Column(Integer, default=0)
    total_reviews = Column(Integer, default=0)
    total_correct = Column(Integer, default=0)
    total_wrong = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
''')
    
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
    
    # app/repositories/
    create_file("app/repositories/__init__.py", "from app.repositories.user_repo import UserRepository\nfrom app.repositories.word_repo import WordRepository\nfrom app.repositories.review_repo import ReviewRepository\n")
    
    create_file("app/repositories/user_repo.py", '''from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.user import User
from datetime import datetime

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        result = await self.session.execute(select(User).where(User.telegram_id == telegram_id))
        return result.scalar_one_or_none()
    
    async def create(self, telegram_id: int, username: str = None, first_name: str = None) -> User:
        user = User(telegram_id=telegram_id, username=username, first_name=first_name, last_activity_date=datetime.utcnow())
        self.session.add(user)
        await self.session.flush()
        return user
    
    async def get_or_create(self, telegram_id: int, username: str = None, first_name: str = None) -> User:
        user = await self.get_by_telegram_id(telegram_id)
        if not user:
            user = await self.create(telegram_id, username, first_name)
        return user
    
    async def update_activity(self, user: User):
        user.last_activity_date = datetime.utcnow()
        await self.session.flush()
    
    async def add_xp(self, user: User, xp: int):
        user.total_xp += xp
        await self.session.flush()
    
    async def update_stats(self, user: User, correct: bool):
        user.total_reviews += 1
        if correct:
            user.total_correct += 1
        else:
            user.total_wrong += 1
        await self.session.flush()
''')
    
    create_file("app/repositories/word_repo.py", '''from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.word import Word
from app.database.models.user_word import UserWord
from datetime import datetime
from typing import List

class WordRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_new_words_for_user(self, user_id: int, level: str, limit: int = 5) -> List[Word]:
        existing = await self.session.execute(select(UserWord.word_id).where(UserWord.user_id == user_id))
        existing_ids = [row[0] for row in existing.all()]
        query = select(Word).where(Word.level == level)
        if existing_ids:
            query = query.where(Word.id.notin_(existing_ids))
        query = query.order_by(Word.frequency_rank.asc()).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def get_words_due_for_review(self, user_id: int, limit: int = 20):
        now = datetime.utcnow()
        result = await self.session.execute(
            select(UserWord).where(and_(UserWord.user_id == user_id, UserWord.next_review_date <= now, UserWord.is_learned == 0))
            .order_by(UserWord.next_review_date.asc()).limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_words_for_level(self, level: str, limit: int = 3, exclude_word_ids: List[int] = None) -> List[Word]:
        query = select(Word).where(Word.level == level)
        if exclude_word_ids:
            query = query.where(Word.id.notin_(exclude_word_ids))
        query = query.order_by(func.random()).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())
''')
    
    create_file("app/repositories/review_repo.py", '''from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.review import Review
from typing import Dict

class ReviewRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_review(self, user_id: int, word_id: int, exercise_type: str, is_correct: bool, response_time: float = None, user_answer: str = None, correct_answer: str = None, quality: int = None) -> Review:
        review = Review(user_id=user_id, word_id=word_id, exercise_type=exercise_type, is_correct=1 if is_correct else 0, response_time=response_time, user_answer=user_answer, correct_answer=correct_answer, quality=quality)
        self.session.add(review)
        await self.session.flush()
        return review
    
    async def get_accuracy_by_type(self, user_id: int) -> Dict[str, float]:
        result = await self.session.execute(select(Review.exercise_type, func.count(Review.id), func.sum(Review.is_correct)).where(Review.user_id == user_id).group_by(Review.exercise_type))
        return {row[0]: (row[2] / row[1] * 100) if row[1] > 0 else 0 for row in result.all()}
''')
    
    # app/services/
    create_file("app/services/__init__.py", "from app.services.learning_service import LearningService\nfrom app.services.spaced_repetition import SpacedRepetition\n")
    
    create_file("app/services/spaced_repetition.py", '''from datetime import datetime, timedelta
from app.database.models.user_word import UserWord

class SpacedRepetition:
    MIN_INTERVAL = 1
    MAX_INTERVAL = 365
    MASTERY_THRESHOLD = 85.0
    
    @staticmethod
    def calculate_quality(is_correct: bool, response_time: float = None) -> int:
        if not is_correct:
            return 1
        if response_time is None:
            return 4
        if response_time < 2.0:
            return 5
        elif response_time < 5.0:
            return 4
        elif response_time < 10.0:
            return 3
        else:
            return 2
    
    @staticmethod
    def update_user_word(user_word: UserWord, quality: int) -> UserWord:
        user_word.times_shown += 1
        if quality >= 3:
            user_word.times_correct += 1
            user_word.repetitions += 1
        else:
            user_word.times_wrong += 1
        
        if quality >= 3:
            user_word.ease_factor = max(1.3, user_word.ease_factor + 0.1)
        else:
            user_word.ease_factor = max(1.3, user_word.ease_factor - 0.2)
        
        if quality < 3:
            user_word.interval_days = SpacedRepetition.MIN_INTERVAL
        else:
            if user_word.repetitions == 1:
                user_word.interval_days = 1
            elif user_word.repetitions == 2:
                user_word.interval_days = 6
            else:
                user_word.interval_days = round(user_word.interval_days * user_word.ease_factor)
            user_word.interval_days = min(user_word.interval_days, SpacedRepetition.MAX_INTERVAL)
        
        user_word.next_review_date = datetime.utcnow() + timedelta(days=user_word.interval_days)
        user_word.last_review_date = datetime.utcnow()
        
        score_increment = (quality / 5.0) * 20
        total_reviews = user_word.times_shown
        if total_reviews == 1:
            user_word.mastery_level = score_increment * 5
        else:
            weight = 1.0 / min(total_reviews, 10)
            user_word.mastery_level = user_word.mastery_level * (1 - weight) + score_increment * 5 * weight
        user_word.mastery_level = min(100.0, user_word.mastery_level)
        
        if user_word.mastery_level >= SpacedRepetition.MASTERY_THRESHOLD:
            user_word.is_learned = 1
        
        return user_word
''')
    
    create_file("app/services/learning_service.py", '''import random
from datetime import datetime
from typing import List, Dict, Tuple
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.user import User
from app.database.models.word import Word
from app.database.models.user_word import UserWord
from app.repositories.user_repo import UserRepository
from app.repositories.word_repo import WordRepository
from app.repositories.review_repo import ReviewRepository
from app.services.spaced_repetition import SpacedRepetition

class LearningService:
    RECOGNITION = "recognition"
    RECALL = "recall"
    LISTENING = "listening"
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)
        self.word_repo = WordRepository(session)
        self.review_repo = ReviewRepository(session)
        self.srs = SpacedRepetition()
    
    async def get_next_words(self, user: User, count: int = 5) -> List[Word]:
        return await self.word_repo.get_new_words_for_user(user_id=user.id, level=user.current_level, limit=count)
    
    async def get_words_for_review(self, user: User, count: int = 20):
        return await self.word_repo.get_words_due_for_review(user_id=user.id, limit=count)
    
    async def create_user_word(self, user_id: int, word_id: int) -> UserWord:
        user_word = UserWord(user_id=user_id, word_id=word_id, next_review_date=datetime.utcnow())
        self.session.add(user_word)
        await self.session.flush()
        return user_word
    
    async def generate_exercise(self, word: Word, user: User, exercise_type: str = None) -> Dict:
        if exercise_type is None:
            exercise_type = random.choice([self.RECOGNITION, self.RECALL, self.LISTENING])
        
        if exercise_type == self.RECOGNITION:
            return await self._generate_recognition(word)
        elif exercise_type == self.RECALL:
            return await self._generate_recall(word)
        elif exercise_type == self.LISTENING:
            return await self._generate_listening(word)
        return await self._generate_recognition(word)
    
    async def _generate_recognition(self, word: Word) -> Dict:
        distractors = await self.word_repo.get_words_for_level(word.level, limit=3, exclude_word_ids=[word.id])
        options = [word.translation] + [w.translation for w in distractors]
        random.shuffle(options)
        return {"type": self.RECOGNITION, "word": word, "question": f"What does '{word.word}' mean?", "options": options, "correct_answer": word.translation}
    
    async def _generate_recall(self, word: Word) -> Dict:
        return {"type": self.RECALL, "word": word, "question": f"How do you say '{word.translation}' in English?", "correct_answer": word.word}
    
    async def _generate_listening(self, word: Word) -> Dict:
        distractors = await self.word_repo.get_words_for_level(word.level, limit=3, exclude_word_ids=[word.id])
        options = [word.word] + [w.word for w in distractors]
        random.shuffle(options)
        return {"type": self.LISTENING, "word": word, "question": "Listen and choose", "audio_text": word.word, "options": options, "correct_answer": word.word}
    
    async def process_answer(self, user: User, word: Word, exercise_type: str, user_answer: str, correct_answer: str, response_time: float = None) -> Tuple[bool, Dict]:
        is_correct = user_answer.strip().lower() == correct_answer.strip().lower()
        quality = self.srs.calculate_quality(is_correct, response_time)
        
        result = await self.session.execute(select(UserWord).where(UserWord.user_id == user.id, UserWord.word_id == word.id))
        user_word = result.scalar_one_or_none()
        if not user_word:
            user_word = await self.create_user_word(user.id, word.id)
        
        self.srs.update_user_word(user_word, quality)
        await self.review_repo.create_review(user.id, word.id, exercise_type, is_correct, response_time, user_answer, correct_answer, quality)
        await self.user_repo.update_stats(user, is_correct)
        await self.user_repo.update_activity(user)
        
        xp = 10 if is_correct else 2
        await self.user_repo.add_xp(user, xp)
        
        if is_correct:
            feedback = {"is_correct": True, "message": "✅ Correct!"}
        else:
            feedback = {"is_correct": False, "message": f"❌ Correct: {correct_answer}"}
        
        return is_correct, feedback
''')
    
    # app/ai/
    create_file("app/ai/__init__.py", "from app.ai.providers import GroqProvider, get_llm_provider\n")
    
    create_file("app/ai/providers.py", '''import os
import aiohttp
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    async def chat(self, messages: list[dict], temperature: float = 0.7, max_tokens: int = 500) -> str:
        pass
    
    async def converse(self, messages: list[dict], user_level: str = "A2") -> str:
        system_prompt = f"You are a friendly English conversation partner. Student level: {user_level}. Keep responses short (1-3 sentences). Ask follow-up questions. If they make a mistake, gently correct."
        full_messages = [{"role": "system", "content": system_prompt}] + messages
        return await self.chat(full_messages, temperature=0.8, max_tokens=150)

class GroqProvider(LLMProvider):
    """Groq — БЕСПЛАТНЫЙ AI (Llama 3.3). Получи ключ: https://console.groq.com/"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = "llama-3.3-70b-versatile"
        self.base_url = "https://api.groq.com/openai/v1"
    
    async def chat(self, messages: list[dict], temperature: float = 0.7, max_tokens: int = 500) -> str:
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"model": self.model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}/chat/completions", headers=headers, json=payload) as response:
                data = await response.json()
                return data["choices"][0]["message"]["content"]

def get_llm_provider() -> LLMProvider:
    return GroqProvider()
''')
    
    # app/speech/
    create_file("app/speech/__init__.py", "from app.speech.providers import EdgeTTSProvider, get_tts_provider\n")
    
    create_file("app/speech/providers.py", '''import os
from abc import ABC, abstractmethod

class TTSProvider(ABC):
    @abstractmethod
    async def synthesize(self, text: str, lang: str = "en") -> bytes:
        pass

class EdgeTTSProvider(TTSProvider):
    """Microsoft Edge TTS — БЕСПЛАТНЫЙ, качественный."""
    
    def __init__(self, voice: str = "en-US-JennyNeural"):
        self.voice = voice
    
    async def synthesize(self, text: str, lang: str = "en") -> bytes:
        import edge_tts
        communicate = edge_tts.Communicate(text=text, voice=self.voice)
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        return audio_data

def get_tts_provider() -> TTSProvider:
    return EdgeTTSProvider()
''')
    
    # app/telegram/
    create_file("app/telegram/__init__.py", "from app.telegram.bot import create_bot, create_dispatcher\n")
    
    create_file("app/telegram/bot.py", '''from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from app.config import settings
from app.telegram.handlers import start, learn, review, dialogue, progress

def create_bot() -> Bot:
    return Bot(token=settings.bot_token)

def create_dispatcher() -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(start.router)
    dp.include_router(learn.router)
    dp.include_router(review.router)
    dp.include_router(dialogue.router)
    dp.include_router(progress.router)
    return dp
''')
    
    create_file("app/telegram/handlers/__init__.py", "from app.telegram.handlers import start, learn, review, dialogue, progress\n")
    create_file("app/telegram/keyboards/__init__.py", "")
    
    create_file("app/telegram/keyboards/main.py", '''from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📚 Учить новые слова", callback_data="learn_new")],
        [InlineKeyboardButton(text="🔁 Повторить", callback_data="review")],
        [InlineKeyboardButton(text="💬 Поговорить", callback_data="dialogue")],
        [InlineKeyboardButton(text="📊 Мой прогресс", callback_data="progress")],
    ])

def get_answer_keyboard(options: list, prefix: str = "ans") -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(text=opt, callback_data=f"{prefix}_{i}")] for i, opt in enumerate(options)]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_continue_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Далее", callback_data="next_exercise")],
        [InlineKeyboardButton(text="🏠 В меню", callback_data="menu")],
    ])
''')
    
    create_file("app/telegram/handlers/start.py", '''from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from app.database.base import async_session
from app.repositories.user_repo import UserRepository
from app.telegram.keyboards.main import get_main_menu_keyboard

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    async with async_session() as session:
        user_repo = UserRepository(session)
        user = await user_repo.get_or_create(telegram_id=message.from_user.id, username=message.from_user.username, first_name=message.from_user.first_name)
        await session.commit()
    
    text = f"🇬🇧 <b>Привет, {message.from_user.first_name}!</b>\\n\\nЯ — твой репетитор английского.\\n\\n<b>Уровень:</b> {user.current_level}\\n<b>XP:</b> {user.total_xp}\\n\\nВыбери действие:"
    await message.answer(text, reply_markup=get_main_menu_keyboard(), parse_mode="HTML")

@router.callback_query(F.data == "menu")
async def callback_menu(callback: CallbackQuery):
    async with async_session() as session:
        user_repo = UserRepository(session)
        user = await user_repo.get_or_create(telegram_id=callback.from_user.id)
        await session.commit()
    
    text = f"<b>🏠 Меню</b>\\n\\nУровень: {user.current_level} | XP: {user.total_xp}"
    await callback.message.edit_text(text, reply_markup=get_main_menu_keyboard(), parse_mode="HTML")
    await callback.answer()
''')
    
    create_file("app/telegram/handlers/learn.py", '''from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.database.base import async_session
from app.repositories.user_repo import UserRepository
from app.services.learning_service import LearningService
from app.telegram.keyboards.main import get_answer_keyboard, get_continue_keyboard

router = Router()

class LearnStates(StatesGroup):
    answering = State()

_exercise_cache = {}

@router.callback_query(F.data == "learn_new")
async def start_learning(callback: CallbackQuery, state: FSMContext):
    async with async_session() as session:
        user_repo = UserRepository(session)
        learning_service = LearningService(session)
        user = await user_repo.get_or_create(telegram_id=callback.from_user.id)
        
        words = await learning_service.get_next_words(user, count=1)
        if not words:
            await callback.message.edit_text("🎉 Все слова изучены!")
            await callback.answer()
            return
        
        word = words[0]
        await learning_service.create_user_word(user.id, word.id)
        await session.commit()
        
        exercise = await learning_service.generate_exercise(word, user)
        _exercise_cache[callback.from_user.id] = exercise
        
        text = f"📚 <b>Новое слово!</b>\\n\\n🇬🇧 <b>{word.word}</b>\\n🇷🇺 {word.translation}\\n\\n<b>{exercise['question']}</b>"
        keyboard = get_answer_keyboard(exercise['options']) if exercise.get('options') else get_continue_keyboard()
        
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
        await state.set_state(LearnStates.answering)
        await callback.answer()

@router.callback_query(LearnStates.answering, F.data.startswith("ans_"))
async def process_answer(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    exercise = _exercise_cache.get(user_id)
    if not exercise:
        await callback.answer("Exercise not found", show_alert=True)
        return
    
    option_index = int(callback.data.split("_")[1])
    user_answer = exercise['options'][option_index]
    correct_answer = exercise['correct_answer']
    word = exercise['word']
    
    async with async_session() as session:
        learning_service = LearningService(session)
        user_repo = UserRepository(session)
        user = await user_repo.get_or_create(telegram_id=user_id)
        is_correct, feedback = await learning_service.process_answer(user, word, exercise['type'], user_answer, correct_answer)
        await session.commit()
    
    if is_correct:
        text = f"✅ <b>Правильно!</b> 🎉\\n\\n🇬🇧 <b>{word.word}</b> — {word.translation}\\n\\n+10 XP"
    else:
        text = f"❌ <b>Неправильно</b>\\n\\nОтвет: <b>{correct_answer}</b>\\n\\n🇬🇧 <b>{word.word}</b> — {word.translation}"
    
    await callback.message.edit_text(text, reply_markup=get_continue_keyboard(), parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data == "next_exercise")
async def next_exercise(callback: CallbackQuery, state: FSMContext):
    _exercise_cache.pop(callback.from_user.id, None)
    await start_learning(callback, state)
''')
    
    create_file("app/telegram/handlers/review.py", '''from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import select
from app.database.base import async_session
from app.database.models.word import Word
from app.repositories.user_repo import UserRepository
from app.services.learning_service import LearningService
from app.telegram.keyboards.main import get_answer_keyboard, get_continue_keyboard

router = Router()

class ReviewStates(StatesGroup):
    answering = State()

_review_cache = {}

@router.callback_query(F.data == "review")
async def start_review(callback: CallbackQuery, state: FSMContext):
    async with async_session() as session:
        user_repo = UserRepository(session)
        learning_service = LearningService(session)
        user = await user_repo.get_or_create(telegram_id=callback.from_user.id)
        
        user_words = await learning_service.get_words_for_review(user, count=1)
        if not user_words:
            await callback.message.edit_text("🎉 Нет слов на повторении!")
            await callback.answer()
            return
        
        user_word = user_words[0]
        result = await session.execute(select(Word).where(Word.id == user_word.word_id))
        word = result.scalar_one_or_none()
        
        if not word:
            await callback.message.edit_text("❌ Слово не найдено")
            await callback.answer()
            return
        
        exercise = await learning_service.generate_exercise(word, user)
        _review_cache[callback.from_user.id] = exercise
        
        text = f"🔁 <b>Повторение</b>\\n\\n{exercise['question']}"
        keyboard = get_answer_keyboard(exercise['options']) if exercise.get('options') else get_continue_keyboard()
        
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
        await state.set_state(ReviewStates.answering)
        await callback.answer()

@router.callback_query(ReviewStates.answering, F.data.startswith("ans_"))
async def process_review_answer(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    exercise = _review_cache.get(user_id)
    if not exercise:
        await callback.answer("Exercise not found", show_alert=True)
        return
    
    option_index = int(callback.data.split("_")[1])
    user_answer = exercise['options'][option_index]
    correct_answer = exercise['correct_answer']
    word = exercise['word']
    
    async with async_session() as session:
        learning_service = LearningService(session)
        user_repo = UserRepository(session)
        user = await user_repo.get_or_create(telegram_id=user_id)
        is_correct, feedback = await learning_service.process_answer(user, word, exercise['type'], user_answer, correct_answer)
        await session.commit()
    
    if is_correct:
        text = f"✅ <b>Правильно!</b>\\n\\n🇬🇧 {word.word} — {word.translation}\\n\\n+10 XP"
    else:
        text = f"❌ <b>Неправильно</b>\\n\\nОтвет: <b>{correct_answer}</b>\\n\\n🇬🇧 {word.word} — {word.translation}"
    
    await callback.message.edit_text(text, reply_markup=get_continue_keyboard(), parse_mode="HTML")
    await callback.answer()
''')
    
    create_file("app/telegram/handlers/dialogue.py", '''from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.database.base import async_session
from app.repositories.user_repo import UserRepository
from app.ai.providers import get_llm_provider
from app.telegram.keyboards.main import get_main_menu_keyboard

router = Router()

class DialogueStates(StatesGroup):
    chatting = State()

_conversation_history = {}

@router.callback_query(F.data == "dialogue")
async def start_dialogue(callback: CallbackQuery, state: FSMContext):
    async with async_session() as session:
        user_repo = UserRepository(session)
        user = await user_repo.get_or_create(telegram_id=callback.from_user.id)
    
    _conversation_history[callback.from_user.id] = []
    
    try:
        llm = get_llm_provider()
        messages = [{"role": "user", "content": "Hi! Let's practice English."}]
        response = await llm.converse(messages=messages, user_level=user.current_level)
        _conversation_history[callback.from_user.id].append({"role": "assistant", "content": response})
        text = f"💬 <b>AI Conversation</b>\\n\\n{response}\\n\\n<i>Напиши ответ на английском</i>"
    except Exception:
        text = "💬 <b>AI Conversation</b>\\n\\nHi! How are you?\\n\\n<i>(Добавь GROQ_API_KEY в .env)</i>"
    
    await callback.message.edit_text(text, reply_markup=get_main_menu_keyboard(), parse_mode="HTML")
    await state.set_state(DialogueStates.chatting)
    await callback.answer()

@router.message(DialogueStates.chatting)
async def handle_dialogue_message(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_text = message.text
    
    async with async_session() as session:
        user_repo = UserRepository(session)
        user = await user_repo.get_or_create(telegram_id=user_id)
    
    if user_id not in _conversation_history:
        _conversation_history[user_id] = []
    
    _conversation_history[user_id].append({"role": "user", "content": user_text})
    
    try:
        llm = get_llm_provider()
        response = await llm.converse(messages=_conversation_history[user_id], user_level=user.current_level)
        _conversation_history[user_id].append({"role": "assistant", "content": response})
        if len(_conversation_history[user_id]) > 10:
            _conversation_history[user_id] = _conversation_history[user_id][-10:]
        await message.answer(response, parse_mode="HTML")
    except Exception:
        await message.answer("Interesting! Tell me more.\\n\\n<i>(Добавь GROQ_API_KEY в .env)</i>", parse_mode="HTML")
''')
    
    create_file("app/telegram/handlers/progress.py", '''from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy import select, func
from app.database.base import async_session
from app.database.models.user_word import UserWord
from app.repositories.user_repo import UserRepository
from app.repositories.review_repo import ReviewRepository
from app.telegram.keyboards.main import get_main_menu_keyboard

router = Router()

@router.callback_query(F.data == "progress")
async def show_progress(callback: CallbackQuery):
    async with async_session() as session:
        user_repo = UserRepository(session)
        review_repo = ReviewRepository(session)
        user = await user_repo.get_or_create(telegram_id=callback.from_user.id)
        
        accuracy = await review_repo.get_accuracy_by_type(user.id)
        
        result = await session.execute(select(func.count(UserWord.id)).where(UserWord.user_id == user.id, UserWord.is_learned == 1))
        learned_count = result.scalar() or 0
    
    total_accuracy = sum(accuracy.values()) / len(accuracy) if accuracy else 0
    
    text = f"""📊 <b>Твоя статистика</b>

<b>🎯 Уровень:</b> {user.current_level}
<b>⭐ XP:</b> {user.total_xp}
<b>🔥 Серия:</b> {user.streak_days} дней

<b>📚 Слов изучено:</b> {learned_count}

<b>📈 Навыки:</b>
• Recognition: {accuracy.get('recognition', 0):.0f}%
• Recall: {accuracy.get('recall', 0):.0f}%
• Listening: {accuracy.get('listening', 0):.0f}%

<b>📊 Точность:</b> {total_accuracy:.0f}%
<b>📝 Ответов:</b> {user.total_correct}✅ / {user.total_wrong}❌"""
    
    await callback.message.edit_text(text, reply_markup=get_main_menu_keyboard(), parse_mode="HTML")
    await callback.answer()
''')
    
    # app/utils/
    create_file("app/utils/__init__.py", "# Utils\n")
    
    # scripts/
    create_file("scripts/__init__.py", "")
    
    create_file("scripts/import_words.py", '''import json
import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from sqlalchemy import select
from app.database.base import async_session, init_db
from app.database.models.word import Word

async def import_from_json(filepath: str):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    words_data = data.get('words', data) if isinstance(data, dict) else data
    stats = {'total': len(words_data), 'imported': 0, 'skipped': 0}
    
    async with async_session() as session:
        for word_data in words_data:
            try:
                existing = await session.execute(select(Word).where(Word.word == word_data['word'].lower()))
                if existing.scalar_one_or_none():
                    stats['skipped'] += 1
                    continue
                
                word = Word(word=word_data['word'].lower(), translation=word_data['translation'], part_of_speech=word_data.get('part_of_speech'), frequency_rank=word_data.get('frequency_rank', 5000), level=word_data.get('level', 'A1'), importance=word_data.get('importance', 5.0), pronunciation=word_data.get('pronunciation'), examples=word_data.get('examples', []), common_phrases=word_data.get('common_phrases', []), collocations=word_data.get('collocations', []), synonyms=word_data.get('synonyms', []), forms=word_data.get('forms', []), tags=word_data.get('tags', []), category=word_data.get('category'))
                session.add(word)
                stats['imported'] += 1
            except Exception as e:
                print(f"Error: {e}")
        
        await session.commit()
    
    print(f"✅ Done! Imported: {stats['imported']}, Skipped: {stats['skipped']}")

async def main():
    if len(sys.argv) < 2:
        print("Usage: python -m scripts.import_words <filepath.json>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    if not Path(filepath).exists():
        print(f"File not found: {filepath}")
        sys.exit(1)
    
    print(f"📚 Importing from: {filepath}")
    await init_db()
    await import_from_json(filepath)

if __name__ == "__main__":
    asyncio.run(main())
''')
    
    # data/
    create_file("data/words_sample.json", json.dumps({
        "words": [
            {"word": "hello", "translation": "привет", "part_of_speech": "interjection", "frequency_rank": 10, "level": "A0", "pronunciation": "/həˈloʊ/", "examples": [{"en": "Hello!", "ru": "Привет!"}], "common_phrases": [], "collocations": [], "synonyms": ["hi"], "forms": [], "tags": ["greetings"], "category": "greetings", "importance": 10.0},
            {"word": "go", "translation": "идти", "part_of_speech": "verb", "frequency_rank": 5, "level": "A1", "pronunciation": "/ɡoʊ/", "examples": [{"en": "I go to work.", "ru": "Я иду на работу."}], "common_phrases": ["go ahead"], "collocations": ["go home"], "synonyms": ["leave"], "forms": ["go", "went", "gone"], "tags": ["basic"], "category": "movement", "importance": 10.0},
            {"word": "water", "translation": "вода", "part_of_speech": "noun", "frequency_rank": 50, "level": "A1", "pronunciation": "/ˈwɔːtər/", "examples": [{"en": "Can I have water?", "ru": "Можно воды?"}], "common_phrases": [], "collocations": [], "synonyms": [], "forms": [], "tags": ["basic"], "category": "food", "importance": 9.0}
        ]
    }, ensure_ascii=False, indent=2))
    
    # ИТОГ
    print()
    print("=" * 60)
    print("✅ ВСЕ ФАЙЛЫ СОЗДАНЫ!")
    print("=" * 60)
    print()
    print("📋 Следующие шаги:")
    print()
    print("1. Установи зависимости:")
    print("   pip install -r requirements.txt")
    print()
    print("2. Отредактируй .env:")
    print("   - Добавь BOT_TOKEN (от @BotFather)")
    print("   - Добавь GROQ_API_KEY (с https://console.groq.com/)")
    print()
    print("3. Запусти PostgreSQL:")
    print("   docker-compose up -d db")
    print()
    print("4. Импортируй словарь:")
    print("   python -m scripts.import_words data/words_sample.json")
    print()
    print("5. Запусти бота:")
    print("   python -m app.main")
    print()
    print("🎉 Готово!")


if __name__ == "__main__":
    setup()
