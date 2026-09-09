"""Learn handler - teaches new words."""

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.database.base import async_session
from app.repositories.user_repo import UserRepository
from app.repositories.word_repo import WordRepository
from app.services.learning_service import LearningService
from app.telegram.keyboards.main import (
    get_answer_keyboard,
    get_exercise_navigation_keyboard,
    get_continue_keyboard,
)

router = Router()


class LearnStates(StatesGroup):
    """States for learning process."""
    learning = State()
    answering = State()


# Store current exercise data per user
_exercise_cache = {}


@router.callback_query(F.data == "learn_new")
async def start_learning(callback: CallbackQuery, state: FSMContext):
    """Start learning new words."""
    async with async_session() as session:
        user_repo = UserRepository(session)
        word_repo = WordRepository(session)
        learning_service = LearningService(session)
        
        user = await user_repo.get_or_create(telegram_id=callback.from_user.id)
        
        # Get new words
        words = await learning_service.get_next_words(user, count=1)
        
        if not words:
            await callback.message.edit_text(
                "🎉 <b>Отлично!</b>\n\nТы выучил все слова для текущего уровня.\n"
                "Переходи к следующему уровню в настройках.",
                parse_mode="HTML",
            )
            await callback.answer()
            return
        
        word = words[0]
        
        # Create user_word entry
        await learning_service.create_user_word(user.id, word.id)
        await session.commit()
        
        # Generate exercise
        exercise = await learning_service.generate_exercise(word, user)
        
        # Cache exercise
        _exercise_cache[callback.from_user.id] = exercise
        
        # Show word introduction first
        word_intro = f"""
📚 <b>Новое слово!</b>

🇬🇧 <b>{word.word}</b> {word.pronunciation or ''}
🇷🇺 {word.translation}

📝 <i>{word.part_of_speech or 'word'}</i> | Уровень: {word.level}
"""
        
        if word.examples:
            example = word.examples[0]
            word_intro += f"\n💬 <i>Пример:</i>\n{example.get('en', '')}\n<i>{example.get('ru', '')}</i>"
        
        # Show exercise
        word_intro += f"\n\n<b>{exercise['question']}</b>"
        
        keyboard = get_answer_keyboard(exercise['options']) if exercise.get('options') else get_exercise_navigation_keyboard()
        
        await callback.message.edit_text(
            word_intro,
            reply_markup=keyboard,
            parse_mode="HTML",
        )
        
        await state.set_state(LearnStates.answering)
        await callback.answer()


@router.callback_query(LearnStates.answering, F.data.startswith("ans_"))
async def process_answer(callback: CallbackQuery, state: FSMContext):
    """Process user's answer."""
    user_id = callback.from_user.id
    exercise = _exercise_cache.get(user_id)
    
    if not exercise:
        await callback.answer("Exercise not found", show_alert=True)
        return
    
    # Get selected option
    option_index = int(callback.data.split("_")[1])
    user_answer = exercise['options'][option_index]
    correct_answer = exercise['correct_answer']
    is_correct = user_answer == correct_answer
    
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
        
        # Update words learned count
        if user.total_words_learned < await _count_learned_words(session, user.id):
            user.total_words_learned = await _count_learned_words(session, user.id)
        
        await session.commit()
    
    # Show feedback
    if is_correct:
        result_text = f"""
✅ <b>Правильно!</b> 🎉

🇬🇧 <b>{word.word}</b> — {word.translation}

+10 XP
"""
    else:
        result_text = f"""
❌ <b>Неправильно</b>

Правильный ответ: <b>{correct_answer}</b>

🇬🇧 <b>{word.word}</b> — {word.translation}

💪 Запомни и попробуй ещё раз!
"""
    
    await callback.message.edit_text(
        result_text,
        reply_markup=get_continue_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "next_exercise")
async def next_exercise(callback: CallbackQuery, state: FSMContext):
    """Continue to next exercise."""
    # Clear cache
    _exercise_cache.pop(callback.from_user.id, None)
    
    # Restart learning
    await start_learning(callback, state)


@router.callback_query(F.data == "skip")
async def skip_exercise(callback: CallbackQuery, state: FSMContext):
    """Skip current exercise."""
    _exercise_cache.pop(callback.from_user.id, None)
    await start_learning(callback, state)


async def _count_learned_words(session, user_id: int) -> int:
    """Count words with mastery >= 85."""
    from sqlalchemy import select, func
    from app.database.models.user_word import UserWord
    
    result = await session.execute(
        select(func.count(UserWord.id)).where(
            UserWord.user_id == user_id,
            UserWord.is_learned == 1,
        )
    )
    return result.scalar() or 0
