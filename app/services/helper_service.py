from datetime import datetime, timedelta

class HelperService: 

    @staticmethod
    def is_schedule_active(start_of_reception: datetime, duration_days: int) -> bool:
        """
        Проверяет расписание на актуальность.
        """
        if duration_days is None:
            return True
        
        end_date = start_of_reception + timedelta(days=duration_days)

        today = datetime.now().date()

        if end_date.date() <= today:
            return False
        
        return True

    @staticmethod
    def get_start_of_reception() -> datetime:
        """
        Возвращает дату и время начала приема таблеток.
        """
        now = datetime.now() + timedelta(days=1) 
        return now.replace(hour=8, minute=0, second=0, microsecond=0) 

    @staticmethod
    def round_minutes(dt: datetime) -> datetime:
        """
        Округляет время до ближайшего кратного 15 минут.
        """
        if isinstance(dt, str):  
            dt = datetime.strptime(dt)

        minutes = (dt.minute // 15) * 15  
        remainder = dt.minute % 15  

        if remainder >= 8:  
            minutes += 15

        if minutes == 60:
            dt = dt.replace(hour=dt.hour + 1, minute=0)
        else:
            dt = dt.replace(minute=minutes, second=0, microsecond=0)

        return dt.strftime("%H:%M")  


