"""
English Learning Telegram Bot - Main Entry Point

A fully autonomous Telegram bot for learning conversational English.
Uses spaced repetition, AI conversation, and speech recognition.
"""

import asyncio
import logging

from aiogram import Bot

from app.config import settings
from app.database.base import init_db, close_db
from app.telegram.bot import create_bot, create_dispatcher

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def on_startup(bot: Bot):
    """Actions on bot startup."""
    logger.info("Initializing database...")
    await init_db()
    
    logger.info("Bot started successfully!")
    logger.info(f"Bot username: @{(await bot.get_me()).username}")


async def on_shutdown(bot: Bot):
    """Actions on bot shutdown."""
    logger.info("Shutting down...")
    await close_db()
    await bot.session.close()
    logger.info("Bot stopped.")


async def main():
    """Main entry point."""
    logger.info("Starting English Learning Bot v1.0...")
    
    bot = create_bot()
    dp = create_dispatcher()
    
    # Register startup/shutdown hooks
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    # Start polling
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
    finally:
        await on_shutdown(bot)


if __name__ == "__main__":
    asyncio.run(main())
