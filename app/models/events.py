from enum import Enum

from pydantic import BaseModel


class EventStatus(str, Enum):
    NEW = "new"
    FIRST_TEAM_WON = "first_team_won"
    SECOND_TEAM_WON = "second_team_won"


class Event(BaseModel):
    event_id: str
    coefficient: float
    deadline: str
    status: EventStatus = EventStatus.NEW
