from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum

from app.core.config import settings
from app.models.bets import BetStatus

# Создаем базовый класс для моделей SQLAlchemy
Base = declarative_base()

# Создаем engine
engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


class BetDB(Base):
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True)
    event_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(Enum(BetStatus), nullable=False, default=BetStatus.PENDING)
    created_at = Column(DateTime, nullable=False)
    coefficient = Column(Float, nullable=True)
