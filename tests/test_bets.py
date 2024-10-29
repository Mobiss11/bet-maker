import pytest
from datetime import datetime, timedelta

from app.models.bets import BetStatus
from app.models.events import EventStatus
from app.core.exceptions import (
    BetValidationError,
    EventNotFoundError,
    DeadlinePassedError
)


@pytest.mark.asyncio
async def test_create_bet_success(bet_service, sample_event, event_service, redis_storage):
    # Подготавливаем тестовые данные
    await redis_storage.cache_event(sample_event)
    amount = 100.0

    # Создаем ставку
    bet = await bet_service.create_bet(sample_event.event_id, amount)

    assert bet is not None
    assert bet.event_id == sample_event.event_id
    assert bet.amount == amount
    assert bet.status == BetStatus.PENDING
    assert bet.coefficient == sample_event.coefficient


@pytest.mark.asyncio
async def test_create_bet_nonexistent_event(bet_service):
    with pytest.raises(EventNotFoundError):
        await bet_service.create_bet("nonexistent", 100.0)


@pytest.mark.asyncio
async def test_create_bet_expired_event(bet_service, expired_event, event_service, redis_storage):
    await redis_storage.cache_event(expired_event)

    with pytest.raises(DeadlinePassedError):
        await bet_service.create_bet(expired_event.event_id, 100.0)


@pytest.mark.asyncio
async def test_create_bet_invalid_amount(bet_service, sample_event, event_service, redis_storage):
    await redis_storage.cache_event(sample_event)

    with pytest.raises(BetValidationError):
        await bet_service.create_bet(sample_event.event_id, -100.0)


@pytest.mark.asyncio
async def test_get_bets(bet_service, sample_event, event_service, redis_storage):
    # Создаем несколько ставок
    await redis_storage.cache_event(sample_event)

    bet1 = await bet_service.create_bet(sample_event.event_id, 100.0)
    bet2 = await bet_service.create_bet(sample_event.event_id, 200.0)

    # Получаем все ставки
    bets = await bet_service.get_bets()

    assert len(bets) == 2
    assert any(b.id == bet1.id for b in bets)
    assert any(b.id == bet2.id for b in bets)


@pytest.mark.asyncio
async def test_update_bet_status(bet_service, sample_event, event_service, redis_storage):
    # Создаем ставку
    await redis_storage.cache_event(sample_event)
    bet = await bet_service.create_bet(sample_event.event_id, 100.0)

    # Обновляем статус события
    updated_bets = await bet_service.update_bet_status(
        sample_event.event_id,
        EventStatus.FIRST_TEAM_WON
    )

    assert len(updated_bets) == 1
    assert updated_bets[0].status == BetStatus.WON


@pytest.mark.asyncio
async def test_update_bet_status_loss(bet_service, sample_event, event_service, redis_storage):
    # Создаем ставку
    await redis_storage.cache_event(sample_event)
    bet = await bet_service.create_bet(sample_event.event_id, 100.0)

    # Обновляем статус события
    updated_bets = await bet_service.update_bet_status(
        sample_event.event_id,
        EventStatus.SECOND_TEAM_WON
    )

    assert len(updated_bets) == 1
    assert updated_bets[0].status == BetStatus.LOST
