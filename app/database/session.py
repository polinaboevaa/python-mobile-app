from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.settings import get_settings, DatabaseSettings

def create_session_factory(settings: DatabaseSettings):
    engine = create_async_engine(settings.database_url, echo=False, future=True)
    return async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db_session(settings: DatabaseSettings = Depends(get_settings)):
    session_factory = create_session_factory(settings)
    async with session_factory() as session:
        yield session
