# Bet Maker Service

## Описание
Bet Maker Service - это сервис для управления ставками, разработанный с использованием FastAPI, PostgreSQL и Redis. Сервис предоставляет API для создания ставок, получения информации о событиях от Line Provider и управления историей ставок.

## Особенности
- 🚀 Асинхронная обработка запросов
- 💾 PostgreSQL для хранения ставок
- 📦 Redis для кэширования событий
- 🔗 Интеграция с Line Provider
- 📝 Автоматическая OpenAPI документация
- 🧪 Полное тестовое покрытие
- 🐳 Docker и Docker Compose поддержка

## Требования
- Python 3.10+
- PostgreSQL 13+
- Redis 6+
- Docker и Docker Compose (для контейнеризации)

## Структура проекта
```
bet_maker/
│
├── app/
│   ├── __init__.py
│   ├── main.py              # Основной файл приложения
│   ├── api/                 # API endpoints
│   │   ├── endpoints/
│   │   │   ├── bets.py     # Эндпоинты для ставок
│   │   │   └── events.py   # Эндпоинты для событий
│   ├── core/                # Конфигурация и базовые компоненты
│   ├── models/              # Pydantic модели
│   ├── schemas/             # Схемы запросов/ответов
│   ├── services/            # Бизнес-логика
│   └── storage/             # Работа с БД и кэшем
│
├── migrations/              # Миграции базы данных
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # Общие фикстуры и конфигурация
│   ├── test_bets.py        # Тесты для ставок
│   ├── test_events.py      # Тесты для событий
│   └── test_service.py     # Тесты для сервисов
│
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

## Установка и запуск

### Локальная разработка
```bash
# Клонирование репозитория
git clone https://github.com/Mobiss11/bet-maker
cd bet-maker

# Создание и активация виртуального окружения
python3.10 -m venv venv
source venv/bin/activate

# Установка и обновление необходимых инструментов
pip install pip --upgrade
pip install setuptools --upgrade
pip install poetry

# Установка зависимостей проекта
poetry install

# Применение миграций
alembic upgrade head
```

### Запуск через Docker
```bash
# Сборка
docker build -t bet-maker:latest .

# Сборка и запуск
docker-compose up --build

# Только запуск (если образ уже собран)
docker-compose up -d

# Остановка
docker-compose down
```

## Конфигурация
Настройки приложения можно изменить через переменные окружения или файл `.env`:

```env
APP_NAME=Bet Maker Service
DEBUG=true
DATABASE_URL=postgresql+asyncpg://betmaker:betmaker@127.0.0.1:5432/betmaker
REDIS_URL=redis://127.0.0.1:6379
LINE_PROVIDER_URL=http://127.0.0.1:8000
LINE_PROVIDER_TIMEOUT=5
MIN_BET_AMOUNT=1.0
MAX_BET_AMOUNT=100000.0
```

## Тестирование

### Настройка окружения для тестов
```bash
# Запуск тестового окружения
docker-compose -f docker-compose.test.yml up -d

# Применение миграций для тестовой БД
alembic upgrade head
```

### Запуск тестов
```bash
# Запуск всех тестов
poetry run pytest

# Запуск с подробным выводом
poetry run pytest -v

# Запуск тестов с покрытием
poetry run pytest --cov=app tests/

# Запуск конкретной группы тестов
poetry run pytest tests/test_bets.py

# Запуск тестов с метками
poetry run pytest -m "integration"  # интеграционные тесты

# Параллельный запуск тестов
poetry run pytest -n auto
```

### Тестовое покрытие
```bash
# Генерация HTML-отчета о покрытии
poetry run pytest --cov=app --cov-report=html

# Отчет будет доступен в coverage_html/index.html
```

## Configuration Ruff
```toml
[tool.ruff]
fix = true
unsafe-fixes = true
line-length = 120
select = ["ALL"]
ignore = ["D1", "D203", "D213", "FA102", "ANN101", "UP007", "TCH001", "BLE001", "DTZ005", "TRY300", "DTZ007"]

[tool.ruff.isort]
no-lines-before = ["standard-library", "local-folder"]
known-third-party = []
known-local-folder = ["whole_app"]

[tool.ruff.extend-per-file-ignores]
"./*.py" = ["ANN401", "S101", "S311", "F401"]
```

## API Endpoints

### Ставки (Bets)

#### Создание ставки
```http
POST /bet
```
Запрос:
```json
{
    "event_id": "event1",
    "amount": 100.50
}
```
Ответ:
```json
{
    "status": "success",
    "message": "Ставка успешно создана",
    "data": {
        "id": 1,
        "event_id": "event1",
        "amount": 100.50,
        "coefficient": 1.85,
        "status": "pending",
        "created_at": "2024-03-25T12:00:00"
    }
}
```

#### Получение списка ставок
```http
GET /bets
```

#### Получение списка событий
```http
GET /events
```

## Производительность

### Кэширование
- Кэширование событий от Line Provider в Redis
- Настраиваемое время жизни кэша
- Автоматическая инвалидация

### БД оптимизации
- Асинхронные запросы к PostgreSQL
- Индексы для часто используемых полей
- Эффективные миграции

## Безопасность

### Основные меры
- Валидация входных данных
- Проверка лимитов ставок
- CORS настройки
- Безопасные заголовки

### Рекомендации по развертыванию
- Использование HTTPS
- Настройка файрвола
- Регулярное обновление зависимостей

## FAQ

### Как добавить новый endpoint?
1. Создайте новый файл в `app/api/endpoints/`
2. Определите новый router
3. Добавьте router в `app/api/routes.py`
4. Добавьте тесты

### Как изменить лимиты ставок?
Измените `MIN_BET_AMOUNT` и `MAX_BET_AMOUNT` в настройках окружения или `.env` файле.

### Как масштабировать сервис?
1. Используйте несколько инстансов приложения
2. Настройте балансировщик нагрузки
3. Используйте репликацию PostgreSQL
4. Настройте Redis Cluster для кэширования