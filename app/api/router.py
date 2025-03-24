from fastapi import APIRouter, Depends, Query

from app.services.schedule_service import ScheduleService
from app.database.database import get_async_db, AsyncSession  
from app.schemas.schemas import ScheduleModel, ScheduleIdModel

router = APIRouter()

@router.post("/schedule")
async def add_schedule(data: ScheduleModel, db: AsyncSession = Depends(get_async_db)):
    """Добавляет новое расписание и возвращает его ID"""
    schedule_id = await ScheduleService.add_schedule(data, db)
    return ScheduleIdModel(schedule_id=schedule_id)

@router.get("/schedules") 
async def get_schedules(user_id: int = Query(..., gt=0), db: AsyncSession = Depends(get_async_db)):
    """Возвращает список ID расписаний выбранного пользователя"""
    schedules = await ScheduleService.get_schedules_ids(user_id, db)
    return schedules

@router.get("/schedule")
async def get_schedule_for_user_by_id(schedule_id: int = Query(..., gt=0), user_id: int = Query(..., gt=0), db: AsyncSession = Depends(get_async_db)):
    
    """Возвращает данные о выбранном расписании с рассчитанным графиком приёмов на день"""
    schedules = await ScheduleService.get_schedule_for_day(db, user_id, schedule_id)
    return schedules

@router.get("/next_takings")
async def get_schedule_for_period(user_id: int = Query(..., gt=0), db: AsyncSession = Depends(get_async_db)):
    """Возвращает данные о таблетках, которые необходимо принять в ближайшие период (например, в ближайший час). Период времени задается через параметры конфигурации сервиса"""
    schedules = await ScheduleService.get_schedules_in_period(db, user_id)
    return schedules




    

