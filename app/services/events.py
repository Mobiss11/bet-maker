from typing import List, Optional

import httpx

from app.models.events import Event
from app.storage.redis import RedisStorage
from app.core.config import settings
from app.core.exceptions import LineProviderError


class EventService:
    def __init__(self, storage: RedisStorage):
        self.storage = storage
        self.line_provider_url = settings.LINE_PROVIDER_URL

    async def get_events(self) -> List[Event]:
        """Получение списка доступных событий"""
        # Пробуем получить из кэша
        # cached_events = await self.storage.get_cached_events_list()
        # if cached_events:
        #     return [Event(**event) for event in cached_events]

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.line_provider_url}/events",
                    timeout=settings.LINE_PROVIDER_TIMEOUT
                )
                response.raise_for_status()

                events = []
                for event in response.json()["data"]["events"]:
                    events.append(Event(**event))


                # for event in events:
                #     await self.storage.cache_event(event)
                # await self.storage.cache_events_list([event.dict() for event in events])
                return events
        except Exception as e:
            raise LineProviderError(str(e))

    async def get_event(self, event_id: str) -> Optional[Event]:
        """Получение информации о конкретном событии"""
        # Пробуем получить из кэша
        # cached_event = await self.storage.get_cached_event(event_id)
        # if cached_event:
        #     return cached_event

        # Если нет в кэше, получаем от line provider
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.line_provider_url}/events/{event_id}",
                    timeout=settings.LINE_PROVIDER_TIMEOUT
                )
                response.raise_for_status()
                event = Event(**response.json()["data"])

                # Кэшируем результат
                await self.storage.cache_event(event)
                return event
        except httpx.HTTPError as e:
            if e.response and e.response.status_code == 404:
                return None
            raise LineProviderError(str(e))
