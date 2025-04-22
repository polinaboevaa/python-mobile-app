from typing import List, Dict

from pydantic import BaseModel, RootModel


class SchedulesListResponse(BaseModel):
    active_schedule_ids: List[int]

class FullScheduleResponse(BaseModel):
    schedule_id: int
    medicine: str
    time_list: List[str]

class DynamicSchedulesResponse(RootModel[Dict[str, List[str]]]):
    pass

class ErrorResponse(BaseModel):
    detail: str

class MessageResponse(BaseModel):
    message: str