from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.database.models import Schedule
from app.generated import ScheduleModel
from app.services.helper_service import HelperService


class ScheduleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_schedule(self, data: ScheduleModel):
        schedule_dict = data.model_dump()
        start_of_reception = HelperService.get_start_of_reception()
        schedule = Schedule(**schedule_dict, start_of_reception=start_of_reception)

        self.db.add(schedule)
        await self.db.flush()
        await self.db.commit()

        return schedule.schedule_id


    async def get_schedules_data_by_user_id(self, user_id: int) -> list[tuple[tuple[int, int | None, datetime], ...]]:
        query = select(Schedule.schedule_id,
                       Schedule.duration_days,
                       Schedule.start_of_reception
                       ).where(Schedule.user_id == user_id)

        result = await self.db.execute(query)
        rows = result.fetchall()

        return [tuple(row) for row in rows]


    async def get_schedule_data_by_schedule_id(self, user_id: int, schedule_id: int):

        query = select(Schedule.frequency,
                        Schedule.duration_days,
                        Schedule.start_of_reception,
                        Schedule.medicine
                        ).where (and_(Schedule.user_id == user_id, Schedule.schedule_id == schedule_id))

        result = await self.db.execute(query)
        row = result.first()

        return row


    async def get_schedules_by_user_id(self, user_id: int):

        query = select(Schedule.medicine,
                        Schedule.frequency,
                        Schedule.duration_days,
                        Schedule.start_of_reception
                        ).where(Schedule.user_id == user_id)

        result = await self.db.execute(query)
        rows = result.fetchall()

        return rows






