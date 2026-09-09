# 🇬🇧 English Learning Telegram Bot

Полностью автономный Telegram-бот для изучения английского языка с **бесплатными** AI, TTS и STT.

## 🎯 Возможности

- ✅ **AI-собеседник** (Groq Llama 3.3 — бесплатно)
- ✅ **Голосовое озвучивание** (edge-tts — бесплатно)
- ✅ **Распознавание речи** (Whisper — бесплатно)
- ✅ **Интервальное повторение** (SM-2 алгоритм)
- ✅ **4 навыка**: Recognition, Recall, Listening, Production
- ✅ **Адаптивное обучение** под уровень пользователя
- ✅ **Статистика** и отслеживание прогресса

## 🆓 Полностью бесплатные решения

| Компонент | Решение | Стоимость | Лимиты |
|-----------|---------|-----------|--------|
| **AI** | Groq (Llama 3.3) | $0 | 14400 запросов/день |
| **TTS** | edge-tts (Microsoft Edge) | $0 | Безлимитно |
| **STT** | Whisper (OpenAI) | $0 | Локально, безлимитно |
| **Database** | PostgreSQL | $0 | Локально |

**Итого: $0/месяц** 🎉

## 🚀 Быстрый старт

### 1. Клонировать проект

```bash
git clone <your-repo-url>
cd english-learning-bot
```

### 2. Создать виртуальное окружение

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Получить Groq API ключ (БЕСПЛАТНО)

1. Зайди на https://console.groq.com/
2. Зарегистрируйся (можно через Google)
3. Перейди в "API Keys"
4. Нажми "Create API Key"
5. Скопируй ключ (начинается с `gsk_...`)

### 5. Создать Telegram бота

1. Открой Telegram → найди @BotFather
2. Отправь `/newbot`
3. Придумай имя и username
4. Скопируй **BOT_TOKEN**

### 6. Настроить .env

```bash
cp .env.example .env
```

Отредактируй `.env`:

```env
# Обязательно
BOT_TOKEN=твой_токен_от_BotFather
GROQ_API_KEY=gsk_твой_groq_ключ

# Остальное можно оставить по умолчанию
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/english_bot
LLM_PROVIDER=groq
TTS_PROVIDER=edge
STT_PROVIDER=whisper
```

### 7. Запустить PostgreSQL

**Вариант A: Docker (проще)**

```bash
docker-compose up -d db
```

**Вариант B: Локально**

```bash
# Установить PostgreSQL
# Создать базу данных:
createdb english_bot
```

### 8. Инициализировать базу данных

```bash
# Создать таблицы
python -c "import asyncio; from app.database.base import init_db; asyncio.run(init_db())"
```

### 9. Сгенерировать словарь (опционально)

```bash
# Сгенерировать 500 слов уровня A1
python -m scripts.generate_dictionary --level A1 --count 500 --output data/words_a1.json

# Импортировать в базу
python -m scripts.import_words data/words_a1.json
```

### 10. Запустить бота

```bash
python -m app.main
```

### 11. Проверить работу

Открой бота в Telegram → `/start`

## 📱 Команды бота

| Команда | Описание |
|---------|----------|
| `/start` | Начальное меню |
| `/learn` | Учить новые слова |
| `/review` | Повторить изученное |
| `/dialogue` | Поговорить с AI |
| `/progress` | Статистика |
| `/help` | Справка |

## 🏗️ Архитектура

```
app/
├── main.py                    # Точка входа
├── config.py                  # Конфигурация
├── database/                  # SQLAlchemy модели
│   ├── base.py
│   └── models/
│       ├── user.py           # Пользователи
│       ├── word.py           # Словарь
│       ├── user_word.py      # Прогресс
│       └── review.py         # История
├── repositories/              # Работа с БД
├── services/                  # Бизнес-логика
│   ├── learning_service.py   # Обучение
│   └── spaced_repetition.py  # SM-2 алгоритм
├── ai/                        # AI провайдеры
│   └── providers.py          # Groq, Gemini
├── speech/                    # Speech провайдеры
│   └── providers.py          # edge-tts, Whisper
└── telegram/                  # Telegram handlers
    ├── bot.py
    ├── handlers/
    │   ├── start.py          # /start, /help
    │   ├── learn.py          # Учить слова
    │   ├── review.py         # Повторение
    │   ├── dialogue.py       # AI-собеседник
    │   └── progress.py       # Статистика
    └── keyboards/
        └── main.py           # Inline кнопки
```

## 🧠 Алгоритм обучения

### Интервальное повторение (SM-2)

- ✅ Правильный ответ → интервал увеличивается
- ❌ Ошибка → интервал сбрасывается
- ⏱️ Время ответа влияет на качество

### 4 навыка для каждого слова

1. **Recognition** — English → Russian (выбор)
2. **Recall** — Russian → English (ввод)
3. **Listening** — Audio → meaning
4. **Production** — свободное построение предложений

## 🎤 Speech (TTS/STT)

### TTS: edge-tts (Microsoft Edge)

```python
from app.speech import EdgeTTSProvider

tts = EdgeTTSProvider(voice="en-US-JennyNeural")
audio = await tts.synthesize("Hello, how are you?")
```

**Доступные голоса:**
- `en-US-JennyNeural` — женский, американский
- `en-US-GuyNeural` — мужской, американский
- `en-GB-SoniaNeural` — женский, британский

### STT: Whisper (OpenAI)

```python
from app.speech import WhisperProvider

stt = WhisperProvider(model_name="base")
text = await stt.transcribe(audio_bytes, lang="en")
```

**Модели:**
- `tiny` — 39 MB, быстрый
- `base` — 74 MB, баланс (рекомендуется)
- `small` — 244 MB, точный

## 🤖 AI-собеседник

### Groq (Llama 3.3)

```python
from app.ai import GroqProvider

llm = GroqProvider(api_key="gsk_...")
response = await llm.converse(
    messages=[{"role": "user", "content": "Hi!"}],
    user_level="A2",
)
```

**Лимиты:**
- 30 запросов/мин
- 14400 запросов/день
- 100,000 токенов/мин

## 📊 Структура слова

```json
{
  "word": "run",
  "translation": "бежать; работать; управлять",
  "part_of_speech": "verb",
  "frequency_rank": 150,
  "level": "A2",
  "pronunciation": "/rʌn/",
  "examples": [
    {"en": "I run every morning.", "ru": "Я бегаю каждое утро."}
  ],
  "common_phrases": ["run out of", "run late"],
  "collocations": ["run a business"],
  "synonyms": ["sprint", "jog"],
  "forms": ["run", "ran", "running"],
  "tags": ["daily", "movement"],
  "importance": 9.4
}
```

## 🐳 Docker

```bash
# Запустить всё (бот + БД)
docker-compose up -d

# Логи
docker-compose logs -f bot

# Остановить
docker-compose down
```

## 📈 Масштабирование

Для production:
- Добавить Redis для кэширования
- Использовать webhook вместо polling
- Настроить мониторинг (Sentry)
- Добавить rate limiting

## 🔧 Разработка

```bash
# Запустить тесты
pytest

# Проверить типы
mypy app/

# Форматирование
black app/
```

## 📝 Лицензия

MIT

## 💡 Принцип

> **НЕ УЧИТЬ АНГЛИЙСКИЙ КАК ШКОЛЬНЫЙ ПРЕДМЕТ. ФОРМИРОВАТЬ АВТОМАТИЧЕСКИЙ НАВЫК ПОНИМАНИЯ И РЕЧИ.**

## 🆘 Поддержка

- Groq API: https://console.groq.com/
- edge-tts: https://github.com/rany2/edge-tts
- Whisper: https://github.com/openai/whisper
- aiogram: https://docs.aiogram.dev/

---

**Всё полностью бесплатно!** 🎉
