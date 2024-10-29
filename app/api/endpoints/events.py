from fastapi import APIRouter, HTTPException, Depends

from app.services.events import EventService
from app.schemas.events import EventsListResponse
from app.storage.redis import RedisStorage
from app.models.common import StatusEnum

router = APIRouter()


def get_event_service():
    return EventService(RedisStorage())


@router.get("/events", response_model=EventsListResponse)
async def get_events(
        service: EventService = Depends(get_event_service)
):
    """Получение списка доступных событий"""
    try:
        events = await service.get_events()
        return EventsListResponse(
            status=StatusEnum.SUCCESS,
            message="События успешно получены",
            data={"events": events}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
