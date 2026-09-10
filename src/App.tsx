import { useState } from 'react'

interface FileData {
  path: string
  content: string
  description: string
}

const files: FileData[] = [
  {
    path: 'app/config.py',
    description: 'Конфигурация с загрузкой .env',
    content: `from dotenv import load_dotenv
load_dotenv()

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    bot_token: str = Field(..., description="Telegram bot token")
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/english_bot"
    )
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
`
  },
  {
    path: 'app/telegram/handlers/dialogue.py',
    description: 'AI-собеседник с обработкой ошибок',
    content: `from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramBadRequest

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
        messages = [{"role": "user", "content": "Hi! Let's practice English. Start with a simple question."}]
        response = await llm.converse(messages=messages, user_level=user.current_level)
        _conversation_history[callback.from_user.id].append({"role": "assistant", "content": response})
        text = f"💬 <b>AI Conversation</b>\\n\\n{response}\\n\\n<i>Напиши ответ на английском</i>"
    except Exception:
        text = f"💬 <b>AI Conversation</b>\\n\\nHi! How are you today?\\n\\n<i>Напиши ответ на английском</i>"

    try:
        await callback.message.edit_text(text, reply_markup=get_main_menu_keyboard(), parse_mode="HTML")
    except TelegramBadRequest:
        pass

    await state.set_state(DialogueStates.chatting)
    await callback.answer()


@router.message(DialogueStates.chatting)
async def handle_dialogue_message(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_text = message.text

    if not user_text:
        return

    async with async_session() as session:
        user_repo = UserRepository(session)
        user = await user_repo.get_or_create(telegram_id=user_id)

    if user_id not in _conversation_history:
        _conversation_history[user_id] = []

    _conversation_history[user_id].append({"role": "user", "content": user_text})

    try:
        llm = get_llm_provider()
        response = await llm.converse(
            messages=_conversation_history[user_id],
            user_level=user.current_level
        )
        _conversation_history[user_id].append({"role": "assistant", "content": response})
        if len(_conversation_history[user_id]) > 10:
            _conversation_history[user_id] = _conversation_history[user_id][-10:]
        await message.answer(response, parse_mode="HTML")
    except Exception as e:
        await message.answer(
            "Interesting! Tell me more.\\n\\n"
            "<i>(Проверь GROQ_API_KEY в .env)</i>",
            parse_mode="HTML"
        )
`
  },
  {
    path: 'app/telegram/handlers/learn.py',
    description: 'Обучение новым словам',
    content: `from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramBadRequest

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
            await callback.message.edit_text("🎉 Все слова для этого уровня изучены!")
            await callback.answer()
            return

        word = words[0]
        await learning_service.create_user_word(user.id, word.id)
        await session.commit()

        exercise = await learning_service.generate_exercise(word, user)
        _exercise_cache[callback.from_user.id] = exercise

        text = f"📚 <b>Новое слово!</b>\\n\\n🇬🇧 <b>{word.word}</b> {word.pronunciation or ''}\\n🇷🇺 {word.translation}\\n\\n<b>{exercise['question']}</b>"
        keyboard = get_answer_keyboard(exercise['options']) if exercise.get('options') else get_continue_keyboard()

        try:
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
        except TelegramBadRequest:
            pass

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
        is_correct, feedback = await learning_service.process_answer(
            user, word, exercise['type'], user_answer, correct_answer
        )
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
`
  },
  {
    path: 'app/telegram/handlers/review.py',
    description: 'Повторение изученных слов',
    content: `from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramBadRequest
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

        try:
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
        except TelegramBadRequest:
            pass

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
        is_correct, feedback = await learning_service.process_answer(
            user, word, exercise['type'], user_answer, correct_answer
        )
        await session.commit()

    if is_correct:
        text = f"✅ <b>Правильно!</b>\\n\\n🇬🇧 {word.word} — {word.translation}\\n\\n+10 XP"
    else:
        text = f"❌ <b>Неправильно</b>\\n\\nОтвет: <b>{correct_answer}</b>\\n\\n🇬🇧 {word.word} — {word.translation}"

    await callback.message.edit_text(text, reply_markup=get_continue_keyboard(), parse_mode="HTML")
    await callback.answer()
`
  },
  {
    path: 'app/telegram/handlers/progress.py',
    description: 'Статистика пользователя',
    content: `from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
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

        result = await session.execute(
            select(func.count(UserWord.id)).where(
                UserWord.user_id == user.id,
                UserWord.is_learned == 1
            )
        )
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

    try:
        await callback.message.edit_text(
            text,
            reply_markup=get_main_menu_keyboard(),
            parse_mode="HTML"
        )
    except TelegramBadRequest:
        pass
    await callback.answer()
`
  },
  {
    path: 'app/telegram/handlers/start.py',
    description: 'Стартовый обработчик',
    content: `from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.exceptions import TelegramBadRequest

from app.database.base import async_session
from app.repositories.user_repo import UserRepository
from app.telegram.keyboards.main import get_main_menu_keyboard

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    async with async_session() as session:
        user_repo = UserRepository(session)
        user = await user_repo.get_or_create(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
        )
        await session.commit()

    text = f"""🇬🇧 <b>Привет, {message.from_user.first_name}!</b>

Я — твой репетитор английского.

<b>Уровень:</b> {user.current_level}
<b>XP:</b> {user.total_xp}
<b>🔥 Серия:</b> {user.streak_days} дней

Выбери действие:"""

    await message.answer(text, reply_markup=get_main_menu_keyboard(), parse_mode="HTML")


@router.callback_query(F.data == "menu")
async def callback_menu(callback: CallbackQuery):
    async with async_session() as session:
        user_repo = UserRepository(session)
        user = await user_repo.get_or_create(telegram_id=callback.from_user.id)
        await session.commit()

    text = f"<b>🏠 Меню</b>\\n\\nУровень: {user.current_level} | XP: {user.total_xp} | 🔥 {user.streak_days}"

    try:
        await callback.message.edit_text(
            text,
            reply_markup=get_main_menu_keyboard(),
            parse_mode="HTML"
        )
    except TelegramBadRequest:
        pass
    await callback.answer()
`
  },
  {
    path: 'app/ai/providers.py',
    description: 'AI провайдеры (Groq)',
    content: `import os
import aiohttp
from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    async def chat(self, messages: list[dict], temperature: float = 0.7, max_tokens: int = 500) -> str:
        pass

    async def converse(self, messages: list[dict], user_level: str = "A2", known_words: list = None) -> str:
        system_prompt = f"""You are a friendly English conversation partner for a Russian speaker.
Student level: {user_level}
RULES:
1. Use simple vocabulary matching their level
2. Keep responses short (1-3 sentences)
3. Ask follow-up questions
4. If they make a mistake, gently correct: "Better: [correct version]"
5. Don't lecture — just chat!"""
        full_messages = [{"role": "system", "content": system_prompt}] + messages
        return await self.chat(full_messages, temperature=0.8, max_tokens=150)


class GroqProvider(LLMProvider):
    """Groq — БЕСПЛАТНЫЙ AI (Llama 3.3). Получи ключ: https://console.groq.com/"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = "llama-3.3-70b-versatile"
        self.base_url = "https://api.groq.com/openai/v1"

    async def chat(self, messages: list[dict], temperature: float = 0.7, max_tokens: int = 500) -> str:
        if not self.api_key:
            raise ValueError("GROQ_API_KEY не установлен. Добавь в .env файл.")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            ) as response:
                data = await response.json()
                if "choices" in data:
                    return data["choices"][0]["message"]["content"]
                raise ValueError(f"Groq API error: {data}")


def get_llm_provider() -> LLMProvider:
    provider = os.getenv("LLM_PROVIDER", "groq").lower()
    if provider == "groq":
        return GroqProvider()
    raise ValueError(f"Unknown provider: {provider}")
`
  },
  {
    path: 'app/speech/providers.py',
    description: 'Speech провайдеры (TTS)',
    content: `import os
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
    provider = os.getenv("TTS_PROVIDER", "edge").lower()
    if provider == "edge":
        return EdgeTTSProvider()
    raise ValueError(f"Unknown TTS provider: {provider}")
`
  },
  {
    path: 'requirements.txt',
    description: 'Зависимости Python',
    content: `aiogram==3.13.1
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
`
  },
  {
    path: '.env',
    description: 'Конфигурация (ЗАМЕНИ ключи на свои!)',
    content: `# Telegram Bot Token (от @BotFather)
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
`
  },
  {
    path: '.gitignore',
    description: 'Игнорируемые файлы для Git',
    content: `.env
.venv/
__pycache__/
*.pyc
bot_data/
audio_cache/
.idea/
*.db
`
  },
]


function App() {
  const [copiedFile, setCopiedFile] = useState<string | null>(null)

  const copyToClipboard = (text: string, path: string) => {
    navigator.clipboard.writeText(text)
    setCopiedFile(path)
    setTimeout(() => setCopiedFile(null), 2000)
  }

  const downloadFile = (content: string, path: string) => {
    const blob = new Blob([content], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = path.split('/').pop() || 'file.txt'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const downloadAllFiles = () => {
    files.forEach((file, index) => {
      setTimeout(() => {
        downloadFile(file.content, file.path)
      }, index * 300)
    })
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-950 to-slate-900 text-white">
      {/* Header */}
      <div className="border-b border-white/10 bg-black/30 backdrop-blur-xl sticky top-0 z-50">
        <div className="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center text-xl">
              🤖
            </div>
            <div>
              <h1 className="font-bold text-lg">English Bot — Файлы</h1>
              <p className="text-xs text-blue-300">Скопируй или скачай файлы в PyCharm</p>
            </div>
          </div>
          <button
            onClick={downloadAllFiles}
            className="px-4 py-2 bg-green-600 hover:bg-green-500 rounded-lg text-sm font-bold transition-colors"
          >
            ⬇️ Скачать все файлы
          </button>
        </div>
      </div>

      {/* Instructions */}
      <div className="max-w-5xl mx-auto px-4 py-6">
        <div className="bg-blue-500/10 border border-blue-500/30 rounded-xl p-4 mb-6">
          <h2 className="font-bold text-blue-300 mb-2">📋 Инструкция</h2>
          <ol className="list-decimal list-inside space-y-1 text-sm text-slate-300">
            <li>Нажми <b>"Копировать"</b> на каждом файле</li>
            <li>В PyCharm открой файл по пути (например <code className="bg-slate-800 px-1 rounded">app/config.py</code>)</li>
            <li>Выдели всё (<b>Ctrl+A</b>) → Вставь (<b>Ctrl+V</b>) → Сохрани (<b>Ctrl+S</b>)</li>
            <li>После всех файлов — перезапусти бота: <code className="bg-slate-800 px-1 rounded">python -m app.main</code></li>
          </ol>
        </div>

        {/* Files */}
        <div className="space-y-4">
          {files.map((file) => (
            <div key={file.path} className="bg-slate-800/50 border border-slate-700 rounded-xl overflow-hidden">
              {/* File header */}
              <div className="flex items-center justify-between px-4 py-3 bg-slate-800 border-b border-slate-700">
                <div>
                  <code className="text-green-400 font-mono text-sm">{file.path}</code>
                  <p className="text-xs text-slate-400 mt-0.5">{file.description}</p>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => copyToClipboard(file.content, file.path)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                      copiedFile === file.path
                        ? 'bg-green-600 text-white'
                        : 'bg-blue-600 hover:bg-blue-500 text-white'
                    }`}
                  >
                    {copiedFile === file.path ? '✅ Скопировано!' : '📋 Копировать'}
                  </button>
                  <button
                    onClick={() => downloadFile(file.content, file.path)}
                    className="px-3 py-1.5 rounded-lg text-xs font-bold bg-slate-700 hover:bg-slate-600 text-white transition-all"
                  >
                    ⬇️ Скачать
                  </button>
                </div>
              </div>

              {/* File content */}
              <pre className="p-4 overflow-x-auto text-xs leading-relaxed max-h-64 overflow-y-auto">
                <code className="text-slate-300">{file.content}</code>
              </pre>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="mt-8 text-center text-slate-500 text-sm pb-8">
          <p>После обновления всех файлов перезапусти бота:</p>
          <code className="bg-slate-800 px-3 py-1 rounded text-green-400 mt-2 inline-block">
            python -m app.main
          </code>
        </div>
      </div>
    </div>
  )
}

export default App
