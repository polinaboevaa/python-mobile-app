from typing import Optional
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, Integer, ForeignKey

class Model(DeclarativeBase):
    pass

class User(Model):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    schedules: Mapped[list["Schedule"]] = relationship("Schedule", back_populates="user")


class Schedule(Model):
    __tablename__ = "schedules"

    schedule_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    medicine: Mapped[str] = mapped_column(String, nullable=False)
    frequency: Mapped[int] = mapped_column(Integer, nullable=False)  # количество приёмов в день
    duration_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=None)  # если 0 — пожизненный прием
    start_of_reception: Mapped[datetime] = mapped_column(DateTime, nullable=False)  # начало приема

    user: Mapped["User"] = relationship(
        "User",
        back_populates="schedules",
        passive_deletes=True
    )
