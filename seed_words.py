"""
Скрипт для добавления начальных слов в базу данных.
Запуск: python seed_words.py
"""

import asyncio
from sqlalchemy import select
from app.database.base import async_session
from app.database.models.word import Word


# Начальные слова для бота
INITIAL_WORDS = [
    # Приветствия
    {"word": "hello", "translation": "привет", "part_of_speech": "interjection", "frequency_rank": 10, "level": "A0", "pronunciation": "/həˈloʊ/", "examples": [{"en": "Hello, how are you?", "ru": "Привет, как дела?"}], "category": "greetings"},
    {"word": "hi", "translation": "привет", "part_of_speech": "interjection", "frequency_rank": 15, "level": "A0", "pronunciation": "/haɪ/", "examples": [{"en": "Hi there!", "ru": "Привет!"}], "category": "greetings"},
    {"word": "goodbye", "translation": "до свидания", "part_of_speech": "interjection", "frequency_rank": 20, "level": "A0", "pronunciation": "/ɡʊdˈbaɪ/", "examples": [{"en": "Goodbye, see you tomorrow!", "ru": "До свидания, увидимся завтра!"}], "category": "greetings"},
    {"word": "bye", "translation": "пока", "part_of_speech": "interjection", "frequency_rank": 25, "level": "A0", "pronunciation": "/baɪ/", "examples": [{"en": "Bye! Have a nice day!", "ru": "Пока! Хорошего дня!"}], "category": "greetings"},
    
    # Базовые слова
    {"word": "yes", "translation": "да", "part_of_speech": "adverb", "frequency_rank": 30, "level": "A0", "pronunciation": "/jes/", "examples": [{"en": "Yes, I agree.", "ru": "Да, я согласен."}], "category": "basics"},
    {"word": "no", "translation": "нет", "part_of_speech": "adverb", "frequency_rank": 35, "level": "A0", "pronunciation": "/noʊ/", "examples": [{"en": "No, thank you.", "ru": "Нет, спасибо."}], "category": "basics"},
    {"word": "please", "translation": "пожалуйста", "part_of_speech": "adverb", "frequency_rank": 40, "level": "A0", "pronunciation": "/pliːz/", "examples": [{"en": "Please help me.", "ru": "Пожалуйста, помоги мне."}], "category": "basics"},
    {"word": "thank", "translation": "благодарить", "part_of_speech": "verb", "frequency_rank": 45, "level": "A0", "pronunciation": "/θæŋk/", "examples": [{"en": "Thank you very much!", "ru": "Большое спасибо!"}], "category": "basics"},
    
    # Местоимения
    {"word": "i", "translation": "я", "part_of_speech": "pronoun", "frequency_rank": 50, "level": "A0", "pronunciation": "/aɪ/", "examples": [{"en": "I am happy.", "ru": "Я счастлив."}], "category": "pronouns"},
    {"word": "you", "translation": "ты/вы", "part_of_speech": "pronoun", "frequency_rank": 55, "level": "A0", "pronunciation": "/juː/", "examples": [{"en": "You are my friend.", "ru": "Ты мой друг."}], "category": "pronouns"},
    {"word": "he", "translation": "он", "part_of_speech": "pronoun", "frequency_rank": 60, "level": "A0", "pronunciation": "/hiː/", "examples": [{"en": "He is tall.", "ru": "Он высокий."}], "category": "pronouns"},
    {"word": "she", "translation": "она", "part_of_speech": "pronoun", "frequency_rank": 65, "level": "A0", "pronunciation": "/ʃiː/", "examples": [{"en": "She is smart.", "ru": "Она умная."}], "category": "pronouns"},
    
    # Глаголы
    {"word": "be", "translation": "быть", "part_of_speech": "verb", "frequency_rank": 70, "level": "A0", "pronunciation": "/biː/", "examples": [{"en": "I want to be happy.", "ru": "Я хочу быть счастливым."}], "category": "verbs"},
    {"word": "have", "translation": "иметь", "part_of_speech": "verb", "frequency_rank": 75, "level": "A0", "pronunciation": "/hæv/", "examples": [{"en": "I have a cat.", "ru": "У меня есть кошка."}], "category": "verbs"},
    {"word": "do", "translation": "делать", "part_of_speech": "verb", "frequency_rank": 80, "level": "A0", "pronunciation": "/duː/", "examples": [{"en": "What do you do?", "ru": "Что ты делаешь?"}], "category": "verbs"},
    {"word": "go", "translation": "идти", "part_of_speech": "verb", "frequency_rank": 85, "level": "A0", "pronunciation": "/ɡoʊ/", "examples": [{"en": "I go to work.", "ru": "Я иду на работу."}], "category": "verbs"},
    {"word": "come", "translation": "приходить", "part_of_speech": "verb", "frequency_rank": 90, "level": "A0", "pronunciation": "/kʌm/", "examples": [{"en": "Come here, please.", "ru": "Подойди сюда, пожалуйста."}], "category": "verbs"},
    
    # Прилагательные
    {"word": "good", "translation": "хороший", "part_of_speech": "adjective", "frequency_rank": 95, "level": "A0", "pronunciation": "/ɡʊd/", "examples": [{"en": "This is good.", "ru": "Это хорошо."}], "category": "adjectives"},
    {"word": "bad", "translation": "плохой", "part_of_speech": "adjective", "frequency_rank": 100, "level": "A0", "pronunciation": "/bæd/", "examples": [{"en": "This is bad.", "ru": "Это плохо."}], "category": "adjectives"},
    {"word": "big", "translation": "большой", "part_of_speech": "adjective", "frequency_rank": 105, "level": "A0", "pronunciation": "/bɪɡ/", "examples": [{"en": "The house is big.", "ru": "Дом большой."}], "category": "adjectives"},
    {"word": "small", "translation": "маленький", "part_of_speech": "adjective", "frequency_rank": 110, "level": "A0", "pronunciation": "/smɔːl/", "examples": [{"en": "The cat is small.", "ru": "Кошка маленькая."}], "category": "adjectives"},
    
    # Еда
    {"word": "water", "translation": "вода", "part_of_speech": "noun", "frequency_rank": 115, "level": "A1", "pronunciation": "/ˈwɔːtər/", "examples": [{"en": "Can I have water?", "ru": "Можно воды?"}], "category": "food"},
    {"word": "food", "translation": "еда", "part_of_speech": "noun", "frequency_rank": 120, "level": "A1", "pronunciation": "/fuːd/", "examples": [{"en": "The food is delicious.", "ru": "Еда вкусная."}], "category": "food"},
    {"word": "coffee", "translation": "кофе", "part_of_speech": "noun", "frequency_rank": 125, "level": "A1", "pronunciation": "/ˈkɔːfi/", "examples": [{"en": "I like coffee.", "ru": "Я люблю кофе."}], "category": "food"},
    {"word": "tea", "translation": "чай", "part_of_speech": "noun", "frequency_rank": 130, "level": "A1", "pronunciation": "/tiː/", "examples": [{"en": "Would you like tea?", "ru": "Хочешь чай?"}], "category": "food"},
    
    # Время
    {"word": "today", "translation": "сегодня", "part_of_speech": "adverb", "frequency_rank": 135, "level": "A1", "pronunciation": "/təˈdeɪ/", "examples": [{"en": "Today is Monday.", "ru": "Сегодня понедельник."}], "category": "time"},
    {"word": "tomorrow", "translation": "завтра", "part_of_speech": "adverb", "frequency_rank": 140, "level": "A1", "pronunciation": "/təˈmɑːroʊ/", "examples": [{"en": "See you tomorrow.", "ru": "Увидимся завтра."}], "category": "time"},
    {"word": "yesterday", "translation": "вчера", "part_of_speech": "adverb", "frequency_rank": 145, "level": "A1", "pronunciation": "/ˈjestərdeɪ/", "examples": [{"en": "I was busy yesterday.", "ru": "Я был занят вчера."}], "category": "time"},
    
    # Места
    {"word": "home", "translation": "дом", "part_of_speech": "noun", "frequency_rank": 150, "level": "A1", "pronunciation": "/hoʊm/", "examples": [{"en": "I want to go home.", "ru": "Я хочу пойти домой."}], "category": "places"},
    {"word": "work", "translation": "работа", "part_of_speech": "noun", "frequency_rank": 155, "level": "A1", "pronunciation": "/wɜːrk/", "examples": [{"en": "I go to work.", "ru": "Я иду на работу."}], "category": "places"},
    {"word": "school", "translation": "школа", "part_of_speech": "noun", "frequency_rank": 160, "level": "A1", "pronunciation": "/skuːl/", "examples": [{"en": "Children go to school.", "ru": "Дети ходят в школу."}], "category": "places"},
    
    # Люди
    {"word": "friend", "translation": "друг", "part_of_speech": "noun", "frequency_rank": 165, "level": "A1", "pronunciation": "/frend/", "examples": [{"en": "He is my friend.", "ru": "Он мой друг."}], "category": "people"},
    {"word": "family", "translation": "семья", "part_of_speech": "noun", "frequency_rank": 170, "level": "A1", "pronunciation": "/ˈfæmɪli/", "examples": [{"en": "I love my family.", "ru": "Я люблю свою семью."}], "category": "people"},
    {"word": "mother", "translation": "мама", "part_of_speech": "noun", "frequency_rank": 175, "level": "A1", "pronunciation": "/ˈmʌðər/", "examples": [{"en": "My mother is kind.", "ru": "Моя мама добрая."}], "category": "people"},
    {"word": "father", "translation": "папа", "part_of_speech": "noun", "frequency_rank": 180, "level": "A1", "pronunciation": "/ˈfɑːðər/", "examples": [{"en": "My father is tall.", "ru": "Мой папа высокий."}], "category": "people"},
]


async def seed_database():
    """Добавляет начальные слова в базу данных."""
    print("📚 Добавление слов в базу данных...")
    
    async with async_session() as session:
        added = 0
        skipped = 0
        
        for word_data in INITIAL_WORDS:
            # Проверяем есть ли уже такое слово
            existing = await session.execute(
                select(Word).where(Word.word == word_data["word"])
            )
            
            if existing.scalar_one_or_none():
                skipped += 1
                continue
            
            # Создаём новое слово
            word = Word(
                word=word_data["word"],
                translation=word_data["translation"],
                part_of_speech=word_data.get("part_of_speech"),
                frequency_rank=word_data.get("frequency_rank", 1000),
                level=word_data.get("level", "A1"),
                pronunciation=word_data.get("pronunciation"),
                examples=word_data.get("examples", []),
                category=word_data.get("category"),
            )
            
            session.add(word)
            added += 1
        
        await session.commit()
        
        print(f"✅ Добавлено слов: {added}")
        print(f"⏭️ Пропущено (уже есть): {skipped}")
        print(f"🎉 Всего слов в базе: {added + skipped}")
        print("\n🚀 Теперь можешь запускать бота: python -m app.main")


if __name__ == "__main__":
    asyncio.run(seed_database())
