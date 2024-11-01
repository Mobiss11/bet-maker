from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Bet Maker Service"
    DEBUG: bool = False

    # База данных
    DATABASE_URL: str = "postgresql+asyncpg://betmaker:betmaker@127.0.0.1:5432/betmaker"

    # Redis
    REDIS_URL: str = "redis://127.0.0.1:6379/0"
    EVENT_CACHE_TTL: int = 30  # Время кеширования событий в секундах

    # Line Provider
    LINE_PROVIDER_URL: str = "http://127.0.0.1:8000"
    LINE_PROVIDER_TIMEOUT: int = 5  # Таймаут для запросов к line-provider

    # Настройки приложения
    MIN_BET_AMOUNT: float = 1.0  # Минимальная сумма ставки
    MAX_BET_AMOUNT: float = 100000.0  # Максимальная сумма ставки

    class Config:
        env_file = ".env"


settings = Settings()
