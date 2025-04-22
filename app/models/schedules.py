from typing import Optional
import re
from pydantic import BaseModel, field_validator


class ScheduleModel(BaseModel):
    user_id: int 
    medicine: str  
    frequency: int  
    duration_days: Optional[int] = None

    model_config = {
        "from_attributes": True
    }

    @field_validator("frequency")
    @classmethod
    def check_frequency(cls, value):
        if value <= 0 or value > 56: # если частота больше чем 56 раз в сутки, то расписание начинает генерироваться некорректно из-за округления
            raise ValueError("некорректный frequency")
        return value

    @field_validator("duration_days")
    @classmethod
    def check_duration_days(cls, value):
        if value == 0:
            raise ValueError("duration_days не может быть 0 (для пожизненного приема укажите null)")
        return value
    
    @field_validator("medicine")
    @classmethod
    def check_medicine(cls, value):
        if not value.strip():
            raise ValueError("medicine не может быть пустым")

        if not re.match("^[A-Za-zА-Яа-я0-9\\s]+$", value):
            raise ValueError("medicine не может содержать спецсимволы")

        return value


class ScheduleIdModel(BaseModel):
    schedule_id: int

    model_config = {
        "from_attributes": True
    }
