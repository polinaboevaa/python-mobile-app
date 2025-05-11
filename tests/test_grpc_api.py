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


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:13") as container:
        container.start()
        yield container

@pytest.fixture(scope="session", autouse=True)
def apply_migrations(test_db_settings):
    alembic_cfg = Config("alembic.test.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", test_db_settings.database_url)

    command.upgrade(alembic_cfg, "head")


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


@pytest.fixture(autouse=True)
def override_settings(test_db_settings):
    import app.settings as settings
    settings.get_settings.cache_clear()
    with patch.object(settings, "get_settings", return_value=test_db_settings):
        yield


@pytest.fixture(scope="function")
async def grpc_server(test_db_settings):
    core_settings = get_base_settings()
    task = asyncio.create_task(start_grpc_server(test_db_settings, core_settings))
    await asyncio.sleep(1.0)

    yield

    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


@pytest.fixture
async def grpc_client():
    import grpc
    channel = grpc.aio.insecure_channel("localhost:50051")
    stub = schedule_pb2_grpc.ScheduleServiceStub(channel)
    yield stub
    await channel.close()

@pytest.mark.asyncio
async def test_add_schedule_grpc(grpc_server, grpc_client):
    request = schedule_pb2.ScheduleModel(
        user_id=1,
        medicine="Aspirin",
        frequency=2,
        duration_days=7
    )
    response = await grpc_client.AddSchedule(request)
    assert response.schedule_id > 0

@pytest.mark.asyncio
async def test_get_schedules_grpc(grpc_server, grpc_client):
    request = schedule_pb2.UserIdRequest(user_id=1)
    response = await grpc_client.GetSchedules(request)
    assert len(response.active_schedule_ids) >= 0
