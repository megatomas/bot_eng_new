"""Telegram inline keyboards for the bot."""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Main menu keyboard."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📚 Учить новые слова", callback_data="learn_new")],
        [InlineKeyboardButton(text="🔁 Повторить", callback_data="review")],
        [InlineKeyboardButton(text="⚡ Быстрая тренировка", callback_data="quick_practice")],
        [InlineKeyboardButton(text="💬 Поговорить", callback_data="dialogue")],
        [InlineKeyboardButton(text="📊 Мой прогресс", callback_data="progress")],
        [InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")],
    ])
    return keyboard


def get_answer_keyboard(options: list[str], prefix: str = "ans") -> InlineKeyboardMarkup:
    """Keyboard with answer options."""
    buttons = []
    for i, option in enumerate(options):
        buttons.append([InlineKeyboardButton(
            text=option,
            callback_data=f"{prefix}_{i}"
        )])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_exercise_navigation_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for navigating between exercises."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⏭️ Пропустить", callback_data="skip"),
            InlineKeyboardButton(text="💡 Подсказка", callback_data="hint"),
        ],
        [InlineKeyboardButton(text="🏠 В меню", callback_data="menu")],
    ])
    return keyboard


def get_continue_keyboard() -> InlineKeyboardMarkup:
    """Keyboard to continue to next exercise."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Далее", callback_data="next_exercise")],
        [InlineKeyboardButton(text="🏠 В меню", callback_data="menu")],
    ])
    return keyboard


def get_settings_keyboard() -> InlineKeyboardMarkup:
    """Settings menu keyboard."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⏰ Время напоминаний", callback_data="set_reminders")],
        [InlineKeyboardButton(text="🎯 Дневная цель", callback_data="set_goal")],
        [InlineKeyboardButton(text="📈 Сбросить прогресс", callback_data="reset_progress")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="menu")],
    ])
    return keyboard
