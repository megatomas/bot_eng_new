"""
Модуль голосового озвучивания с использованием Google Text-to-Speech.
Генерирует аудиофайлы из текста для отправки в Telegram.
"""

import os
import uuid
import asyncio
from pathlib import Path
from gtts import gTTS


# Директория для временных аудиофайлов
AUDIO_DIR = Path("audio_cache")
AUDIO_DIR.mkdir(exist_ok=True)


def generate_speech(text: str, lang: str = "en", slow: bool = False) -> str:
    """
    Генерирует аудиофайл из текста.
    
    Args:
        text: Текст для озвучивания
        lang: Язык ('en' для английского, 'ru' для русского)
        slow: Замедленное воспроизведение
    
    Returns:
        Путь к сгенерированному аудиофайлу
    """
    # Уникальное имя файла
    filename = f"{uuid.uuid4().hex}.mp3"
    filepath = AUDIO_DIR / filename
    
    try:
        tts = gTTS(text=text, lang=lang, slow=slow)
        tts.save(str(filepath))
        return str(filepath)
    except Exception as e:
        print(f"Error generating speech: {e}")
        return None


async def generate_speech_async(text: str, lang: str = "en", slow: bool = False) -> str:
    """Асинхронная версия генерации речи."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, generate_speech, text, lang, slow)


def generate_word_audio(word: str, lang: str = "en") -> str:
    """Генерирует аудио для одного слова."""
    return generate_speech(word, lang=lang, slow=False)


def generate_slow_audio(word: str, lang: str = "en") -> str:
    """Генерирует замедленное аудио для слова."""
    return generate_speech(word, lang=lang, slow=True)


def generate_example_audio(example: str, lang: str = "en") -> str:
    """Генерирует аудио для примера предложения."""
    return generate_speech(example, lang=lang, slow=False)


def cleanup_old_files(max_age_hours: int = 24):
    """Удаляет старые аудиофайлы из кэша."""
    import time
    current_time = time.time()
    
    for filepath in AUDIO_DIR.glob("*.mp3"):
        file_age = current_time - filepath.stat().st_mtime
        if file_age > max_age_hours * 3600:
            try:
                filepath.unlink()
            except Exception as e:
                print(f"Error deleting {filepath}: {e}")


def cleanup_file(filepath: str):
    """Удаляет конкретный аудиофайл."""
    try:
        if filepath and os.path.exists(filepath):
            os.remove(filepath)
    except Exception as e:
        print(f"Error cleaning up {filepath}: {e}")
