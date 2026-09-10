"""
Скрипт для пересоздания базы данных.
Удаляет все старые таблицы и создаёт новые.

Запуск:
    python reset_db.py
"""

import asyncio
from sqlalchemy import text
from app.database.base import engine, Base


async def reset_database():
    """Удаляет все таблицы и создаёт заново."""
    print("🔄 Пересоздание базы данных...")
    
    async with engine.begin() as conn:
        # Удаляем все таблицы
        await conn.run_sync(Base.metadata.drop_all)
        print("✅ Старые таблицы удалены")
        
        # Создаём новые таблицы
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Новые таблицы созданы")
    
    await engine.dispose()
    print("🎉 Готово! Можешь запускать бота: python -m app.main")


if __name__ == "__main__":
    asyncio.run(reset_database())
