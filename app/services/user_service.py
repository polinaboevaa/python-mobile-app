from fastapi import HTTPException

from app.core.logger import get_logger
from app.repository.user_repository import UserRepository

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def check_user_existence(self, user_id: int):
        try:
            user = await self.user_repo.get_user(user_id)
            if not user:
                get_logger().bind(user_id=user_id).error("User does not exist")
                raise HTTPException(status_code=404, detail="Пользователь не найден")
            return user
        except Exception as e:
            get_logger().bind(user_id=user_id).error(f"An error occurred when checking user existence: {str(e)}")
            raise

    async def get_or_create_user(self, user_id: int):
        try:
            user = await self.user_repo.get_user(user_id)
        except Exception as e:
            get_logger().bind(user_id=user_id).error(f"Error while getting user: {str(e)}")
            raise

        if not user:
            try:
                user = await self.user_repo.create_user(user_id)
                get_logger().bind(user_id=user_id).debug("New user has been created")
            except Exception as e:
                get_logger().bind(user_id=user_id).error(f"Error while creating user: {str(e)}")
                raise

        return user
