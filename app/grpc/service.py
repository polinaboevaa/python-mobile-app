import pprint

import grpc
from app.generated import ScheduleModel
from app.grpc.generated import schedule_pb2_grpc
from app.grpc.generated import schedule_pb2
from app.services.schedule_service import ScheduleService


class ScheduleServiceGRPC(schedule_pb2_grpc.ScheduleServiceServicer):
    def __init__(self, schedule_service: ScheduleService):
        self.service = schedule_service

    async def AddSchedule(self, request: schedule_pb2.ScheduleModel, context):
        try:
            schedule_data = ScheduleModel(
                user_id=request.user_id,
                medicine=request.medicine,
                frequency=request.frequency,
                duration_days=request.duration_days or None,
            )

            schedule_id = await self.service.add_schedule(schedule_data)
            return schedule_pb2.ScheduleIdModel(schedule_id=schedule_id)

        except Exception as e:
            context.set_details(f"Unexpected error: {str(e)}")
            context.set_code(grpc.StatusCode.UNKNOWN)
            return schedule_pb2.ScheduleIdModel()

    async def GetSchedules(self, request: schedule_pb2.UserIdRequest, context) -> schedule_pb2.SchedulesListResponse:
        result = await self.service.get_schedules_ids(request.user_id)
        return schedule_pb2.SchedulesListResponse(active_schedule_ids=result["active_schedule_ids"])


    async def GetScheduleById(self, request: schedule_pb2.ScheduleQuery, context) -> schedule_pb2.ScheduleResponse:
        schedule = await self.service.get_schedule_for_day(request.user_id, request.schedule_id)

        if "schedule_id" in schedule:
            response = schedule_pb2.ScheduleResponse(
                full_schedule=schedule_pb2.FullScheduleResponse(
                    schedule_id=schedule["schedule_id"],
                    medicine=schedule["medicine"],
                    time_list=schedule["time_list"]
                )
            )
        else:
            response = schedule_pb2.ScheduleResponse(
                message=schedule_pb2.MessageResponse(message=schedule["message"])
            )

        return response

    async def GetNextTakings(self, request: schedule_pb2.UserIdRequest,context) -> schedule_pb2.DynamicSchedulesResponse:
        try:
            result = await self.service.get_schedules_in_period(request.user_id)

            schedule_times_map = {
                medicine: schedule_pb2.TimeList(times=times)
                for medicine, times in result["data"].items()
            }

            return schedule_pb2.DynamicSchedulesResponse(
                message=result["message"],
                schedule_times=schedule_times_map
            )

        except Exception as e:
            context.set_details(f"Unexpected error: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return schedule_pb2.DynamicSchedulesResponse()

