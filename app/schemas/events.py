from typing import List

from pydantic import BaseModel

from app.models.events import Event
from app.schemas.responses import DataResponse


class EventsList(BaseModel):
    events: List[Event]


class EventsListResponse(DataResponse[EventsList]):
    pass
