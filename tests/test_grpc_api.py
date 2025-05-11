import socket
from contextlib import closing
import grpc
import pytest
import asyncio
from testcontainers.postgres import PostgresContainer
from unittest.mock import patch
from urllib.parse import urlparse
from app.settings import DatabaseSettings,get_base_settings
from app.grpc.server import start_grpc_server
from app.grpc.generated import schedule_pb2_grpc, schedule_pb2
from alembic import command
from alembic.config import Config

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:13") as container:
        container.start()
        yield container

@pytest.fixture(scope="session")
def test_db_settings(postgres_container):
    parsed = urlparse(postgres_container.get_connection_url())
    return DatabaseSettings(
        USER=parsed.username,
        PASS=parsed.password,
        HOST=parsed.hostname,
        PORT=parsed.port,
        NAME=parsed.path[1:]
    )


@pytest.fixture(scope="function", autouse=True)
def apply_migrations(test_db_settings):
    alembic_cfg = Config("alembic.test.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", test_db_settings.database_url)

    command.upgrade(alembic_cfg, "head")

    yield

    command.downgrade(alembic_cfg, "base")
    command.upgrade(alembic_cfg, "head")

@pytest.fixture(autouse=True)
def override_settings(test_db_settings):
    import app.settings as settings
    settings.get_settings.cache_clear()
    with patch.object(settings, "get_settings", return_value=test_db_settings):
        yield

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
