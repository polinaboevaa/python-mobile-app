from typing import Optional, List
from pydantic import BaseModel, field_validator

class ScheduleModel(BaseModel):
    user_id: int 
    medicine: str  
    frequency: int  
    duration_days: Optional[int] = None

    @field_validator("user_id")
    @classmethod
    def check_user_id(cls, value):
        if value <= 0:
            raise ValueError("user_id должен быть больше или равен 0")
        return value

    @field_validator("frequency")
    @classmethod
    def check_frequency(cls, value):
        if value <= 0 or value > 56: # если частота больше чем 56 раз в сутки то расписание начинает генерироваться некорректно из-за округления
            raise ValueError("некорректный frequency")
        return value

    @field_validator("duration_days")
    @classmethod
    def check_duration_days(cls, value):
        if value == 0:
            raise ValueError("duration_days не может быть 0 (для пожизненного приема укажите null)")
        return value


class ScheduleIdModel(BaseModel):
    schedule_id: int  

    class Config:
        from_attributes = True

