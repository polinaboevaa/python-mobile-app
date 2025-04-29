import asyncio
import grpc
from app.grpc.service import ScheduleServiceGRPC
from app.proto import schedule_pb2_grpc, schedule_pb2
from app.database.database import get_async_db
from app.grpc.dependencies import make_schedule_service_for_grpc
from grpc_reflection.v1alpha import reflection

async def start_grpc_server():

    db_gen = get_async_db()
    db = await anext(db_gen)

    try:
        schedule_service = make_schedule_service_for_grpc(db)

        server = grpc.aio.server()
        schedule_pb2_grpc.add_ScheduleServiceServicer_to_server(
            ScheduleServiceGRPC(schedule_service), server
        )

        SERVICE_NAMES = (
            schedule_pb2.DESCRIPTOR.services_by_name['ScheduleService'].full_name,
            reflection.SERVICE_NAME,
        )

        reflection.enable_server_reflection(SERVICE_NAMES, server)

        server.add_insecure_port('[::]:50051')
        await server.start()
        print("gRPC async server started on port 50051...")

        try:
            await server.wait_for_termination()
        except asyncio.CancelledError:
            print("gRPC server cancellation received, shutting down gracefully...")
            await server.stop(grace=5)
            raise
    finally:
        await db_gen.aclose()
