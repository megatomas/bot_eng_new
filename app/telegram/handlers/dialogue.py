"""Dialogue handler — AI conversation partner."""

from aiogram import Router, F
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


# Store conversation history per user
_conversation_history = {}


@router.callback_query(F.data == "dialogue")
async def start_dialogue(callback: CallbackQuery, state: FSMContext):
    """Start AI conversation."""
    async with async_session() as session:
        user_repo = UserRepository(session)
        user = await user_repo.get_or_create(telegram_id=callback.from_user.id)
    
    # Initialize conversation
    _conversation_history[callback.from_user.id] = []
    
    # AI greeting
    try:
        llm = get_llm_provider()
        
        messages = [
            {
                "role": "user",
                "content": "Hi! Let's practice English. Start with a simple question.",
            }
        ]
        
        response = await llm.converse(
            messages=messages,
            user_level=user.current_level,
        )
        
        _conversation_history[callback.from_user.id].append({
            "role": "assistant",
            "content": response,
        })
        
        text = f"💬 <b>AI Conversation</b>\n\n{response}\n\n<i>Напиши ответ на английском</i>"
        
    except Exception as e:
        text = (
            "💬 <b>AI Conversation</b>\n\n"
            "Hi! How are you today?\n\n"
            "<i>Напиши ответ на английском</i>\n\n"
            "<i>(AI не настроен, используется базовый режим)</i>"
        )
    
    await callback.message.edit_text(
        text,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML",
    )
    
    await state.set_state(DialogueStates.chatting)
    await callback.answer()


@router.message(DialogueStates.chatting)
async def handle_dialogue_message(message: Message, state: FSMContext):
    """Handle user's message in dialogue."""
    user_id = message.from_user.id
    user_text = message.text
    
    if user_text == "🏠 В меню":
        await state.clear()
        _conversation_history.pop(user_id, None)
        return
    
    # Get user
    async with async_session() as session:
        user_repo = UserRepository(session)
        user = await user_repo.get_or_create(telegram_id=user_id)
    
    # Add user message to history
    if user_id not in _conversation_history:
        _conversation_history[user_id] = []
    
    _conversation_history[user_id].append({
        "role": "user",
        "content": user_text,
    })
    
    # Get AI response
    try:
        llm = get_llm_provider()
        
        response = await llm.converse(
            messages=_conversation_history[user_id],
            user_level=user.current_level,
        )
        
        _conversation_history[user_id].append({
            "role": "assistant",
            "content": response,
        })
        
        # Limit history to last 10 messages
        if len(_conversation_history[user_id]) > 10:
            _conversation_history[user_id] = _conversation_history[user_id][-10:]
        
        await message.answer(response, parse_mode="HTML")
        
    except Exception as e:
        # Fallback response
        await message.answer(
            "Interesting! Can you tell me more?\n\n"
            "<i>(AI не настроен. Добавь GROQ_API_KEY в .env для полноценного диалога)</i>",
            parse_mode="HTML",
        )
