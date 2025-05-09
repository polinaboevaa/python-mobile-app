import pytest
from unittest.mock import AsyncMock
from app.services.schedule_service import ScheduleService
from datetime import time, timedelta

@pytest.fixture
def mock_user_service():
    return AsyncMock()

@pytest.fixture
def mock_schedule_repo():
    return AsyncMock()

@pytest.fixture
def schedule_service(mock_schedule_repo, mock_user_service):
    return ScheduleService(mock_schedule_repo, mock_user_service)

@pytest.fixture
def fake_settings():
    class FakeSettings:
        INTERVAL_HOURS = 12
        START_TIME = time(8, 0)
        PERIOD = timedelta(days=3)
    return FakeSettings()



@pytest.mark.asyncio
@pytest.mark.parametrize(
    "frequency, duration, expected_times_count",
    [
        (3, 10, 3),    # обычный случай
        (1, 5, 1),     # граница - 1 приём в день
        (2, 0, 2),     # граница - 0 дней (всё ещё сегодня может быть)
    ]
)
async def test_get_schedule_for_day_parametrized(frequency, duration, expected_times_count, mock_user_service, mock_schedule_repo, schedule_service, fake_settings):
    mock_user_service.check_user_existence.return_value = None

    start_time = fake_settings.START_TIME
    mock_schedule_repo.get_schedule_data_by_schedule_id.return_value = (
        frequency, duration, start_time, "Анальгин"
    )

    result = await schedule_service.get_schedule_for_day(user_id=1, schedule_id=1)

    assert result["medicine"] == "string"
    assert len(result["time_list"]) == expected_times_count
