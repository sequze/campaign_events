from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.config import settings


class DatabaseHelper:
    def __init__(
        self,
        url: str,
        params: dict,
    ):
        self.engine = create_async_engine(
            url=url,
            **params,
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self):
        await self.engine.dispose()

    async def session_getter(self):
        async with self.session_factory() as session:
            yield session


if settings.mode == "TEST":
    db_url = settings.test_db.url
    params = {"poolclass": NullPool, "echo": False}
elif settings.mode == "PROD" or settings.mode == "DEV":
    db_url = settings.db.url
    params = {
        "echo": settings.db.echo,
        "pool_size": settings.db.pool_size,
        "max_overflow": settings.db.max_overflow,
    }
else:
    raise ValueError(f"Invalid mode {settings.mode}")
db_helper = DatabaseHelper(
    url=str(db_url),
    params=params,
)
