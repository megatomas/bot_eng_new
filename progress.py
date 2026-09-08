"""
Модуль управления прогрессом пользователей.
Использует SQLite для хранения данных.
"""

import aiosqlite
import json
import time
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional


DB_PATH = Path("bot_data/progress.db")
DB_PATH.parent.mkdir(exist_ok=True)


@dataclass
class UserProgress:
    user_id: int
    learned_words: List[str] = field(default_factory=list)
    correct_answers: int = 0
    wrong_answers: int = 0
    current_lesson_index: int = 0
    current_word_index: int = 0
    streak: int = 0
    best_streak: int = 0
    total_xp: int = 0
    level: int = 1
    last_practice_date: str = ""
    words_to_repeat: List[str] = field(default_factory=list)
    total_sessions: int = 0
    username: str = ""
    
    @property
    def accuracy(self) -> float:
        total = self.correct_answers + self.wrong_answers
        if total == 0:
            return 0.0
        return round(self.correct_answers / total * 100, 1)
    
    @property
    def xp_to_next_level(self) -> int:
        return (self.level * 100) - self.total_xp


class ProgressManager:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or str(DB_PATH)
    
    async def init_db(self):
        """Инициализация базы данных."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT DEFAULT '',
                    learned_words TEXT DEFAULT '[]',
                    correct_answers INTEGER DEFAULT 0,
                    wrong_answers INTEGER DEFAULT 0,
                    current_lesson_index INTEGER DEFAULT 0,
                    current_word_index INTEGER DEFAULT 0,
                    streak INTEGER DEFAULT 0,
                    best_streak INTEGER DEFAULT 0,
                    total_xp INTEGER DEFAULT 0,
                    level INTEGER DEFAULT 1,
                    last_practice_date TEXT DEFAULT '',
                    words_to_repeat TEXT DEFAULT '[]',
                    total_sessions INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            await db.commit()
    
    async def get_user(self, user_id: int, username: str = "") -> UserProgress:
        """Получить прогресс пользователя или создать нового."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM users WHERE user_id = ?", (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                
                if row:
                    return UserProgress(
                        user_id=row["user_id"],
                        learned_words=json.loads(row["learned_words"]),
                        correct_answers=row["correct_answers"],
                        wrong_answers=row["wrong_answers"],
                        current_lesson_index=row["current_lesson_index"],
                        current_word_index=row["current_word_index"],
                        streak=row["streak"],
                        best_streak=row["best_streak"],
                        total_xp=row["total_xp"],
                        level=row["level"],
                        last_practice_date=row["last_practice_date"],
                        words_to_repeat=json.loads(row["words_to_repeat"]),
                        total_sessions=row["total_sessions"],
                        username=row["username"],
                    )
                else:
                    # Создать нового пользователя
                    progress = UserProgress(
                        user_id=user_id,
                        username=username,
                    )
                    await self.save_user(progress)
                    return progress
    
    async def save_user(self, progress: UserProgress):
        """Сохранить прогресс пользователя."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT OR REPLACE INTO users 
                (user_id, username, learned_words, correct_answers, wrong_answers,
                 current_lesson_index, current_word_index, streak, best_streak,
                 total_xp, level, last_practice_date, words_to_repeat, total_sessions)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                progress.user_id,
                progress.username,
                json.dumps(progress.learned_words),
                progress.correct_answers,
                progress.wrong_answers,
                progress.current_lesson_index,
                progress.current_word_index,
                progress.streak,
                progress.best_streak,
                progress.total_xp,
                progress.level,
                progress.last_practice_date,
                json.dumps(progress.words_to_repeat),
                progress.total_sessions,
            ))
            await db.commit()
    
    async def record_correct_answer(self, progress: UserProgress, word_id: str, xp: int):
        """Записать правильный ответ."""
        progress.correct_answers += 1
        progress.streak += 1
        if progress.streak > progress.best_streak:
            progress.best_streak = progress.streak
        
        # XP с бонусом за серию
        bonus_xp = xp + min(progress.streak * 2, 20)
        progress.total_xp += bonus_xp
        
        # Обновить уровень
        progress.level = (progress.total_xp // 100) + 1
        
        # Добавить слово в изученные
        if word_id not in progress.learned_words:
            progress.learned_words.append(word_id)
        
        # Убрать из повтора
        if word_id in progress.words_to_repeat:
            progress.words_to_repeat.remove(word_id)
        
        await self.save_user(progress)
        return bonus_xp
    
    async def record_wrong_answer(self, progress: UserProgress, word_id: str):
        """Записать неправильный ответ."""
        progress.wrong_answers += 1
        progress.streak = 0
        
        # Добавить в очередь повторения
        if word_id not in progress.words_to_repeat:
            progress.words_to_repeat.append(word_id)
        
        await self.save_user(progress)
    
    async def advance_word(self, progress: UserProgress, total_words_in_lesson: int):
        """Перейти к следующему слову."""
        progress.current_word_index += 1
        if progress.current_word_index >= total_words_in_lesson:
            progress.current_word_index = 0
            progress.current_lesson_index += 1
        await self.save_user(progress)
    
    async def reset_user(self, user_id: int):
        """Сбросить прогресс пользователя."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            await db.commit()
    
    async def get_all_users_count(self) -> int:
        """Получить количество пользователей."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT COUNT(*) FROM users") as cursor:
                row = await cursor.fetchone()
                return row[0] if row else 0
