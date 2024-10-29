from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class BetStatus(str, Enum):
    PENDING = "pending"  # Ставка ожидает результата
    WON = "won"  # Ставка выиграла
    LOST = "lost"  # Ставка проиграла


class Bet(BaseModel):
    id: int | None = None
    event_id: str
    amount: float = Field(gt=0)
    status: BetStatus = BetStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.now)
    coefficient: float | None = None  # Коэффициент на момент ставки
