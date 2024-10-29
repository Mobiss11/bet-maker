from typing import Dict

from pydantic import BaseModel

from app.models.events import Event
from app.schemas.responses import DataResponse


class EventsList(BaseModel):
    events: Dict[str, Event]


class EventsListResponse(DataResponse[EventsList]):
    pass
