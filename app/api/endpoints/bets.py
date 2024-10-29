from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.bets import BetService
from app.services.events import EventService
from app.schemas.bets import (
    CreateBetRequest,
    BetResponse,
    BetsListResponse
)
from app.storage.postgres import AsyncSessionLocal
from app.storage.redis import RedisStorage
from app.models.common import StatusEnum
from app.core.exceptions import (
    BetValidationError,
    EventNotFoundError,
    DeadlinePassedError
)

router = APIRouter()


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


def get_bet_service(
        session: AsyncSession = Depends(get_session),
        event_service: EventService = Depends(lambda: EventService(RedisStorage()))
):
    return BetService(session, event_service)


@router.post("/bet", response_model=BetResponse)
async def create_bet(
        bet_request: CreateBetRequest,
        service: BetService = Depends(get_bet_service)
):
    """Создание новой ставки"""
    try:
        bet = await service.create_bet(
            bet_request.event_id,
            bet_request.amount
        )
        return BetResponse(
            status=StatusEnum.SUCCESS,
            message="Ставка успешно создана",
            data=bet
        )
    except (BetValidationError, EventNotFoundError, DeadlinePassedError) as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/bets", response_model=BetsListResponse)
async def get_bets(
        service: BetService = Depends(get_bet_service)
):
    """Получение списка всех ставок"""
    try:
        bets = await service.get_bets()
        return BetsListResponse(
            status=StatusEnum.SUCCESS,
            message="Список ставок получен",
            data={"bets": bets}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
