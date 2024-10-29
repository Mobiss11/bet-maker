import json
from typing import Optional, Dict

from redis import asyncio as aioredis

from app.core.config import settings
from app.models.events import Event


class RedisStorage:
    def __init__(self):
        self.redis = aioredis.from_url(settings.REDIS_URL)
        self.EVENT_PREFIX = "event:"

    async def cache_event(self, event: Event) -> None:
        """Кэширование события"""
        key = f"{self.EVENT_PREFIX}{event.event_id}"
        await self.redis.set(
            key,
            event.model_dump_json(),
            ex=settings.EVENT_CACHE_TTL
        )

    async def get_cached_event(self, event_id: str) -> Optional[Event]:
        """Получение события из кэша"""
        key = f"{self.EVENT_PREFIX}{event_id}"
        data = await self.redis.get(key)
        if data:
            return Event.model_validate_json(data)
        return None

    async def cache_events_list(self, events: Dict[str, Event]) -> None:
        """Кэширование списка событий"""
        await self.redis.set(
            "events_list",
            json.dumps({k: v.model_dump() for k, v in events.items()}),
            ex=settings.EVENT_CACHE_TTL
        )

    async def get_cached_events_list(self) -> Optional[Dict[str, Event]]:
        """Получение списка событий из кэша"""
        data = await self.redis.get("events_list")
        if data:
            events_dict = json.loads(data)
            return {k: Event(**v) for k, v in events_dict.items()}
        return None
