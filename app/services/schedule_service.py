from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List

from config import PERIOD, START_TIME, INTERVAL_HOURS
from app.repository.repository import Repository
from app.services.helper_service import HelperService

class ScheduleService:
    """Класс для работы с расписанием приёма лекарств."""

    async def get_schedule_for_day(db: AsyncSession, user_id: int, schedule_id: int) -> Dict[str, Any]:
        """
        Возвращает время приема таблеток на день для конкретного пользователя и препарата.
        """ 
        row = await Repository.get_schedule_data_by_schedule_id(db, user_id, schedule_id)

        if not row:
            return {"message": "Нет расписаний для пользователя"}
        
        frequency, duration_days, start_of_reception, medicine = row  

        if HelperService.is_schedule_active(start_of_reception, duration_days) == False:
            return {"message": "Расписание неактуально"}

        interval = timedelta(hours=INTERVAL_HOURS) / frequency  
        time_list = [HelperService.round_minutes(datetime.combine(datetime.today(), START_TIME) + interval * i) for i in range(frequency)]

        return {
            "schedule_id": schedule_id, 
            "medicine": medicine,
            "time_list": time_list
        }

    async def get_schedules_in_period(db: AsyncSession, user_id: int) -> Dict[str, List[str]]:
        """
        Возвращает расписание приёмов лекарств для пользователя на указанный период.
        """
        from_date = datetime.now()  
        to_date = from_date + PERIOD  

        rows = await Repository.get_schedules_by_user_id(db, user_id)
        
        if not rows:
            return {"message": "Нет расписаний для пользователя"}

        schedule_list = {}

        for row in rows:
            medicine, frequency, duration_days, start_of_reception = row

            if HelperService.is_schedule_active(start_of_reception, duration_days) == False:
                continue
            
            if duration_days is None or duration_days == 0:
                end_date = to_date 
            else:
                end_date = start_of_reception + timedelta(days=duration_days)  

            interval = timedelta(hours=INTERVAL_HOURS) / frequency
            daily_times = [HelperService.round_minutes(start_of_reception + interval * i) for i in range(frequency)]

            medicine_schedule = []
            current_date = max(start_of_reception, from_date)  

            while current_date <= end_date and current_date <= to_date:  
                for t in daily_times:
                    time_obj = datetime.strptime(t, "%H:%M").time()  
                    intake_time = datetime.combine(current_date.date(), time_obj)  
                    
                    if from_date <= intake_time <= to_date:
                        medicine_schedule.append(f"{intake_time.strftime('%H:%M %d.%m')}")

                current_date += timedelta(days=1)

            if medicine_schedule:
                schedule_list[medicine] = medicine_schedule

        return schedule_list



    async def get_schedules_ids(user_id: int, db: AsyncSession) -> Dict[str, List[int]]:
        """
        Возвращает ID актуальных расписаний пользователя.
        """
        rows = await Repository.get_schedules_data_by_user_id(db, user_id)

        if not rows:
            return {"message": "Нет расписаний для пользователя"}
        
        schedule_ids = []
        for schedule_id, duration_days, start_of_reception in rows:
            if HelperService.is_schedule_active(start_of_reception, duration_days):
                schedule_ids.append(schedule_id)

        return {"active_schedule_ids": schedule_ids}

    
            



