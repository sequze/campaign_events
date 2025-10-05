from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.config import settings


class DatabaseHelper:
    def __init__(
        self,
        url: str,
        pool_size: int,
        max_overflow: int,
        echo: bool = False,
    ):
        self.engine = create_async_engine(
            url=url,
            pool_size=pool_size,
            max_overflow=max_overflow,
            echo=echo,
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


db_helper = DatabaseHelper(
    url=str(settings.db.url),
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
    echo=settings.db.echo,
)
