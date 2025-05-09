from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.settings import get_settings
from typing import AsyncGenerator

# Создаем движок один раз при старте приложения
engine = create_async_engine(get_settings().database_url)

# Фабрика сессий
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)

# Генератор сессий для использования во всем приложении
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Генератор сессий, который можно использовать:
    - В FastAPI dependencies
    - В gRPC сервере
    - В любом другом месте приложения
    """
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
