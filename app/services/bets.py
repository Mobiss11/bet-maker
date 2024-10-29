from typing import List, Optional
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.bets import Bet, BetStatus
from app.models.events import Event, EventStatus
from app.storage.postgres import BetDB
from app.core.config import settings
from app.core.exceptions import (
    BetValidationError,
    EventNotFoundError,
    DeadlinePassedError
)


class BetService:
    def __init__(self, session: AsyncSession, event_service):
        self.session = session
        self.event_service = event_service

    async def create_bet(self, event_id: str, amount: float) -> Bet:
        """Создание новой ставки"""
        # Проверяем существование события
        event = await self.event_service.get_event(event_id)
        if not event:
            raise EventNotFoundError(event_id)

        # Проверяем время дедлайна
        deadline = datetime.fromisoformat(event.deadline)
        if deadline <= datetime.now():
            raise DeadlinePassedError(event_id)

        # Валидируем сумму ставки
        if not settings.MIN_BET_AMOUNT <= amount <= settings.MAX_BET_AMOUNT:
            raise BetValidationError(
                f"Сумма ставки должна быть между {settings.MIN_BET_AMOUNT} и {settings.MAX_BET_AMOUNT}"
            )

        # Создаем ставку
        bet_db = BetDB(
            event_id=event_id,
            amount=amount,
            coefficient=event.coefficient,
            created_at=datetime.now()
        )

        self.session.add(bet_db)
        await self.session.commit()
        await self.session.refresh(bet_db)

        return Bet(
            id=bet_db.id,
            event_id=bet_db.event_id,
            amount=bet_db.amount,
            status=bet_db.status,
            created_at=bet_db.created_at,
            coefficient=bet_db.coefficient
        )

    async def get_bets(self) -> List[Bet]:
        """Получение списка всех ставок"""
        query = select(BetDB).order_by(BetDB.created_at.desc())
        result = await self.session.execute(query)
        bets_db = result.scalars().all()

        return [
            Bet(
                id=bet.id,
                event_id=bet.event_id,
                amount=bet.amount,
                status=bet.status,
                created_at=bet.created_at,
                coefficient=bet.coefficient
            )
            for bet in bets_db
        ]

    async def get_bet(self, bet_id: int) -> Optional[Bet]:
        """Получение информации о конкретной ставке"""
        bet_db = await self.session.get(BetDB, bet_id)
        if not bet_db:
            return None

        return Bet(
            id=bet_db.id,
            event_id=bet_db.event_id,
            amount=bet_db.amount,
            status=bet_db.status,
            created_at=bet_db.created_at,
            coefficient=bet_db.coefficient
        )

    async def update_bet_status(self, event_id: str, event_status: EventStatus) -> List[Bet]:
        """Обновление статуса ставок при изменении статуса события"""
        query = select(BetDB).where(BetDB.event_id == event_id)
        result = await self.session.execute(query)
        bets_db = result.scalars().all()

        updated_bets = []
        for bet_db in bets_db:
            if event_status == EventStatus.FIRST_TEAM_WON:
                bet_db.status = BetStatus.WON
            elif event_status == EventStatus.SECOND_TEAM_WON:
                bet_db.status = BetStatus.LOST

            updated_bets.append(Bet(
                id=bet_db.id,
                event_id=bet_db.event_id,
                amount=bet_db.amount,
                status=bet_db.status,
                created_at=bet_db.created_at,
                coefficient=bet_db.coefficient
            ))

        await self.session.commit()
        return updated_bets
