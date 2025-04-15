from typing import Optional, AsyncGenerator
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, relationship
from sqlalchemy import String, DateTime, Integer, ForeignKey

engine = create_async_engine("sqlite+aiosqlite:///medicineSchedule.db")
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


class Model(DeclarativeBase):
    pass

class User(Model):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    schedules: Mapped[list["Schedule"]] = relationship("Schedule", back_populates="user")



class Schedule(Model):
    __tablename__ = "schedules"

    schedule_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False, index=True)
    medicine: Mapped[str] = mapped_column(String, nullable=False)
    frequency: Mapped[int] = mapped_column(Integer, nullable=False)  # кол-во приёмов в день
    duration_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=None)  # если 0  значит прием пожизненый
    start_of_reception: Mapped[datetime] = mapped_column(DateTime, nullable=False) # начало приема - 8 утра следующего дня (после добавления в БД)

    user: Mapped["User"] = relationship("User", back_populates="schedules")



async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
