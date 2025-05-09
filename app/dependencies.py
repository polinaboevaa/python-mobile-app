from app.database.session import get_db_session
from app.integrations.schedule_repository import ScheduleRepository
from app.integrations.user_repository import UserRepository
from app.services.schedule_service import ScheduleService
from app.services.user_service import UserService

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

get_async_db = get_db_session

def make_schedule_repository(db: AsyncSession = Depends(get_async_db)) -> ScheduleRepository:
    return ScheduleRepository(db)

def make_user_repository(db: AsyncSession = Depends(get_async_db)) -> UserRepository:
    return UserRepository(db)

def make_user_service(user_repo: UserRepository = Depends(make_user_repository)) -> UserService:
    return UserService(user_repo)

def make_schedule_service(
    schedule_repo: ScheduleRepository = Depends(make_schedule_repository),
    user_service: UserService = Depends(make_user_service)
) -> ScheduleService:
    return ScheduleService(schedule_repo, user_service)

