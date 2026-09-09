# 📖 Подробная инструкция по установке (Windows)

## Шаг 1: Установка Python 3.10+

1. Скачай Python с https://www.python.org/downloads/
2. При установке **ОБЯЗАТЕЛЬНО** поставь галку "Add Python to PATH"
3. Проверь установку:
   ```cmd
   python --version
   ```

## Шаг 2: Установка PostgreSQL

### Вариант A: Через Docker (проще)

1. Установи Docker Desktop: https://www.docker.com/products/docker-desktop/
2. Запусти Docker Desktop
3. В терминале проекта:
   ```cmd
   docker-compose up -d db
   ```

### Вариант B: Локально

1. Скачай PostgreSQL: https://www.postgresql.org/download/windows/
2. При установке:
   - Порт: 5432
   - Пароль: postgres (или свой)
   - Запомни пароль!
3. Создай базу данных через pgAdmin или командную строку:
   ```sql
   CREATE DATABASE english_bot;
   ```

## Шаг 3: Создание Telegram бота

1. Открой Telegram
2. Найди @BotFather
3. Отправь `/newbot`
4. Введи имя бота (например: "English Learning Bot")
5. Введи username (например: `my_english_learning_bot`)
6. **Скопируй токен** (выглядит так: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

## Шаг 4: Получение Groq API ключа (БЕСПЛАТНО)

1. Зайди на https://console.groq.com/
2. Нажми "Sign in" → войди через Google
3. Перейди в раздел "API Keys" (слева в меню)
4. Нажми "Create API Key"
5. Дай имя (например: "english-bot")
6. **Скопируй ключ** (начинается с `gsk_...`)
   - ⚠️ Ключ показывается только один раз!

## Шаг 5: Настройка проекта

### 5.1. Скачай проект

```cmd
cd D:\PYTHON
git clone <your-repo-url>
cd bot_eng_new
```

### 5.2. Создай виртуальное окружение

```cmd
python -m venv venv
venv\Scripts\activate
```

После активации в начале строки появится `(venv)`

### 5.3. Установи зависимости

```cmd
pip install -r requirements.txt
```

Если будут ошибки с `openai-whisper`, установи отдельно:
```cmd
pip install openai-whisper
```

### 5.4. Установи FFmpeg (для Whisper)

1. Скачай FFmpeg: https://ffmpeg.org/download.html
2. Выбери "Windows" → скачай build
3. Распакуй в `C:\ffmpeg`
4. Добавь в PATH:
   - Правой кнопкой на "Этот компьютер" → Свойства
   - Дополнительные параметры системы → Переменные среды
   - В "Path" добавь: `C:\ffmpeg\bin`
5. Перезапусти терминал
6. Проверь:
   ```cmd
   ffmpeg -version
   ```

### 5.5. Настрой .env файл

```cmd
copy .env.example .env
```

Открой `.env` в блокноте и заполни:

```env
# ОБЯЗАТЕЛЬНО заполни:
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
GROQ_API_KEY=gsk_твой_ключ_здесь

# База данных (если пароль другой, измени):
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/english_bot

# Остальное можно не трогать:
LLM_PROVIDER=groq
TTS_PROVIDER=edge
STT_PROVIDER=whisper
```

**ВАЖНО:**
- Убери кавычки вокруг значений!
- Не добавляй пробелы вокруг `=`

## Шаг 6: Инициализация базы данных

```cmd
python -c "import asyncio; from app.database.base import init_db; asyncio.run(init_db())"
```

Если всё хорошо, увидишь создание таблиц.

## Шаг 7: Генерация словаря (опционально)

```cmd
# Сгенерировать 100 слов для теста
python -m scripts.generate_dictionary --level A1 --count 100 --output data/words_a1.json

# Импортировать в базу
python -m scripts.import_words data/words_a1.json
```

## Шаг 8: Запуск бота

```cmd
python -m app.main
```

Должен увидеть:
```
INFO: Starting English Learning Bot...
INFO: Initializing database...
INFO: Bot started successfully!
INFO: Bot username: @your_bot_username
```

## Шаг 9: Проверка

1. Открой Telegram
2. Найди своего бота по username
3. Нажми "Start" или отправь `/start`
4. Должно появиться приветствие с кнопками

## 🐛 Решение проблем

### Ошибка: "TELEGRAM_BOT_TOKEN не установлен"

**Причина:** Не загружается .env файл

**Решение:**
```cmd
# Проверь что .env существует
dir .env

# Проверь содержимое
type .env

# Убедись что нет кавычек и пробелов вокруг =
```

### Ошибка: "connection refused" для PostgreSQL

**Причина:** PostgreSQL не запущен или неправильный пароль

**Решение:**
```cmd
# Проверь что PostgreSQL запущен
# Services → PostgreSQL → Running

# Проверь пароль в .env
DATABASE_URL=postgresql+asyncpg://postgres:ТВОЙ_ПАРОЛЬ@localhost:5432/english_bot
```

### Ошибка: "ModuleNotFoundError: No module named 'edge_tts'"

**Причина:** Не установлены зависимости

**Решение:**
```cmd
pip install edge-tts
```

### Ошибка: "FFmpeg not found"

**Причина:** FFmpeg не в PATH

**Решение:**
1. Проверь что FFmpeg установлен
2. Добавь `C:\ffmpeg\bin` в PATH
3. Перезапусти терминал

### Бот не отвечает

**Причина:** Бот не запущен или ошибка в коде

**Решение:**
```cmd
# Проверь что бот запущен
# В терминале должно быть: "Bot started successfully!"

# Перезапусти бота
Ctrl+C
python -m app.main
```

## 📱 Первые команды

После запуска попробуй:

1. `/start` — приветствие
2. Нажми "📚 Учить новые слова"
3. Пройди первое упражнение
4. Нажми "🔁 Повторить"
5. Нажми "💬 Поговорить" (AI-собеседник)
6. Нажми "📊 Мой прогресс"

## 🎯 Что дальше?

1. **Сгенерируй больше слов:**
   ```cmd
   python -m scripts.generate_dictionary --level A2 --count 500
   python -m scripts.import_words data/generated_words.json
   ```

2. **Настрой напоминания** (добавить в будущем)

3. **Добавь больше режимов** (practice, shadowing)

4. **Поделись с друзьями!** 🎉

## 💡 Советы

- Занимайся каждый день хотя бы 10 минут
- Используй режим "Повторение" для закрепления
- Попробуй "AI-собеседник" для практики речи
- Смотри статистику для мотивации

---

**Всё готово! Приятного изучения!** 🇬🇧✨
