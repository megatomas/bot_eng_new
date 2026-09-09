# ⚡ Быстрый старт (5 минут)

## Что нужно:
- ✅ Python 3.10+
- ✅ PostgreSQL (или Docker)
- ✅ Telegram аккаунт
- ✅ 5 минут времени

## 1. Установи зависимости

```bash
pip install -r requirements.txt
```

## 2. Получи 2 ключа (бесплатно)

### Telegram Bot Token:
1. Открой @BotFather в Telegram
2. Отправь `/newbot`
3. Скопируй токен

### Groq API Key:
1. Зайди на https://console.groq.com/
2. Войди через Google
3. Создай API Key (начинается с `gsk_...`)

## 3. Настрой .env

```bash
cp .env.example .env
```

Отредактируй `.env`:
```env
BOT_TOKEN=твой_токен_от_BotFather
GROQ_API_KEY=gsk_твой_groq_ключ
```

## 4. Запусти PostgreSQL

```bash
docker-compose up -d db
```

Или используй локальный PostgreSQL.

## 5. Инициализируй базу

```bash
python -c "import asyncio; from app.database.base import init_db; asyncio.run(init_db())"
```

## 6. Запусти бота

```bash
python -m app.main
```

## 7. Готово! 🎉

Открой бота в Telegram → `/start`

---

## 🆘 Проблема?

Смотри подробную инструкцию: [INSTALL_WINDOWS.md](INSTALL_WINDOWS.md)

---

**Всё бесплатно! Наслаждайся!** 🚀
