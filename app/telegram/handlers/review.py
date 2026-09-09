"""Review handler — интервальное повторение изученных слов."""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.database.base import async_session
from app.repositories.user_repo import UserRepository
from app.services.learning_service import LearningService
from app.telegram.keyboards.main import (
    get_answer_keyboard,
    get_continue_keyboard,
    get_exercise_navigation_keyboard,
)

router = Router()


class ReviewStates(StatesGroup):
    reviewing = State()
    answering = State()


_review_cache = {}


@router.callback_query(F.data == "review")
async def start_review(callback: CallbackQuery, state: FSMContext):
    """Start reviewing words due for repetition."""
    async with async_session() as session:
        user_repo = UserRepository(session)
        learning_service = LearningService(session)
        
        user = await user_repo.get_or_create(telegram_id=callback.from_user.id)
        
        # Get words due for review
        user_words = await learning_service.get_words_for_review(user, count=1)
        
        if not user_words:
            await callback.message.edit_text(
                "🎉 <b>Отлично!</b>\n\nНет слов на повторении.\n"
                "Учи новые слова или зайди позже!",
                parse_mode="HTML",
            )
            await callback.answer()
            return
        
        user_word = user_words[0]
        
        # Get the actual word
        from sqlalchemy import select
        from app.database.models.word import Word
        
        result = await session.execute(
            select(Word).where(Word.id == user_word.word_id)
        )
        word = result.scalar_one_or_none()
        
        if not word:
            await callback.message.edit_text("❌ Слово не найдено")
            await callback.answer()
            return
        
        # Generate exercise
        exercise = await learning_service.generate_exercise(word, user)
        
        # Cache
        _review_cache[callback.from_user.id] = {
            "exercise": exercise,
            "user_word_id": user_word.id,
        }
        
        # Show exercise
        text = f"🔁 <b>Повторение</b>\n\n{exercise['question']}"
        
        keyboard = (
            get_answer_keyboard(exercise['options']) 
            if exercise.get('options') 
            else get_exercise_navigation_keyboard()
        )
        
        await callback.message.edit_text(
            text,
            reply_markup=keyboard,
            parse_mode="HTML",
        )
        
        await state.set_state(ReviewStates.answering)
        await callback.answer()


@router.callback_query(ReviewStates.answering, F.data.startswith("ans_"))
async def process_review_answer(callback: CallbackQuery, state: FSMContext):
    """Process review answer."""
    user_id = callback.from_user.id
    cached = _review_cache.get(user_id)
    
    if not cached:
        await callback.answer("Exercise not found", show_alert=True)
        return
    
    exercise = cached["exercise"]
    option_index = int(callback.data.split("_")[1])
    user_answer = exercise['options'][option_index]
    correct_answer = exercise['correct_answer']
    
    word = exercise['word']
    
    async with async_session() as session:
        learning_service = LearningService(session)
        user_repo = UserRepository(session)
        
        user = await user_repo.get_or_create(telegram_id=user_id)
        
        # Process answer
        is_correct, feedback = await learning_service.process_answer(
            user=user,
            word=word,
            exercise_type=exercise['type'],
            user_answer=user_answer,
            correct_answer=correct_answer,
        )
        
        await session.commit()
    
    # Show result
    if is_correct:
        text = f"✅ <b>Правильно!</b>\n\n🇬🇧 {word.word} — {word.translation}\n\n+10 XP"
    else:
        text = f"❌ <b>Неправильно</b>\n\nПравильный ответ: <b>{correct_answer}</b>\n\n🇬🇧 {word.word} — {word.translation}"
    
    await callback.message.edit_text(
        text,
        reply_markup=get_continue_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "next_exercise")
async def next_review(callback: CallbackQuery, state: FSMContext):
    """Continue to next review."""
    _review_cache.pop(callback.from_user.id, None)
    await start_review(callback, state)
