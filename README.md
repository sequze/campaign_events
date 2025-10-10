# Campaign Events API
_FastAPI, PostgreSQL, SQLAlchemy, APScheduler, pytest, httpx, docker compose_

## Быстрый запуск:
- Приложение:
```bash
cp .env.example .env
docker compose --profile default up -d
```
- Тесты:
```bash
cp .env.example .env
pip install poetry
poetry install
docker compose --profile test up -d
pytest
```

## Структура проекта:
- app/main.py - основной файл
- app/scheduler_manager.py — управление событиями (периодическое создание Event, обработка)
- app/api/* - эндпоинты
- app/campaign/*, app/events/* — схемы, репозитории, сервисы.
- app/core/* - настройка проекта, ORM и модели бд
- app/alembic/* - миграции
- tests/* - тесты

## Архитектурные решения
- Чистое разделение слоёв: роуты → сервис → репозиторий → БД.
- Идемпотентность на уровне БД (уникальный индекс) и репозитория (ON CONFLICT DO NOTHING).
- Исполнение событий: было принято решение использовать APScheduler, т.к. задачи асинхронные(работа с бд), а Celery поддерживает только синхронные задачи. Если нужно использовать Celery, можно подключить синхронный движок(psycopg), но для данного проекта лучшим решением для меня показалось использовать APScheduler.
- Для аккуратной работы с транзакциями и сессией реализовал паттерн Unit Of Work, который в виде контекстного менеджера работает с сессией, делает rollback при ошибке.