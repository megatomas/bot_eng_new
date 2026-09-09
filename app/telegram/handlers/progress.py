"""Progress handler — статистика пользователя."""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy import select, func

from app.database.base import async_session
from app.repositories.user_repo import UserRepository
from app.repositories.review_repo import ReviewRepository
from app.database.models.user_word import UserWord

router = Router()


@router.callback_query(F.data == "progress")
async def show_progress(callback: CallbackQuery):
    """Show user's progress statistics."""
    async with async_session() as session:
        user_repo = UserRepository(session)
        review_repo = ReviewRepository(session)
        
        user = await user_repo.get_or_create(telegram_id=callback.from_user.id)
        
        # Get stats
        accuracy = await review_repo.get_accuracy_by_type(user.id)
        mistake_profile = await review_repo.get_mistake_profile(user.id)
        
        # Count learned words
        result = await session.execute(
            select(func.count(UserWord.id)).where(
                UserWord.user_id == user.id,
                UserWord.is_learned == 1,
            )
        )
        learned_count = result.scalar() or 0
        
        # Count total words in rotation
        result = await session.execute(
            select(func.count(UserWord.id)).where(
                UserWord.user_id == user.id,
            )
        )
        total_in_rotation = result.scalar() or 0
    
    # Calculate overall accuracy
    total_accuracy = 0
    if accuracy:
        total_accuracy = sum(accuracy.values()) / len(accuracy)
    
    # Build progress text
    text = f"""
📊 <b>Твоя статистика</b>

<b>🎯 Уровень:</b> {user.current_level}
<b>⭐ XP:</b> {user.total_xp}
<b>🔥 Серия:</b> {user.streak_days} дней

<b>📚 Словарь:</b>
• Изучено: {learned_count}
• В процессе: {total_in_rotation - learned_count}

<b>📈 Навыки:</b>
• Recognition: {accuracy.get('recognition', 0):.0f}%
• Recall: {accuracy.get('recall', 0):.0f}%
• Listening: {accuracy.get('listening', 0):.0f}%
• Production: {accuracy.get('production', 0):.0f}%

<b>📊 Общая точность:</b> {total_accuracy:.0f}%

<b>📝 Ответов:</b>
• Правильных: {user.total_correct}
• Ошибок: {user.total_wrong}
"""
    
    if mistake_profile:
        text += "\n<b>⚠️ Слабые места:</b>\n"
        for error_type, count in list(mistake_profile.items())[:3]:
            text += f"• {error_type}: {count} ошибок\n"
    
    from app.telegram.keyboards.main import get_main_menu_keyboard
    
    await callback.message.edit_text(
        text,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()
