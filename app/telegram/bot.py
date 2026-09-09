"""Telegram bot setup and configuration."""

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.config import settings
from app.telegram.handlers import start, learn, review, dialogue, progress


def create_bot() -> Bot:
    """Create and configure the bot."""
    return Bot(token=settings.bot_token)


def create_dispatcher() -> Dispatcher:
    """Create and configure the dispatcher."""
    dp = Dispatcher(storage=MemoryStorage())
    
    # Register all routers (handlers)
    dp.include_router(start.router)      # /start, /help, menu
    dp.include_router(learn.router)      # Учить новые слова
    dp.include_router(review.router)     # Повторение (интервальное)
    dp.include_router(dialogue.router)   # AI-собеседник
    dp.include_router(progress.router)   # Статистика
    
    return dp
