import pytest
from app.models.common import StatusEnum


@pytest.mark.asyncio
async def test_get_events_api(client, event_service, sample_events, redis_storage):
    # Подготавливаем данные
    await redis_storage.cache_events_list({event.event_id: event for event in sample_events})

    # Делаем запрос
    response = await client.get("/events")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == StatusEnum.SUCCESS
    assert len(data["data"]["events"]) == len(sample_events)


@pytest.mark.asyncio
async def test_create_bet_api(client, sample_event, event_service, redis_storage):
    # Подготавливаем данные
    await redis_storage.cache_event(sample_event)

    # Создаем ставку
    response = await client.post(
        "/bet",
        json={
            "event_id": sample_event.event_id,
            "amount": 100.0
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == StatusEnum.SUCCESS
    assert data["data"]["event_id"] == sample_event.event_id


@pytest.mark.asyncio
async def test_create_bet_api_invalid_amount(client, sample_event, redis_storage):
    await redis_storage.cache_event(sample_event)

    response = await client.post(
        "/bet",
        json={
            "event_id": sample_event.event_id,
            "amount": -100.0
        }
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_bets_api(client, bet_service, sample_event, event_service, redis_storage):
    # Создаем тестовые ставки
    await redis_storage.cache_event(sample_event)
    await bet_service.create_bet(sample_event.event_id, 100.0)
    await bet_service.create_bet(sample_event.event_id, 200.0)

    # Получаем список ставок
    response = await client.get("/bets")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == StatusEnum.SUCCESS
    assert len(data["data"]["bets"]) == 2
