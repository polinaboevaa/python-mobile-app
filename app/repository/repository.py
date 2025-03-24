from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Tuple, Optional
from datetime import datetime

from app.database.database import Schedule
from app.schemas.schemas import ScheduleIdModel
from app.services.helper_service import HelperService


class Repository:

    @staticmethod 
    async def add_schedule(db: AsyncSession, data: ScheduleIdModel):
        schedule_dict = data.model_dump()

        start_of_reception =  HelperService.get_start_of_reception()

        schedule = Schedule(**schedule_dict, start_of_reception=start_of_reception)

        async with db.begin():  
            db.add(schedule)
            await db.flush() 
            await db.commit()
    
        return schedule.schedule_id
    
        
    @staticmethod
    async def get_schedules_data_by_user_id(db: AsyncSession, user_id: int) -> list[Tuple[int, Optional[int], datetime]]:
        query = select(Schedule.schedule_id, 
                       Schedule.duration_days, 
                       Schedule.start_of_reception
                       ).where(Schedule.user_id == user_id)
        
        result = await db.execute(query)
        rows = result.fetchall()  
        
        return [tuple(row) for row in rows]  
    
    @staticmethod
    async def get_schedule_data_by_schedule_id(db: AsyncSession, user_id: int, schedule_id: int):

        query = select(Schedule.frequency, 
                        Schedule.duration_days, 
                        Schedule.start_of_reception, 
                        Schedule.medicine
                        ).where (and_(Schedule.user_id == user_id, Schedule.schedule_id == schedule_id))
        
        result = await db.execute(query)
        row = result.first()

        return row
    
    @staticmethod
    async def get_schedules_by_user_id(db: AsyncSession, user_id: int):

        query = select(Schedule.medicine, 
                        Schedule.frequency, 
                        Schedule.duration_days, 
                        Schedule.start_of_reception
                        ).where(Schedule.user_id == user_id)

        result = await db.execute(query)
        rows = result.fetchall()

        return rows
    



