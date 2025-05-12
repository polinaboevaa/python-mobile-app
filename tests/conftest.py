import socket
from contextlib import closing
from unittest.mock import patch
from urllib.parse import urlparse

import pytest
from alembic import command
from alembic.config import Config
from testcontainers.postgres import PostgresContainer

from app.settings import DatabaseSettings


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
