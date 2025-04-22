from app.repository.schedule_repository import ScheduleRepository
from app.repository.user_repository import UserRepository
from app.services.schedule_service import ScheduleService
from app.services.user_service import UserService
from sqlalchemy.ext.asyncio import AsyncSession


def make_schedule_service_for_grpc(db: AsyncSession) -> ScheduleService:
    schedule_repo = ScheduleRepository(db)
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    return ScheduleService(schedule_repo, user_service)