import pytest
from httpx import AsyncClient, ASGITransport
from app.main import make_app

@pytest.fixture
async def rest_client():
    app = make_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac

@pytest.mark.asyncio
async def test_get_schedules_rest(rest_client):
    resp1 = await rest_client.post("/schedule", json={
        "user_id": 1,
        "medicine": "medicine1",
        "frequency": 3,
        "duration_days": 45
    })
    assert resp1.status_code == 200
    schedule_id1 = resp1.json()["schedule_id"]

    resp2 = await rest_client.post("/schedule", json={
        "user_id": 1,
        "medicine": "medicine2",
        "frequency": 12,
        "duration_days": 12
    })
    assert resp2.status_code == 200
    schedule_id2 = resp2.json()["schedule_id"]

    response = await rest_client.get("/schedules", params={"user_id": 1})
    assert response.status_code == 200
    data = response.json()

    assert "active_schedule_ids" in data
    assert len(data["active_schedule_ids"]) == 2
    assert set(data["active_schedule_ids"]) == {schedule_id1, schedule_id2}
