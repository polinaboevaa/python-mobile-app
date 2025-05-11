import pytest
from unittest.mock import AsyncMock, Mock

from fastapi import HTTPException

from app.services.schedule_service import ScheduleService
from datetime import timedelta, datetime, date
from app.settings import get_base_settings


@pytest.fixture
def mock_user_service():
    return AsyncMock()

@pytest.fixture
def mock_schedule_repo():
    return AsyncMock()

@pytest.fixture
def mock_helper_service():
    return Mock()

@pytest.fixture
def settings():
    return get_base_settings()

@pytest.fixture
def schedule_service(mock_schedule_repo, mock_user_service, mock_helper_service, settings):
    return ScheduleService(mock_schedule_repo, mock_user_service, mock_helper_service, settings)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "frequency, duration, start_of_reception, medicine",
    [
        (1, 5, datetime.now(), "Анальгин"),
        (2, None, datetime.now(), "Анальгин"),
        (3, 10, datetime.now(), "Анальгин"),
    ]
)
async def test_get_schedule_for_day_parametrized(frequency, duration, start_of_reception, mock_user_service, mock_schedule_repo, schedule_service,medicine):
    mock_user_service.check_user_existence.return_value = None

    mock_schedule_repo.get_schedule_data_by_schedule_id.return_value = (
        frequency, duration, start_of_reception, medicine
    )

    result = await schedule_service.get_schedule_for_day(user_id=1, schedule_id=1)

    assert result["schedule_id"] == 1
    assert result["medicine"] == "Анальгин"
    assert len(result["time_list"]) == frequency


@pytest.mark.asyncio
async def test_schedule_times_are_reasonable(mock_user_service, mock_schedule_repo, schedule_service,mock_helper_service, settings):
    mock_user_service.check_user_existence.return_value = None

    frequency = 10
    duration = 10
    start_of_reception = datetime.now()
    medicine = "Анальгин"

    mock_schedule_repo.get_schedule_data_by_schedule_id.return_value = (
        frequency, duration, start_of_reception, medicine
    )
    mock_helper_service.round_minutes.side_effect = lambda dt: dt.strftime("%H:%M")

    result = await schedule_service.get_schedule_for_day(user_id=1, schedule_id=1)


    times = [datetime.strptime(t, "%H:%M") for t in result["time_list"]]

    for i in range(len(times) - 1):
        assert times[i] < times[i + 1]

    for t in times:
        assert t < datetime.combine(date.today(), settings.START_TIME) + timedelta(hours=settings.INTERVAL_HOURS)

@pytest.mark.asyncio
async def test_get_schedule_user_does_not_exist(mock_user_service, mock_schedule_repo, schedule_service):
    mock_user_service.check_user_existence.side_effect = HTTPException(status_code=404, detail="Пользователь не найден")

    with pytest.raises(HTTPException) as http_exception:
        await schedule_service.get_schedule_for_day(user_id=1, schedule_id=1)

    assert http_exception.value.status_code == 404
    assert http_exception.value.detail == "Пользователь не найден"

@pytest.mark.asyncio
async def test_get_schedule_schedule_does_not_exist(mock_user_service, mock_schedule_repo, schedule_service):
    mock_schedule_repo.get_schedule_data_by_schedule_id.return_value = None

    result = await schedule_service.get_schedule_for_day(user_id=1, schedule_id=1)

    assert result["message"] == "Нет расписаний для пользователя"


@pytest.mark.asyncio
async def test_get_schedule_schedule_is_not_relevant(mock_user_service, mock_schedule_repo, schedule_service,mock_helper_service):
    mock_user_service.check_user_existence.return_value = None

    frequency = 13
    duration = 12
    start_of_reception = datetime.now() - timedelta(days=duration)
    medicine = "Анальгин"

    mock_schedule_repo.get_schedule_data_by_schedule_id.return_value = (
        frequency, duration, start_of_reception, medicine
    )

    mock_helper_service.is_schedule_active.return_value = False

    result = await schedule_service.get_schedule_for_day(user_id=1, schedule_id=1)

    assert result["message"] == "Расписание неактуально"

@pytest.mark.asyncio
async def test_get_schedule_division_by_zero(mock_user_service, mock_schedule_repo, schedule_service,mock_helper_service):
    mock_user_service.check_user_existence.return_value = None

    frequency = 0
    duration = 1
    start_of_reception = datetime.now()
    medicine = "Анальгин"

    mock_schedule_repo.get_schedule_data_by_schedule_id.return_value = (
        frequency, duration, start_of_reception, medicine
    )
    mock_helper_service.round_minutes.side_effect = lambda dt: dt.strftime("%H:%M")

    result = await schedule_service.get_schedule_for_day(user_id=1, schedule_id=1)

    assert result["message"] == "Некорректное расписание"


@pytest.mark.asyncio
async def test_get_schedules_in_period(mock_user_service, mock_schedule_repo, schedule_service, mock_helper_service):
    mock_user_service.check_user_existence.return_value = None

    frequency = 2
    duration = 5
    start_of_reception = datetime.now()
    medicine = "Анальгин"

    mock_schedule_repo.get_schedules_by_user_id.return_value = [
        (medicine, frequency, duration, start_of_reception),
    ]

    mock_helper_service.is_schedule_active.return_value = True
    mock_helper_service.round_minutes.side_effect = lambda dt: dt.strftime("%H:%M")

    result = await schedule_service.get_schedules_in_period(user_id=1)

    assert result["message"] == "Активные расписания для пользователя"
    assert medicine in result["data"]
    assert len(result["data"][medicine]) > 0


@pytest.mark.asyncio
async def test_get_schedules_in_period_valid_schedule(mock_user_service, mock_schedule_repo, schedule_service, mock_helper_service):

    mock_user_service.check_user_existence.return_value = None
    mock_helper_service.is_schedule_active.return_value = True
    mock_helper_service.round_minutes.side_effect = lambda x: x.strftime("%H:%M")

    frequency = 2
    duration = 5
    start_of_reception = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    medicine = "Анальгин"

    mock_schedule_repo.get_schedules_by_user_id.return_value = [
        (medicine, frequency, duration, start_of_reception),
    ]

    result = await schedule_service.get_schedules_in_period(user_id=1)

    schedule = result["data"][medicine]

    parsed_times = []
    for time_str in schedule:
        time_part, date_part = time_str.split()
        day, month = map(int, date_part.split('.'))
        hour, minute = map(int, time_part.split(':'))
        parsed_time = datetime(datetime.now().year, month, day, hour, minute)
        parsed_times.append(parsed_time)

    for i in range(len(parsed_times) - 1):
        assert parsed_times[i] < parsed_times[i + 1]


@pytest.mark.asyncio
async def test_get_schedules_in_period_inactive_schedule(mock_user_service, mock_schedule_repo, schedule_service, settings, mock_helper_service):
    mock_user_service.check_user_existence.return_value = None

    mock_schedule_repo.get_schedules_by_user_id.return_value = [
        ("Анальгин", 2, 5, datetime.now() - timedelta(days=6)),
        ("Пенталгин", 3, 6, datetime.now())
    ]

    mock_helper_service.is_schedule_active.side_effect = [False, True]
    mock_helper_service.round_minutes.side_effect = lambda dt: dt.strftime("%H:%M")

    settings.PERIOD = timedelta(days=1)
    settings.INTERVAL_HOURS = 24

    result = await schedule_service.get_schedules_in_period(user_id=1)

    assert result["message"] == "Активные расписания для пользователя"
    assert "Пенталгин" in result["data"]
    assert "Анальгин" not in result["data"]

@pytest.mark.asyncio
async def test_get_schedules_in_period_no_schedules(mock_user_service, mock_schedule_repo, schedule_service):
    mock_user_service.check_user_existence.return_value = None

    mock_schedule_repo.get_schedules_by_user_id.return_value = []

    result = await schedule_service.get_schedules_in_period(user_id=1)

    assert result["message"] == "Нет расписаний для пользователя"
    assert not result["data"]


@pytest.mark.asyncio
async def test_get_schedules_in_period_incorrect_schedule(mock_user_service, mock_schedule_repo, schedule_service):
    mock_user_service.check_user_existence.return_value = None

    frequency = 0
    duration = 5
    start_of_reception = datetime.now()
    medicine = "Анальгин"

    mock_schedule_repo.get_schedules_by_user_id.return_value = [
        (medicine, frequency, duration, start_of_reception),
    ]

    result = await schedule_service.get_schedules_in_period(user_id=1)

    assert result["message"] == "Некорректное расписание"
    assert not result["data"]


@pytest.mark.asyncio
async def test_get_schedules_in_period_within_date_range(mock_user_service, mock_schedule_repo, schedule_service,settings, mock_helper_service):
    mock_user_service.check_user_existence.return_value = None

    frequency = 10
    duration = 5
    start_of_reception = datetime.now()
    medicine = "Анальгин"

    mock_schedule_repo.get_schedules_by_user_id.return_value = [
        (medicine, frequency, duration, start_of_reception),
    ]

    mock_helper_service.is_schedule_active.return_value = True
    mock_helper_service.round_minutes.side_effect = lambda dt: dt.strftime("%H:%M")

    settings.PERIOD = timedelta(days=1)
    result = await schedule_service.get_schedules_in_period(user_id=1)

    assert result["message"] == "Активные расписания для пользователя"
    assert "Анальгин" in result["data"]
    assert len(result["data"]["Анальгин"]) > 0

@pytest.mark.asyncio
async def test_get_schedules_ids_with_active_schedules(mock_user_service, mock_schedule_repo, schedule_service, mock_helper_service):
    mock_user_service.check_user_existence.return_value = None

    mock_schedule_repo.get_schedules_data_by_user_id.return_value = [
        (1, 10, datetime.now()),
        (2, 5, datetime.now() - timedelta(days=1)),
    ]
    mock_helper_service.is_schedule_active.return_value = True

    result = await schedule_service.get_schedules_ids(user_id=1)

    assert "active_schedule_ids" in result
    assert result["active_schedule_ids"] == [1, 2]

@pytest.mark.asyncio
async def test_get_schedules_ids_with_one_inactive_schedule(mock_user_service, mock_schedule_repo, schedule_service, mock_helper_service):
    mock_user_service.check_user_existence.return_value = None

    mock_schedule_repo.get_schedules_data_by_user_id.return_value = [
        (1, 10, datetime.now()),
        (2, 5, datetime.now() - timedelta(days=6)),
    ]
    mock_helper_service.is_schedule_active.side_effect = [True, False]

    result = await schedule_service.get_schedules_ids(user_id=1)

    assert "active_schedule_ids" in result
    assert result["active_schedule_ids"] == [1]

@pytest.mark.asyncio
async def test_get_schedules_ids_with_inactive_schedules(mock_user_service, mock_schedule_repo, schedule_service, mock_helper_service):
    mock_user_service.check_user_existence.return_value = None

    mock_schedule_repo.get_schedules_data_by_user_id.return_value = [
        (1, 10, datetime.now() - timedelta(days=11)),
        (2, 5, datetime.now() - timedelta(days=6)),
    ]
    mock_helper_service.is_schedule_active.return_value = False

    result = await schedule_service.get_schedules_ids(user_id=1)

    assert "active_schedule_ids" in result
    assert result["active_schedule_ids"] == []


