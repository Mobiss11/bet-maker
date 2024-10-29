import asyncio

import pytest

from datetime import datetime, timedelta
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.models.events import Event, EventStatus
from app.storage.postgres import Base
from app.storage.redis import RedisStorage
from app.services.events import EventService
from app.services.bets import BetService

# Тестовая база данных
TEST_DATABASE_URL = "postgresql+asyncpg://betmaker:betmaker@localhost:5432/betmaker"
TEST_REDIS_URL = "redis://localhost:6379/1"

# Тестовые данные
TEST_EVENTS = [
    {
        "event_id": "event1",
        "coefficient": 1.85,
        "deadline": (datetime.now() + timedelta(days=1)).isoformat(),
        "status": "new"
    },
    {
        "event_id": "event2",
        "coefficient": 2.10,
        "deadline": (datetime.now() + timedelta(days=1)).isoformat(),
        "status": "new"
    }
]


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def db_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def db_session(db_engine):
    TestingSessionLocal = sessionmaker(
        db_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def redis_storage():
    storage = RedisStorage()
    storage.redis_url = TEST_REDIS_URL
    return storage


@pytest.fixture
def event_service(redis_storage):
    return EventService(redis_storage)


@pytest.fixture
def bet_service(db_session, event_service):
    return BetService(db_session, event_service)


@pytest.fixture
def sample_event():
    return Event(
        event_id="test_event_1",
        coefficient=1.85,
        deadline=(datetime.now() + timedelta(days=1)).isoformat(),
        status=EventStatus.NEW
    )


@pytest.fixture
def sample_events():
    return [Event(**event_data) for event_data in TEST_EVENTS]


@pytest.fixture
def expired_event():
    return Event(
        event_id="expired_event",
        coefficient=1.85,
        deadline=(datetime.now() - timedelta(hours=1)).isoformat(),
        status=EventStatus.NEW
    )
