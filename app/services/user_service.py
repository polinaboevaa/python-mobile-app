from fastapi import HTTPException

from app.repository.user_repository import UserRepository

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def check_user_existence(self, user_id: int):
        user = await self.user_repo.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return user
    
    async def get_or_create_user(self, user_id: int):
        user = await self.user_repo.get_user(user_id)
        if not user:
            user = await self.user_repo.create_user(user_id)
        return user