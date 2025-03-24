from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.repository import Repository

class UserService:
    @staticmethod
    async def check_user_existence(db: AsyncSession, user_id: int):
        user = await Repository.check_user(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return user