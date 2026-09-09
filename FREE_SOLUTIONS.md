# 🆓 Бесплатные решения для бота

## 🤖 1. AI-собеседник (БЕСПЛАТНО)

### Лучший выбор: **Groq** (Llama 3.3)

**Почему Groq:**
- ✅ Полностью бесплатный
- ✅ Llama 3.3 70B (качество как GPT-4)
- ✅ Очень быстрый (500 токенов/сек)
- ✅ 30 запросов/мин, 14400/день
- ✅ Совместим с OpenAI SDK

**Как получить API ключ:**
1. Зайди на https://console.groq.com/
2. Зарегистрируйся (можно через Google)
3. Перейди в "API Keys"
4. Нажми "Create API Key"
5. Скопируй ключ (начинается с `gsk_...`)
6. Добавь в `.env`:
   ```env
   LLM_PROVIDER=groq
   GROQ_API_KEY=gsk_твой_ключ_здесь
   ```

**Лимиты:**
- 30 запросов в минуту
- 14400 запросов в день
- 100,000 токенов в минуту

Этого **более чем достаточно** для личного бота!

---

### Альтернатива: **Google Gemini**

**Почему Gemini:**
- ✅ Бесплатный tier
- ✅ 15 запросов/мин, 1M токенов/день
- ✅ Gemini 1.5 Flash — быстрый и качественный

**Как получить:**
1. Зайди на https://aistudio.google.com/apikey
2. Нажми "Create API Key"
3. Скопируй ключ
4. Добавь в `.env`:
   ```env
   LLM_PROVIDER=gemini
   GEMINI_API_KEY=твой_ключ_здесь
   ```

---

## 🎤 2. Speech (TTS + STT) — БЕСПЛАТНО

### TTS (Text-to-Speech): **edge-tts**

**Почему edge-tts:**
- ✅ Полностью бесплатный
- ✅ Microsoft Edge голоса (очень качественные)
- ✅ Нейросетевые голоса
- ✅ Много вариантов (мужские/женские, американские/британские)
- ✅ Не требует API ключа!

**Установка:**
```bash
pip install edge-tts
```

**Использование:**
```python
from app.speech.providers import EdgeTTSProvider

tts = EdgeTTSProvider(voice="en-US-JennyNeural")
audio_bytes = await tts.synthesize("Hello, how are you?")
```

**Доступные голоса:**
- `en-US-JennyNeural` — женский, американский (рекомендуется)
- `en-US-GuyNeural` — мужской, американский
- `en-GB-SoniaNeural` — женский, британский
- `en-GB-RyanNeural` — мужской, британский
- `ru-RU-SvetlanaNeural` — женский, русский

---

### STT (Speech-to-Text): **Whisper**

**Почему Whisper:**
- ✅ Полностью бесплатный (локальный)
- ✅ OpenAI разработка
- ✅ Очень точный
- ✅ Работает офлайн
- ✅ Поддерживает много языков

**Установка:**
```bash
pip install openai-whisper
```

**Использование:**
```python
from app.speech.providers import WhisperProvider

stt = WhisperProvider(model_name="base")
text = await stt.transcribe(audio_bytes, lang="en")
```

**Модели (выбирай по мощности ПК):**
- `tiny` — 39 MB, быстрый, менее точный
- `base` — 74 MB, хороший баланс (рекомендуется)
- `small` — 244 MB, точный
- `medium` — 769 MB, очень точный
- `large` — 1550 MB, максимальная точность

**Требования:**
- Python 3.8+
- FFmpeg (`apt install ffmpeg` или скачать с ffmpeg.org)
- 2+ GB RAM для base модели

---

### Альтернатива STT: **Vosk**

**Почему Vosk:**
- ✅ Лёгкий (модели ~50 MB)
- ✅ Очень быстрый
- ✅ Полностью офлайн

**Установка:**
```bash
pip install vosk
```

**Минусы:** менее точный чем Whisper

---

## 📚 3. Где взять 5000-10000 слов?

### Вариант 1: **Готовые словари**

**Frequency Dictionaries:**
1. **Oxford 3000/5000** — самые частотные слова
   - https://www.oxfordlearnersdictionaries.com/wordlist/
   - Скачай HTML, распарси в JSON

2. **COCA (Corpus of Contemporary American English)**
   - https://www.wordfrequency.info/
   - Бесплатный список 5000 слов с частотностью

3. **Wiktionary**
   - https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists
   - Огромные списки по частотности

### Вариант 2: **API для получения данных**

**Free Dictionary API:**
```python
import aiohttp

async def get_word_data(word: str) -> dict:
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            # Парси и конвертируй в наш формат
            return data
```

**Datamuse API** (синонимы, коллокации):
```python
async def get_synonyms(word: str) -> list[str]:
    url = f"https://api.datamuse.com/words?rel_syn={word}"
    # ...
```

### Вариант 3: **Создать свой словарь**

Используй скрипт импорта:

```bash
python -m scripts.import_words data/my_words.json
```

**Формат JSON:**
```json
{
  "words": [
    {
      "word": "run",
      "translation": "бежать; работать",
      "part_of_speech": "verb",
      "frequency_rank": 150,
      "level": "A2",
      "pronunciation": "/rʌn/",
      "examples": [
        {"en": "I run every day.", "ru": "Я бегаю каждый день."}
      ],
      "common_phrases": ["run out of", "run late"],
      "collocations": ["run a business"],
      "synonyms": ["sprint", "jog"],
      "forms": ["run", "ran", "running"],
      "tags": ["daily", "movement"],
      "category": "movement",
      "importance": 9.4
    }
  ]
}
```

### Вариант 4: **Сгенерировать с AI**

Используй Groq/Gemini для генерации слов:

```python
async def generate_words_batch(level: str, count: int) -> list[dict]:
    prompt = f"""
    Generate {count} English words for level {level}.
    Return JSON array with:
    - word, translation (Russian), part_of_speech
    - frequency_rank (1-10000)
    - examples (2 sentences with translation)
    - common_phrases (3 phrases)
    - pronunciation (IPA)
    
    Focus on most useful conversational words.
    """
    
    llm = get_llm_provider()
    response = await llm.chat([{"role": "user", "content": prompt}])
    
    # Парси JSON из ответа
    import json
    return json.loads(response)
```

---

## 🎯 Рекомендуемый стек (всё бесплатно!)

```
AI: Groq (Llama 3.3)
TTS: edge-tts (Microsoft Edge)
STT: Whisper (base model)
Database: PostgreSQL (локально или Docker)
```

**Итого:**
- AI: $0 (14400 запросов/день)
- TTS: $0 (безлимитно)
- STT: $0 (локально)
- Database: $0 (локально)

**Всё полностью бесплатно!** 🎉

---

## 🚀 Быстрый старт

1. **Получи Groq API ключ:**
   - https://console.groq.com/
   - Добавь в `.env`: `GROQ_API_KEY=gsk_...`

2. **Установи speech:**
   ```bash
   pip install edge-tts openai-whisper
   ```

3. **Обнови .env:**
   ```env
   LLM_PROVIDER=groq
   GROQ_API_KEY=gsk_твой_ключ
   TTS_PROVIDER=edge
   STT_PROVIDER=whisper
   ```

4. **Запусти бота:**
   ```bash
   python -m app.main
   ```

Всё готово! Бот работает с бесплатными решениями. 🎊
