import asyncio
import logging

import pytest
from httpx import AsyncClient

from core.models.event import StatusEnum

log = logging.getLogger(__name__)


@pytest.fixture(scope="function")
async def campaign_id(ac: AsyncClient) -> int:
    """
    Фикстура, возвращающая существующий campaign_id(Создаем либо передаем имеющийся)
    """
    events = await ac.get("/api/events/")
    data = events.json()
    if len(data) == 0:
        data_to_create = {
            "name": "Velocity",
        }
        response = await ac.post("/api/campaigns/", json=data_to_create)
        campaign = response.json()
        assert "id" in campaign
    else:
        campaign = data[0]
    return campaign["id"]


@pytest.mark.asyncio
async def test_create_campaign(ac: AsyncClient):
    """
    1. Проверяем создание кампании.
    """
    data_to_create = {
        "name": "Apple",
    }
    response = await ac.post("/api/campaigns/", json=data_to_create)
    assert response.status_code == 201

    data = response.json()
    assert "id" in data
    assert data["name"] == data_to_create["name"]


@pytest.mark.asyncio
async def test_create_event_deduplication(ac: AsyncClient, campaign_id: int):
    """
    2. Проверяем, что одинаковые события не создаются (дедупликация).
    """

    event_payload = {
        "campaign_id": campaign_id,
        "chat_id": 100,
        "account_id": 200,
        "message_id": 300,
    }

    first = await ac.post("/api/events/", json=event_payload)
    assert first.status_code == 201
    # При повторном создании возвращается 409
    second = await ac.post("/api/events/", json=event_payload)
    assert second.status_code == 409

    events = await ac.get("/api/events/")
    data = events.json()
    # Получаем единственный элемент
    assert len(data) == 1


@pytest.mark.asyncio
async def test_process_pending_events(ac: AsyncClient, campaign_id: int):
    """
    3. Проверяем исполнение событий (перевод в COMPLETED).
    """

    for i in range(1, 4):
        await ac.post(
            "/api/events/",
            json={
                "campaign_id": campaign_id,
                "chat_id": i,
                "account_id": i + 10,
                "message_id": i + 100,
            },
        )

    resp = await ac.get("/api/events/")
    events = resp.json()
    log.debug(f"Got events: {events}")
    # Все статусы PENDING
    assert all(e["status"] == StatusEnum.PENDING for e in events)

    # Запускаем scheduler
    process_resp = await ac.post("/api/scheduler/start")
    assert process_resp.status_code == 200
    await asyncio.sleep(1)
    resp = await ac.get("/api/events/")
    events_updated = resp.json()
    # Проверяем что были созданы новые event`ы
    assert len(events_updated) > len(events)
    # Проверяем, что все существовавшие event`ы имеют статус COMPLETED
    for i in events:
        for j in events_updated:
            if i["id"] == j["id"]:
                assert j["status"] == StatusEnum.COMPLETED
