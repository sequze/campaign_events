import pytest
from httpx import AsyncClient, ASGITransport

from app.core.config import settings
from app.core.models import Base
from app.core.db import db_helper
from app.main import app as fastapi_app


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    assert settings.mode.upper() == "TEST"

    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app), base_url="http://test"
    ) as ac:
        yield ac
