from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import User

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_user(self, user_id: int):
        query = select(User).where(User.user_id == user_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def create_user(self, user_id: int):
        user = User(user_id=user_id)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
