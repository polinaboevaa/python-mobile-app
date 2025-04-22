from app.proto import schedule_pb2_grpc, schedule_pb2
from app.services.schedule_service import ScheduleService


class ScheduleServiceGRPC(schedule_pb2_grpc.ScheduleServiceServicer):
    def __init__(self, schedule_service: ScheduleService):
        self.service = schedule_service

    async def AddSchedule(self, request: schedule_pb2.ScheduleModel, context) -> schedule_pb2.ScheduleIdModel:
        schedule_id = await self.service.add_schedule(request)
        return schedule_pb2.ScheduleIdModel(schedule_id=schedule_id)

    async def GetSchedules(self, request: schedule_pb2.UserIdRequest, context) -> schedule_pb2.SchedulesListResponse:
        result = await self.service.get_schedules_ids(request.user_id)
        return schedule_pb2.SchedulesListResponse(active_schedule_ids=result)

    async def GetScheduleById(self, request: schedule_pb2.ScheduleQuery, context) -> schedule_pb2.ScheduleResponse:
        schedule = await self.service.get_schedule_for_day(request.user_id, request.schedule_id)
        return schedule_pb2.ScheduleResponse(full_schedule=schedule)

    async def GetNextTakings(self, request: schedule_pb2.UserIdRequest, context) -> schedule_pb2.DynamicSchedulesResponse:
        next_takings = await self.service.get_schedules_in_period(request.user_id)
        return schedule_pb2.DynamicSchedulesResponse(schedule_times=next_takings)

