"""Start command handler."""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from app.database.base import async_session
from app.repositories.user_repo import UserRepository
from app.telegram.keyboards.main import get_main_menu_keyboard

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Handle /start command."""
    async with async_session() as session:
        user_repo = UserRepository(session)
        
        # Get or create user
        user = await user_repo.get_or_create(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
        )
        await session.commit()
    
    welcome_text = f"""
🇬🇧 <b>Привет, {message.from_user.first_name}!</b>

Я — твой персональный репетитор английского языка.

🎯 Моя цель — помочь тебе <b>заговорить</b> на английском, а не просто учить слова.

<b>Что я умею:</b>
📚 Учить слова в контексте
🔁 Повторять по интервальному методу
🎧 Тренировать аудирование
🎤 Улучшать произношение
💬 Вести диалог на английском

<b>Твой уровень:</b> {user.current_level}
<b>Слов изучено:</b> {user.total_words_learned}
<b>Серия:</b> {user.streak_days} 🔥

Выбери, что хочешь делать:
"""
    
    await message.answer(
        welcome_text,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML",
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Handle /help command."""
    help_text = """
<b>📖 Команды бота:</b>

/start — Начальное меню
/learn — Учить новые слова
/review — Повторить изученное
/practice — Быстрая тренировка
/dialogue — Поговорить на английском
/progress — Твоя статистика
/settings — Настройки
/help — Эта справка

<b>💡 Совет:</b> Занимайся каждый день хотя бы 10 минут!
"""
    await message.answer(help_text, parse_mode="HTML")


@router.callback_query(F.data == "menu")
async def callback_menu(callback: CallbackQuery):
    """Handle menu callback."""
    async with async_session() as session:
        user_repo = UserRepository(session)
        user = await user_repo.get_or_create(
            telegram_id=callback.from_user.id,
        )
        await session.commit()
    
    text = f"""
<b>🏠 Главное меню</b>

Уровень: {user.current_level} | XP: {user.total_xp} | 🔥 {user.streak_days}
"""
    
    await callback.message.edit_text(
        text,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()
