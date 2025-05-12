from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.settings import get_settings, DatabaseSettings


def get_db_session(settings: DatabaseSettings = Depends(get_settings)):
    engine = create_async_engine(settings.database_url, echo=False, future=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async def get_session():
        async with async_session() as session:
            yield session

    return get_session()
