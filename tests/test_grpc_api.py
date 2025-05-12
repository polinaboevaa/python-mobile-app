import grpc
import pytest
import asyncio
from app.settings import get_base_settings
from app.grpc.server import start_grpc_server
from app.grpc.generated import schedule_pb2_grpc, schedule_pb2

from tests.conftest import find_free_port


@pytest.fixture(scope="function")
async def grpc_server(test_db_settings):
    port = find_free_port()
    core_settings = get_base_settings()
    server_task = asyncio.create_task(
        start_grpc_server(test_db_settings, core_settings, port=port)
    )
    await asyncio.sleep(0.1)
    yield port
    server_task.cancel()
    try:
        await server_task
    except asyncio.CancelledError:
        pass

@pytest.fixture
async def grpc_client(grpc_server):
    port = grpc_server
    channel = grpc.aio.insecure_channel(f"localhost:{port}")
    stub = schedule_pb2_grpc.ScheduleServiceStub(channel)
    yield stub
    await channel.close()

@pytest.mark.asyncio
async def test_get_schedules_grpc(grpc_server, grpc_client):
    await grpc_client.AddSchedule(
        schedule_pb2.ScheduleModel(
            user_id=1,
            medicine="medicine1",
            frequency=3,
            duration_days=45
        )
    )
    await grpc_client.AddSchedule(
        schedule_pb2.ScheduleModel(
            user_id=1,
            medicine="medicine2",
            frequency=12,
            duration_days=12
        )
    )

    request = schedule_pb2.UserIdRequest(user_id=1)
    response = await grpc_client.GetSchedules(request)

    assert len(response.active_schedule_ids) == 2
    assert len(set(response.active_schedule_ids)) == len(response.active_schedule_ids)
