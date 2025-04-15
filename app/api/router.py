from fastapi import APIRouter, Depends, Query

from app.services.schedule_service import ScheduleService 
from app.schemas.schemas import ScheduleModel, ScheduleIdModel
from dependencies import make_schedule_service

router = APIRouter()


@router.post("/schedule")
async def add_schedule(data: ScheduleModel, schedule_service: ScheduleService = Depends(make_schedule_service)):
    schedule_id = await schedule_service.add_schedule(data)
    return ScheduleIdModel(schedule_id=schedule_id)

@router.get("/schedules") 
async def get_schedules(user_id: int = Query(..., gt=0), schedule_service: ScheduleService = Depends(make_schedule_service)):
    return await schedule_service.get_schedules_ids(user_id)

@router.get("/schedule")
async def get_schedule_for_user_by_id(schedule_id: int = Query(..., gt=0), user_id: int = Query(..., gt=0),schedule_service: ScheduleService = Depends(make_schedule_service)):
    return await schedule_service.get_schedule_for_day(user_id, schedule_id)

@router.get("/next_takings")
async def get_schedule_for_period(user_id: int = Query(..., gt=0), schedule_service: ScheduleService = Depends(make_schedule_service)):
    return await schedule_service.get_schedules_in_period(user_id)





    

