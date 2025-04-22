import grpc
from concurrent import futures
from app.grpc.service import ScheduleServiceGRPC
from app.proto import schedule_pb2_grpc
from app.database.database import get_async_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.grpc.dependencies import make_schedule_service_for_grpc

def start_grpc_server(db: AsyncSession = Depends(get_async_db)):
    schedule_service = make_schedule_service_for_grpc(db)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    schedule_pb2_grpc.add_ScheduleServiceServicer_to_server(ScheduleServiceGRPC(schedule_service), server)

    server.add_insecure_port('[::]:50051')
    print("gRPC server started on port 50051...")
    server.start()

    server.wait_for_termination()
