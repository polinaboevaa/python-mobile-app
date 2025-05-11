from app.integrations.schedule_repository import ScheduleRepository
from app.integrations.user_repository import UserRepository
from app.services.helper_service import HelperService
from app.services.schedule_service import ScheduleService
from app.services.user_service import UserService
from sqlalchemy.ext.asyncio import AsyncSession

from app.settings import BaseAppSettings


def make_schedule_service_for_grpc(db: AsyncSession, settings: BaseAppSettings) -> ScheduleService:
    schedule_repo = ScheduleRepository(db)
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    helper_service = HelperService()
    return ScheduleService(schedule_repo, user_service, helper_service, settings)
