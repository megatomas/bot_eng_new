"""Telegram bot setup and configuration."""

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.config import settings
from app.telegram.handlers import start, learn


def create_bot() -> Bot:
    """Create and configure the bot."""
    return Bot(token=settings.bot_token)


def create_dispatcher() -> Dispatcher:
    """Create and configure the dispatcher."""
    dp = Dispatcher(storage=MemoryStorage())
    
    # Register routers
    dp.include_router(start.router)
    dp.include_router(learn.router)
    
    return dp
