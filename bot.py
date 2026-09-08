"""
🤖 Telegram Bot для обучения английскому языку
Полностью автономный бот с голосовым озвучиванием.

Запуск:
    export TELEGRAM_BOT_TOKEN="your_token_here"
    python bot.py
"""

import os
import sys
import random
import asyncio
import logging
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from telegram.constants import ParseMode, ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from lessons import (
    ALL_LESSONS,
    ALL_WORDS,
    GRAMMAR_RULES,
    Word,
    Lesson,
    get_lesson_by_id,
    get_word_by_id,
)
from speech import (
    generate_speech,
    generate_word_audio,
    generate_slow_audio,
    generate_example_audio,
    cleanup_file,
)
from progress import ProgressManager, UserProgress


# ============================================================
# КОНФИГУРАЦИЯ
# ============================================================
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
WORDS_PER_SESSION = 5  # Количество упражнений за сессию

# Типы упражнений
EXERCISE_TYPES = [
    "translate_to_english",
    "translate_to_russian",
    "listen_and_choose",
    "type_word",
    "match_pairs",
]

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ============================================================
# СОСТОЯНИЕ ПОЛЬЗОВАТЕЛЯ (in-memory)
# ============================================================
class UserSession:
    """Хранит текущее состояние пользователя во время упражнения."""
    def __init__(self):
        self.current_word: Optional[Word] = None
        self.exercise_type: str = ""
        self.options: list = []
        self.correct_answer: str = ""
        self.question: str = ""
        self.exercise_count: int = 0
        self.session_correct: int = 0
        self.session_wrong: int = 0
        self.is_practicing: bool = False
        self.waiting_for_text: bool = False
        self.grammar_index: int = 0


# Глобальное хранилище сессий
user_sessions: dict[int, UserSession] = {}
progress_manager = ProgressManager()


def get_session(user_id: int) -> UserSession:
    if user_id not in user_sessions:
        user_sessions[user_id] = UserSession()
    return user_sessions[user_id]


# ============================================================
# ГЕНЕРАЦИЯ УПРАЖНЕНИЙ
# ============================================================
def generate_options(correct: str, all_options: list[str], count: int = 3) -> list[str]:
    """Генерирует варианты ответов."""
    others = [o for o in all_options if o != correct]
    random.shuffle(others)
    selected = others[:count]
    options = [correct] + selected
    random.shuffle(options)
    return options


def create_exercise(word: Word, exercise_type: str, all_words: list[Word]) -> dict:
    """Создаёт упражнение для слова."""
    if exercise_type == "translate_to_english":
        return {
            "type": exercise_type,
            "word": word,
            "question": f"🇷🇺 ➜ 🇬🇧\n\nПереведи на английский:\n\n<b>«{word.russian}»</b>",
            "correct_answer": word.english.lower(),
            "options": None,
        }
    
    elif exercise_type == "translate_to_russian":
        options = generate_options(word.russian, [w.russian for w in all_words])
        return {
            "type": exercise_type,
            "word": word,
            "question": f"🇬🇧 ➜ 🇷🇺\n\nВыбери правильный перевод:\n\n<b>«{word.english}»</b>\n\n<i>{word.transcription}</i>",
            "correct_answer": word.russian,
            "options": options,
        }
    
    elif exercise_type == "listen_and_choose":
        options = generate_options(word.english, [w.english for w in all_words])
        return {
            "type": exercise_type,
            "word": word,
            "question": "🔊 <b>Послушай и выбери слово</b>\n\n(Нажми ▶️ чтобы прослушать)",
            "correct_answer": word.english,
            "options": options,
        }
    
    elif exercise_type == "type_word":
        # Подсказка: первая буква
        hint = word.english[0] + "_" * (len(word.english) - 1)
        return {
            "type": exercise_type,
            "word": word,
            "question": f"⌨️ <b>Напиши по-английски:</b>\n\n🇷🇺 «{word.russian}»\n\n💡 Подсказка: <code>{hint}</code>\n🔤 Транскрипция: <code>{word.transcription}</code>",
            "correct_answer": word.english.lower(),
            "options": None,
        }
    
    elif exercise_type == "match_pairs":
        options = generate_options(word.russian, [w.russian for w in all_words])
        return {
            "type": exercise_type,
            "word": word,
            "question": f"🔗 <b>Соедини пару:</b>\n\n🇬🇧 <b>«{word.english}»</b> = ?",
            "correct_answer": word.russian,
            "options": options,
        }
    
    return {}


# ============================================================
# КОМАНДА /start
# ============================================================
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start."""
    user = update.effective_user
    progress = await progress_manager.get_user(user.id, user.username or "")
    
    welcome_text = f"""
🎓 <b>Привет, {user.first_name}!</b>

Я — твой персональный репетитор английского языка! 🤖

📚 <b>Что я умею:</b>
• Учить слова с произношением 🔊
• Проводить интерактивные упражнения
• Следить за твоим прогрессом 📊
• Объяснять грамматику 📝

🎯 <b>У тебя уже:</b>
• Изучено слов: {len(progress.learned_words)}
• Уровень: {progress.level} ⭐
• XP: {progress.total_xp}

Выбери действие:
"""
    
    keyboard = [
        [InlineKeyboardButton("📖 Начать урок", callback_data="start_lesson")],
        [InlineKeyboardButton("🏋️ Практика слов", callback_data="start_practice")],
        [InlineKeyboardButton("📝 Грамматика", callback_data="show_grammar")],
        [InlineKeyboardButton("📊 Мой прогресс", callback_data="show_stats")],
        [InlineKeyboardButton("📚 Все уроки", callback_data="show_lessons")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_text,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup,
    )


# ============================================================
# КОМАНДА /learn — Начать урок
# ============================================================
async def cmd_learn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начать новый урок."""
    user = update.effective_user
    progress = await progress_manager.get_user(user.id)
    
    lesson_index = progress.current_lesson_index % len(ALL_LESSONS)
    lesson = ALL_LESSONS[lesson_index]
    
    text = f"""
📖 <b>Урок {lesson_index + 1}: {lesson.title}</b>

{lesson.description}

📝 Слов в уроке: {len(lesson.words)}
🎯 Уровень: {'⭐' * lesson.level}

Начинаем обучение? Каждое слово будет с произношением! 🔊
"""
    
    keyboard = [
        [InlineKeyboardButton("▶️ Начать урок", callback_data=f"begin_lesson_{lesson_index}")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup,
    )


# ============================================================
# КОМАНДА /practice — Практика
# ============================================================
async def cmd_practice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начать практику слов."""
    user = update.effective_user
    progress = await progress_manager.get_user(user.id)
    
    # Если есть слова на повторение — предложить их
    if progress.words_to_repeat:
        text = f"""
🔄 <b>Повторение</b>

У тебя {len(progress.words_to_repeat)} слов на повторении!

Давай повторим их, чтобы закрепить? 🧠
"""
        keyboard = [
            [InlineKeyboardButton("🔄 Повторить ошибки", callback_data="practice_repeat")],
            [InlineKeyboardButton("📖 Новый урок", callback_data="start_lesson")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")],
        ]
    else:
        text = f"""
🏋️ <b>Практика</b>

Готов к упражнениям? Будем тренировать слова из текущего урока!

💪 Упражнений за сессию: {WORDS_PER_SESSION}
"""
        keyboard = [
            [InlineKeyboardButton("🏋️ Начать практику", callback_data="start_practice_go")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")],
        ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup)


# ============================================================
# КОМАНДА /vocab — Словарь
# ============================================================
async def cmd_vocab(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать изученные слова."""
    user = update.effective_user
    progress = await progress_manager.get_user(user.id)
    
    if not progress.learned_words:
        await update.message.reply_text(
            "📚 <b>Словарь пуст</b>\n\nТы ещё не выучил ни одного слова.\nНачни урок с помощью /learn!",
            parse_mode=ParseMode.HTML,
        )
        return
    
    # Показываем первые 10 слов
    words_to_show = progress.learned_words[:10]
    text = f"📚 <b>Твой словарь</b> ({len(progress.learned_words)} слов)\n\n"
    
    for word_id in words_to_show:
        word = get_word_by_id(word_id)
        if word:
            text += f"• <b>{word.english}</b> — {word.russian} {word.transcription}\n"
    
    if len(progress.learned_words) > 10:
        text += f"\n... и ещё {len(progress.learned_words) - 10} слов"
    
    keyboard = [
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup)


# ============================================================
# КОМАНДА /grammar — Грамматика
# ============================================================
async def cmd_grammar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать грамматические правила."""
    session = get_session(update.effective_user.id)
    session.grammar_index = 0
    
    rule = GRAMMAR_RULES[0]
    text = f"""
📝 <b>Грамматика: {rule.title}</b>
⭐ Уровень: {'⭐' * rule.level}

{rule.explanation}

<b>Примеры:</b>
"""
    for ex in rule.examples:
        text += f"\n🇬🇧 {ex['english']}\n🇷🇺 {ex['russian']}\n"
    
    keyboard = [
        [InlineKeyboardButton("▶️ Прослушать примеры", callback_data=f"grammar_audio_{0}")],
        [InlineKeyboardButton("➡️ Следующее правило", callback_data="grammar_next")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup)


# ============================================================
# КОМАНДА /stats — Статистика
# ============================================================
async def cmd_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать статистику."""
    user = update.effective_user
    progress = await progress_manager.get_user(user.id)
    
    # Прогресс до следующего уровня
    current_level_xp = (progress.level - 1) * 100
    next_level_xp = progress.level * 100
    xp_progress = progress.total_xp - current_level_xp
    xp_needed = next_level_xp - current_level_xp
    progress_bar_len = 10
    filled = int(xp_progress / xp_needed * progress_bar_len)
    bar = "█" * filled + "░" * (progress_bar_len - filled)
    
    text = f"""
📊 <b>Твоя статистика</b>

👤 {user.first_name}
⭐ Уровень: <b>{progress.level}</b>
✨ XP: {progress.total_xp}
📈 Прогресс: [{bar}] {xp_progress}/{xp_needed}

📚 Изучено слов: <b>{len(progress.learned_words)}</b> из {len(ALL_WORDS)}
✅ Правильных ответов: {progress.correct_answers}
❌ Ошибок: {progress.wrong_answers}
🎯 Точность: {progress.accuracy}%

🔥 Текущая серия: {progress.streak}
🏆 Лучшая серия: {progress.best_streak}
🔄 На повторении: {len(progress.words_to_repeat)}
📅 Сессий: {progress.total_sessions}
"""
    
    keyboard = [
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup)


# ============================================================
# КОМАНДА /reset — Сброс
# ============================================================
async def cmd_reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сбросить прогресс."""
    keyboard = [
        [InlineKeyboardButton("⚠️ Да, сбросить", callback_data="confirm_reset")],
        [InlineKeyboardButton("🔙 Отмена", callback_data="back_to_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "⚠️ <b>Ты уверен?</b>\n\nВесь прогресс будет удалён!",
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup,
    )


# ============================================================
# ОБРАБОТКА CALLBACK КНОПОК
# ============================================================
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка нажатий inline-кнопок."""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = query.data
    session = get_session(user_id)
    progress = await progress_manager.get_user(user_id, query.from_user.username or "")
    
    # === НАВИГАЦИЯ ===
    if data == "back_to_menu":
        await cmd_start(update, context)
        return
    
    # === НАЧАЛО УРОКА ===
    elif data == "start_lesson":
        lesson_index = progress.current_lesson_index % len(ALL_LESSONS)
        lesson = ALL_LESSONS[lesson_index]
        
        text = f"""
📖 <b>Урок {lesson_index + 1}: {lesson.title}</b>

{lesson.description}

📝 Слов: {len(lesson.words)} | 🎯 Уровень: {'⭐' * lesson.level}
"""
        keyboard = [
            [InlineKeyboardButton("▶️ Начать", callback_data=f"begin_lesson_{lesson_index}")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")],
        ]
        await query.edit_message_text(text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
    
    elif data.startswith("begin_lesson_"):
        lesson_index = int(data.split("_")[2])
        lesson = ALL_LESSONS[lesson_index % len(ALL_LESSONS)]
        
        session.is_practicing = True
        session.exercise_count = 0
        session.session_correct = 0
        session.session_wrong = 0
        
        progress.total_sessions += 1
        await progress_manager.save_user(progress)
        
        # Начать с первого слова
        await send_word_introduction(query, context, lesson.words[0], lesson)
    
    # === ПРАКТИКА ===
    elif data == "start_practice" or data == "start_practice_go":
        session.is_practicing = True
        session.exercise_count = 0
        session.session_correct = 0
        session.session_wrong = 0
        
        progress.total_sessions += 1
        await progress_manager.save_user(progress)
        
        lesson_index = progress.current_lesson_index % len(ALL_LESSONS)
        lesson = ALL_LESSONS[lesson_index]
        word_index = progress.current_word_index % len(lesson.words)
        
        await send_exercise(query, context, lesson, word_index)
    
    elif data == "practice_repeat":
        if not progress.words_to_repeat:
            await query.edit_message_text("🎉 Нет слов на повторении!")
            return
        
        session.is_practicing = True
        session.exercise_count = 0
        session.session_correct = 0
        session.session_wrong = 0
        
        # Взять слово на повторение
        word_id = progress.words_to_repeat[0]
        word = get_word_by_id(word_id)
        if word:
            lesson_index = progress.current_lesson_index % len(ALL_LESSONS)
            lesson = ALL_LESSONS[lesson_index]
            exercise_type = random.choice(EXERCISE_TYPES)
            exercise = create_exercise(word, exercise_type, lesson.words)
            session.current_word = word
            session.exercise_type = exercise_type
            session.correct_answer = exercise["correct_answer"]
            session.options = exercise.get("options")
            session.question = exercise["question"]
            
            await send_exercise_message(query, context, exercise, word)
    
    # === ВЫБОР ОТВЕТА (кнопки) ===
    elif data.startswith("answer_"):
        answer_index = int(data.split("_")[1])
        if session.options and answer_index < len(session.options):
            answer = session.options[answer_index]
            await process_answer(query, context, answer, progress)
    
    # === ПРОСЛУШАТЬ СЛОВО ===
    elif data.startswith("listen_word_"):
        word_id = data.replace("listen_word_", "")
        word = get_word_by_id(word_id)
        if word:
            await context.bot.send_chat_action(chat_id=query.message.chat_id, action=ChatAction.RECORD_AUDIO)
            audio_path = generate_word_audio(word.english)
            if audio_path:
                with open(audio_path, "rb") as audio:
                    await query.message.reply_audio(audio=audio, title=f"{word.english}", performer="🎓 English Bot")
                cleanup_file(audio_path)
    
    elif data.startswith("listen_slow_"):
        word_id = data.replace("listen_slow_", "")
        word = get_word_by_id(word_id)
        if word:
            await context.bot.send_chat_action(chat_id=query.message.chat_id, action=ChatAction.RECORD_AUDIO)
            audio_path = generate_slow_audio(word.english)
            if audio_path:
                with open(audio_path, "rb") as audio:
                    await query.message.reply_audio(audio=audio, title=f"{word.english} (slow)", performer="🐢 Slow mode")
                cleanup_file(audio_path)
    
    elif data.startswith("listen_example_"):
        word_id = data.replace("listen_example_", "")
        word = get_word_by_id(word_id)
        if word:
            await context.bot.send_chat_action(chat_id=query.message.chat_id, action=ChatAction.RECORD_AUDIO)
            audio_path = generate_example_audio(word.example)
            if audio_path:
                with open(audio_path, "rb") as audio:
                    await query.message.reply_audio(audio=audio, title="Example", performer="🎓 English Bot")
                cleanup_file(audio_path)
    
    # === ПРОДОЛЖИТЬ ПОСЛЕ СЛОВА ===
    elif data == "next_word":
        lesson_index = progress.current_lesson_index % len(ALL_LESSONS)
        lesson = ALL_LESSONS[lesson_index]
        word_index = progress.current_word_index % len(lesson.words)
        
        if session.exercise_count >= WORDS_PER_SESSION:
            await show_session_result(query, context, session, progress)
        else:
            await send_word_introduction(query, context, lesson.words[word_index], lesson)
    
    elif data == "next_exercise":
        lesson_index = progress.current_lesson_index % len(ALL_LESSONS)
        lesson = ALL_LESSONS[lesson_index]
        word_index = progress.current_word_index % len(lesson.words)
        
        if session.exercise_count >= WORDS_PER_SESSION:
            await show_session_result(query, context, session, progress)
        else:
            await send_exercise(query, context, lesson, word_index)
    
    # === ГРАММАТИКА ===
    elif data == "show_grammar":
        session.grammar_index = 0
        rule = GRAMMAR_RULES[0]
        text = f"📝 <b>Грамматика: {rule.title}</b>\n⭐ Уровень: {'⭐' * rule.level}\n\n{rule.explanation}\n\n<b>Примеры:</b>\n"
        for ex in rule.examples:
            text += f"\n🇬🇧 {ex['english']}\n🇷🇺 {ex['russian']}\n"
        
        keyboard = [
            [InlineKeyboardButton("▶️ Прослушать", callback_data=f"grammar_audio_{0}")],
            [InlineKeyboardButton("➡️ Далее", callback_data="grammar_next")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")],
        ]
        await query.edit_message_text(text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
    
    elif data == "grammar_next":
        session.grammar_index = (session.grammar_index + 1) % len(GRAMMAR_RULES)
        rule = GRAMMAR_RULES[session.grammar_index]
        text = f"📝 <b>Грамматика: {rule.title}</b>\n⭐ Уровень: {'⭐' * rule.level}\n\n{rule.explanation}\n\n<b>Примеры:</b>\n"
        for ex in rule.examples:
            text += f"\n🇬🇧 {ex['english']}\n🇷🇺 {ex['russian']}\n"
        
        keyboard = [
            [InlineKeyboardButton("▶️ Прослушать", callback_data=f"grammar_audio_{session.grammar_index}")],
            [InlineKeyboardButton("➡️ Далее", callback_data="grammar_next")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")],
        ]
        await query.edit_message_text(text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
    
    elif data.startswith("grammar_audio_"):
        idx = int(data.split("_")[2])
        rule = GRAMMAR_RULES[idx]
        await context.bot.send_chat_action(chat_id=query.message.chat_id, action=ChatAction.RECORD_AUDIO)
        
        for ex in rule.examples:
            audio_path = generate_speech(ex["english"], lang="en")
            if audio_path:
                with open(audio_path, "rb") as audio:
                    await query.message.reply_audio(
                        audio=audio,
                        title=ex["english"],
                        performer="📝 Grammar",
                    )
                cleanup_file(audio_path)
    
    # === СПИСОК УРОКОВ ===
    elif data == "show_lessons":
        text = "📚 <b>Все уроки:</b>\n\n"
        for i, lesson in enumerate(ALL_LESSONS):
            status = "✅" if i < progress.current_lesson_index else "📖" if i == progress.current_lesson_index else "🔒"
            text += f"{status} <b>{lesson.title}</b> — {lesson.description}\n"
        
        keyboard = [
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")],
        ]
        await query.edit_message_text(text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
    
    # === СТАТИСТИКА ===
    elif data == "show_stats":
        current_level_xp = (progress.level - 1) * 100
        next_level_xp = progress.level * 100
        xp_progress = progress.total_xp - current_level_xp
        xp_needed = next_level_xp - current_level_xp
        filled = int(xp_progress / xp_needed * 10)
        bar = "█" * filled + "░" * (10 - filled)
        
        text = f"""
📊 <b>Статистика</b>

⭐ Уровень: <b>{progress.level}</b>
✨ XP: {progress.total_xp}
📈 [{bar}] {xp_progress}/{xp_needed}

📚 Слов: <b>{len(progress.learned_words)}</b>/{len(ALL_WORDS)}
✅ Правильно: {progress.correct_answers}
❌ Ошибок: {progress.wrong_answers}
🎯 Точность: {progress.accuracy}%
🔥 Серия: {progress.streak} | 🏆 Рекорд: {progress.best_streak}
"""
        keyboard = [
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")],
        ]
        await query.edit_message_text(text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
    
    # === СБРОС ===
    elif data == "confirm_reset":
        await progress_manager.reset_user(user_id)
        await query.edit_message_text("✅ Прогресс сброшен! Используй /start чтобы начать заново.")
    
    # === ПРОПУСК ===
    elif data == "skip_exercise":
        lesson_index = progress.current_lesson_index % len(ALL_LESSONS)
        lesson = ALL_LESSONS[lesson_index]
        word_index = progress.current_word_index % len(lesson.words)
        
        session.exercise_count += 1
        await progress_manager.advance_word(progress, len(lesson.words))
        
        if session.exercise_count >= WORDS_PER_SESSION:
            await show_session_result(query, context, session, progress)
        else:
            await send_exercise(query, context, lesson, progress.current_word_index % len(lesson.words))


# ============================================================
# ОТПРАВКА СЛОВА С ОЗВУЧИВАНИЕМ
# ============================================================
async def send_word_introduction(query, context, word: Word, lesson: Lesson):
    """Показывает новое слово с произношением."""
    text = f"""
📖 <b>Новое слово!</b>

🇬🇧 <b>{word.english}</b> {word.transcription}
🇷🇺 {word.russian}

💬 <i>Пример:</i>
🇬🇧 {word.example}
🇷🇺 {word.example_translation}
"""
    
    keyboard = [
        [
            InlineKeyboardButton("🔊 Произношение", callback_data=f"listen_word_{word.id}"),
            InlineKeyboardButton("🐢 Медленно", callback_data=f"listen_slow_{word.id}"),
        ],
        [InlineKeyboardButton("💬 Пример", callback_data=f"listen_example_{word.id}")],
        [InlineKeyboardButton("✅ Далее →", callback_data="next_word")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await query.edit_message_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup)
    except Exception:
        await query.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup)
    
    # Автоматически отправить аудио
    await context.bot.send_chat_action(chat_id=query.message.chat_id, action=ChatAction.RECORD_AUDIO)
    audio_path = generate_word_audio(word.english)
    if audio_path:
        try:
            with open(audio_path, "rb") as audio:
                await query.message.reply_audio(
                    audio=audio,
                    title=f"🔊 {word.english}",
                    performer="🎓 English Bot",
                )
        except Exception as e:
            logger.error(f"Error sending audio: {e}")
        finally:
            cleanup_file(audio_path)


# ============================================================
# ОТПРАВКА УПРАЖНЕНИЯ
# ============================================================
async def send_exercise(query, context, lesson: Lesson, word_index: int):
    """Создаёт и отправляет упражнение."""
    session = get_session(query.from_user.id)
    word = lesson.words[word_index % len(lesson.words)]
    
    exercise_type = random.choice(EXERCISE_TYPES)
    exercise = create_exercise(word, exercise_type, lesson.words)
    
    session.current_word = word
    session.exercise_type = exercise_type
    session.correct_answer = exercise["correct_answer"]
    session.options = exercise.get("options")
    session.question = exercise["question"]
    session.waiting_for_text = exercise_type in ("translate_to_english", "type_word")
    
    await send_exercise_message(query, context, exercise, word)


async def send_exercise_message(query, context, exercise: dict, word: Word):
    """Отправляет сообщение с упражнением."""
    session = get_session(query.from_user.id)
    
    text = f"{exercise['question']}\n\n"
    text += f"<i>Упражнение {session.exercise_count + 1}/{WORDS_PER_SESSION}</i>"
    
    keyboard = []
    
    if exercise.get("options"):
        # Кнопочный ответ
        for i, option in enumerate(exercise["options"]):
            keyboard.append([InlineKeyboardButton(option, callback_data=f"answer_{i}")])
        
        # Для аудирования — кнопка прослушать
        if exercise["type"] == "listen_and_choose":
            keyboard.insert(0, [
                InlineKeyboardButton("🔊 Прослушать", callback_data=f"listen_word_{word.id}"),
                InlineKeyboardButton("🐢 Медленно", callback_data=f"listen_slow_{word.id}"),
            ])
    else:
        # Текстовый ввод
        text += "\n\n💬 <i>Напиши ответ текстом:</i>"
        session.waiting_for_text = True
    
    keyboard.append([InlineKeyboardButton("⏭ Пропустить", callback_data="skip_exercise")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await query.edit_message_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup)
    except Exception:
        await query.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup)
    
    # Для аудирования — автоматически отправить аудио
    if exercise["type"] == "listen_and_choose":
        await context.bot.send_chat_action(chat_id=query.message.chat_id, action=ChatAction.RECORD_AUDIO)
        audio_path = generate_word_audio(word.english)
        if audio_path:
            try:
                with open(audio_path, "rb") as audio:
                    await query.message.reply_audio(
                        audio=audio,
                        title="🔊 Listen!",
                        performer="🎓 English Bot",
                    )
            except Exception as e:
                logger.error(f"Error sending audio: {e}")
            finally:
                cleanup_file(audio_path)


# ============================================================
# ОБРАБОТКА ТЕКСТОВЫХ ОТВЕТОВ
# ============================================================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка текстовых сообщений (ответы на упражнения)."""
    user_id = update.effective_user.id
    session = get_session(user_id)
    
    if not session.is_practicing or not session.waiting_for_text:
        # Если не в режиме практики — показать подсказку
        await update.message.reply_text(
            "💡 Используй /learn для урока или /practice для практики!\n\n"
            "Или нажми кнопку в меню.",
        )
        return
    
    answer = update.message.text.strip()
    progress = await progress_manager.get_user(user_id)
    
    await process_answer_text(update, context, answer, progress)


async def process_answer(query, context, answer: str, progress: UserProgress):
    """Обработка ответа с inline-кнопки."""
    session = get_session(query.from_user.id)
    is_correct = answer.lower().strip() == session.correct_answer.lower().strip()
    
    await show_answer_result(query, context, is_correct, progress, session)


async def process_answer_text(update: Update, context: ContextTypes.DEFAULT_TYPE, answer: str, progress: UserProgress):
    """Обработка текстового ответа."""
    session = get_session(update.effective_user.id)
    is_correct = answer.lower().strip() == session.correct_answer.lower().strip()
    
    session.waiting_for_text = False
    
    if is_correct:
        xp = await progress_manager.record_correct_answer(progress, session.current_word.id, 10)
        text = f"""
✅ <b>Правильно!</b> 🎉

🇬🇧 <b>{session.current_word.english}</b> — {session.current_word.russian}
💬 {session.current_word.example}

+{xp} XP 🔥 Серия: {progress.streak}
"""
    else:
        await progress_manager.record_wrong_answer(progress, session.current_word.id)
        text = f"""
❌ <b>Неправильно</b>

Правильный ответ: <b>{session.correct_answer}</b>

🇬🇧 <b>{session.current_word.english}</b> — {session.current_word.russian}
💬 {session.current_word.example}
🇷🇺 {session.current_word.example_translation}
"""
    
    session.exercise_count += 1
    if is_correct:
        session.session_correct += 1
    else:
        session.session_wrong += 1
    
    lesson_index = progress.current_lesson_index % len(ALL_LESSONS)
    lesson = ALL_LESSONS[lesson_index]
    await progress_manager.advance_word(progress, len(lesson.words))
    
    keyboard = []
    
    # Кнопка прослушать правильный ответ
    keyboard.append([
        InlineKeyboardButton("🔊 Произношение", callback_data=f"listen_word_{session.current_word.id}"),
    ])
    
    if session.exercise_count >= WORDS_PER_SESSION:
        keyboard.append([InlineKeyboardButton("📊 Результаты", callback_data="next_exercise")])
    else:
        keyboard.append([InlineKeyboardButton("✅ Далее →", callback_data="next_exercise")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup)
    
    # Отправить аудио правильного ответа
    await context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.RECORD_AUDIO)
    audio_path = generate_word_audio(session.current_word.english)
    if audio_path:
        try:
            with open(audio_path, "rb") as audio:
                await update.message.reply_audio(
                    audio=audio,
                    title=f"🔊 {session.current_word.english}",
                    performer="🎓 English Bot",
                )
        except Exception as e:
            logger.error(f"Error sending audio: {e}")
        finally:
            cleanup_file(audio_path)


async def show_answer_result(query, context, is_correct: bool, progress: UserProgress, session: UserSession):
    """Показывает результат ответа."""
    session.waiting_for_text = False
    
    if is_correct:
        xp = await progress_manager.record_correct_answer(progress, session.current_word.id, 10)
        text = f"""
✅ <b>Правильно!</b> 🎉

🇬🇧 <b>{session.current_word.english}</b> — {session.current_word.russian}
💬 {session.current_word.example}

+{xp} XP 🔥 Серия: {progress.streak}
"""
        session.session_correct += 1
    else:
        await progress_manager.record_wrong_answer(progress, session.current_word.id)
        text = f"""
❌ <b>Неправильно</b>

Правильный ответ: <b>{session.correct_answer}</b>

🇬🇧 <b>{session.current_word.english}</b> — {session.current_word.russian}
💬 {session.current_word.example}
🇷🇺 {session.current_word.example_translation}
"""
        session.session_wrong += 1
    
    session.exercise_count += 1
    lesson_index = progress.current_lesson_index % len(ALL_LESSONS)
    lesson = ALL_LESSONS[lesson_index]
    await progress_manager.advance_word(progress, len(lesson.words))
    
    keyboard = []
    keyboard.append([
        InlineKeyboardButton("🔊 Произношение", callback_data=f"listen_word_{session.current_word.id}"),
    ])
    
    if session.exercise_count >= WORDS_PER_SESSION:
        keyboard.append([InlineKeyboardButton("📊 Результаты", callback_data="next_exercise")])
    else:
        keyboard.append([InlineKeyboardButton("✅ Далее →", callback_data="next_exercise")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await query.edit_message_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup)
    except Exception:
        await query.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup)


# ============================================================
# РЕЗУЛЬТАТЫ СЕССИИ
# ============================================================
async def show_session_result(query, context, session: UserSession, progress: UserProgress):
    """Показывает результаты завершённой сессии."""
    session.is_practicing = False
    session.waiting_for_text = False
    
    total = session.session_correct + session.session_wrong
    accuracy = round(session.session_correct / total * 100) if total > 0 else 0
    
    # Оценка
    if accuracy >= 90:
        grade = "🏆 Отлично!"
        emoji = "🌟"
    elif accuracy >= 70:
        grade = "👍 Хорошо!"
        emoji = "😊"
    elif accuracy >= 50:
        grade = "💪 Неплохо!"
        emoji = "🤔"
    else:
        grade = "📚 Нужно больше практики"
        emoji = "😅"
    
    text = f"""
{emoji} <b>Сессия завершена!</b>

{grade}

📊 <b>Результаты:</b>
✅ Правильно: {session.session_correct}
❌ Ошибок: {session.session_wrong}
🎯 Точность: {accuracy}%

📈 <b>Общий прогресс:</b>
⭐ Уровень: {progress.level}
✨ XP: {progress.total_xp}
📚 Слов изучено: {len(progress.learned_words)}
🔥 Серия: {progress.streak}

{f'🔄 Слов на повторении: {len(progress.words_to_repeat)}' if progress.words_to_repeat else ''}
"""
    
    keyboard = [
        [InlineKeyboardButton("📖 Следующий урок", callback_data="start_lesson")],
        [InlineKeyboardButton("🏋️ Ещё практика", callback_data="start_practice_go")],
        [InlineKeyboardButton("📊 Статистика", callback_data="show_stats")],
        [InlineKeyboardButton("🏠 В меню", callback_data="back_to_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await query.edit_message_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup)
    except Exception:
        await query.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup)


# ============================================================
# ЗАПУСК БОТА
# ============================================================
def main():
    """Запуск бота."""
    if not BOT_TOKEN:
        print("❌ Ошибка: TELEGRAM_BOT_TOKEN не установлен!")
        print("Установите переменную окружения:")
        print('  export TELEGRAM_BOT_TOKEN="your_token_here"')
        sys.exit(1)
    
    print("🤖 Запуск English Learning Bot...")
    print(f"📚 Уроков: {len(ALL_LESSONS)}")
    print(f"📝 Слов: {len(ALL_WORDS)}")
    print(f"📝 Грамматических правил: {len(GRAMMAR_RULES)}")
    
    # Инициализация БД
    loop = asyncio.new_event_loop()
    loop.run_until_complete(progress_manager.init_db())
    
    # Создание приложения
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Регистрация обработчиков
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("learn", cmd_learn))
    app.add_handler(CommandHandler("practice", cmd_practice))
    app.add_handler(CommandHandler("vocab", cmd_vocab))
    app.add_handler(CommandHandler("grammar", cmd_grammar))
    app.add_handler(CommandHandler("stats", cmd_stats))
    app.add_handler(CommandHandler("reset", cmd_reset))
    
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print("✅ Бот запущен! Ожидание сообщений...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
