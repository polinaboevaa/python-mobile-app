import asyncio
import grpc
from app.database.session import get_db_session
from app.grpc.logging_interceptor import LoggingInterceptor
from app.grpc.service import ScheduleServiceGRPC
from app.grpc.generated import schedule_pb2_grpc, schedule_pb2
from app.grpc.dependencies import make_schedule_service_for_grpc
from grpc_reflection.v1alpha import reflection

from app.settings import get_base_settings


async def start_grpc_server():
    db_generator = get_db_session()

    db = await anext(db_generator)

    try:
        settings = get_base_settings()
        schedule_service = make_schedule_service_for_grpc(db, settings)

        server = grpc.aio.server(interceptors=[LoggingInterceptor()])
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
    except Exception as e:
        print(f"gRPC server crashed: {str(e)}")
    finally:
        try:
            await anext(db_generator)
        except StopAsyncIteration:
            pass
