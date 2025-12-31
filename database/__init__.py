"""
Database package для hongkong_surprise_bot.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from pathlib import Path

# Путь к базе данных
DB_PATH = Path(__file__).parent.parent / "quest_bot.db"
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

# Создаем движок
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
)

# Создаем фабрику сессий
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db():
    """Инициализация базы данных."""
    from database.models import Base

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    """Получить сессию базы данных."""
    async with AsyncSessionLocal() as session:
        yield session
