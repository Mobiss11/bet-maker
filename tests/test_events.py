import pytest
from unittest.mock import patch
from httpx import Response
import json

from app.models.events import EventStatus
from app.models.common import StatusEnum
from app.core.exceptions import LineProviderError


@pytest.mark.asyncio
async def test_get_events_from_cache(event_service, sample_events, redis_storage):
    # Кэшируем события
    await redis_storage.cache_events_list({event.event_id: event for event in sample_events})

    # Получаем события
    events = await event_service.get_events()
    assert len(events) == len(sample_events)
    assert all(event.event_id in events for event in sample_events)


@pytest.mark.asyncio
async def test_get_events_from_line_provider(event_service, sample_events):
    # Мокаем ответ от line-provider
    mock_response = {
        "status": "success",
        "data": {
            "events": {event.event_id: event.model_dump() for event in sample_events}
        }
    }

    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.return_value = Response(200, json=mock_response)
        events = await event_service.get_events()

        assert len(events) == len(sample_events)
        assert all(event.event_id in events for event in sample_events)


@pytest.mark.asyncio
async def test_get_events_line_provider_error(event_service):
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.side_effect = Exception("Connection error")

        with pytest.raises(LineProviderError):
            await event_service.get_events()


@pytest.mark.asyncio
async def test_get_single_event_from_cache(event_service, sample_event, redis_storage):
    # Кэшируем событие
    await redis_storage.cache_event(sample_event)

    # Получаем событие
    event = await event_service.get_event(sample_event.event_id)
    assert event is not None
    assert event.event_id == sample_event.event_id


@pytest.mark.asyncio
async def test_get_nonexistent_event(event_service):
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.return_value = Response(404)
        event = await event_service.get_event("nonexistent")
        assert event is None
