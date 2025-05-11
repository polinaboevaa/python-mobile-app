from datetime import datetime, timedelta
from typing import Dict, Any

from app.integrations.schedule_repository import ScheduleRepository
from app.services.helper_service import HelperService
from app.services.user_service import UserService
from app.generated import ScheduleModel
from app.core.logger import logger, get_logger
from app.settings import BaseAppSettings


class ScheduleService:
    def __init__(self, schedule_repo: ScheduleRepository, user_service: UserService, helper_service: HelperService, settings: BaseAppSettings):
        self.schedule_repo = schedule_repo
        self.user_service = user_service
        self.helper_service = helper_service
        self.settings = settings

    async def get_schedule_for_day(self, user_id: int, schedule_id: int) -> Dict[str, Any]:
        try:
            await self.user_service.check_user_existence(user_id)
            logger.bind(user_id=user_id, schedule_id=schedule_id).debug("Schedule request for user")

            row = await self.schedule_repo.get_schedule_data_by_schedule_id(user_id, schedule_id)
            if not row:
                logger.bind(user_id=user_id, schedule_id=schedule_id).error("No schedule found")
                return {"message": "Нет расписаний для пользователя"}

            frequency, duration_days, start_of_reception, medicine = row
            if not self.helper_service.is_schedule_active(start_of_reception, duration_days):
                logger.bind(user_id=user_id, schedule_id=schedule_id).warning("The schedule is not relevant")
                return {"message": "Расписание неактуально"}

            if frequency==0:
                return {"message": "Некорректное расписание"}
            interval = timedelta(hours=self.settings.INTERVAL_HOURS) / frequency
            time_list = [self.helper_service.round_minutes(datetime.combine(datetime.today(), self.settings.START_TIME) + interval * i) for i in range(frequency)]
            logger.bind(user_id=user_id, schedule_id=schedule_id).debug("The schedule has been formed")

            return {
                "schedule_id": schedule_id,
                "medicine": medicine,
                "time_list": time_list
            }

        except Exception as e:
            logger.bind(user_id=user_id, schedule_id=schedule_id).error(f"An error occurred when receiving the schedule: {str(e)}")
            raise e

    async def get_schedules_in_period(self, user_id: int) -> dict[str, Any]:
        try:
            from_date = datetime.now()
            to_date = from_date + self.settings.PERIOD

            await self.user_service.check_user_existence(user_id)
            get_logger().bind(user_id=user_id).debug("Request schedules for period")

            rows = await self.schedule_repo.get_schedules_by_user_id(user_id)

            if not rows:
                return {
                    'message': "Нет расписаний для пользователя",
                    'data': {}
                }

            schedule_data = {}
            for row in rows:
                medicine, frequency, duration_days, start_of_reception = row

                if not self.helper_service.is_schedule_active(start_of_reception, duration_days):
                    continue

                if frequency == 0:
                    return {
                        'message': "Некорректное расписание",
                        'data': {}
                    }
                interval = timedelta(hours=self.settings.INTERVAL_HOURS) / frequency
                daily_times = [self.helper_service.round_minutes(start_of_reception + interval * i) for i in range(frequency)]

                medicine_schedule = []
                current_date = max(start_of_reception, from_date)
                end_date = to_date if duration_days is None or duration_days == 0 else start_of_reception + timedelta(days=duration_days)

                while current_date <= end_date and current_date <= to_date:
                    for t in daily_times:
                        time_obj = datetime.strptime(t, "%H:%M").time()
                        intake_time = datetime.combine(current_date.date(), time_obj)
                        if from_date <= intake_time <= to_date:
                            medicine_schedule.append(f"{intake_time.strftime('%H:%M %d.%m')}")
                    current_date += timedelta(days=1)

                if medicine_schedule:
                    schedule_data[medicine] = medicine_schedule

            return {
                'message': "Активные расписания для пользователя" if schedule_data else "Нет активных расписаний",
                'data': schedule_data
            }

        except Exception as e:
            get_logger().bind(user_id=user_id).error(f"Error: {str(e)}")
            return {
                'message': f"Ошибка сервера: {str(e)}",
                'data': {}
            }



    async def get_schedules_ids(self, user_id: int) -> dict[str, str] | dict[str, list[Any]]:
        try:
            await self.user_service.check_user_existence(user_id)
            get_logger().bind(user_id=user_id).debug("Request for a list of schedules ids for user")
            rows = await self.schedule_repo.get_schedules_data_by_user_id(user_id)

            if not rows:
                get_logger().bind(user_id=user_id).error("No schedule found")
                return {"message": "Нет расписаний для пользователя"}

            schedule_ids = []
            for schedule_id, duration_days, start_of_reception in rows:
                if self.helper_service.is_schedule_active(start_of_reception, duration_days):
                    schedule_ids.append(schedule_id)

            get_logger().bind(user_id=user_id).debug("Schedules ids has been received")
            return {"active_schedule_ids": schedule_ids}

        except Exception as e:
            get_logger().bind(user_id=user_id).error(f"An error occurred when receiving the schedule ids: {str(e)}")
            raise e

    async def add_schedule(self, data: ScheduleModel):
        try:
            get_logger().bind(user_id=data.user_id).debug("Adding schedule")
            user = await self.user_service.get_or_create_user(data.user_id)
            schedule_id = await self.schedule_repo.add_schedule(data)
            get_logger().bind(user_id=data.user_id).debug("Schedule has been added")
            return schedule_id
        except Exception as e:
            get_logger().bind(user_id=data.user_id).error(f"An error occurred when adding a schedule: {str(e)}")
            raise e






