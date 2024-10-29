from typing import List

from pydantic import BaseModel

from app.models.bets import Bet
from app.schemas.responses import DataResponse


class CreateBetRequest(BaseModel):
    event_id: str
    amount: float


class BetResponse(DataResponse[Bet]):
    pass


class BetsList(BaseModel):
    bets: List[Bet]


class BetsListResponse(DataResponse[BetsList]):
    pass
