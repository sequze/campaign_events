from sqlalchemy import select, update, insert, inspect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert as pg_insert
from core.db.base_repository import SQlAlchemyRepository
from core.models import Event
from core.models.event import StatusEnum


class EventRepository(SQlAlchemyRepository):
    model = Event

    @classmethod
    async def create(cls, session: AsyncSession, data: dict) -> Event | None:
        mapper = inspect(cls.model)
        data_to_create = {k: v for k, v in data.items() if k in mapper.columns}

        stmt = (
            pg_insert(Event)
            .values(**data_to_create)
            .on_conflict_do_nothing(
                index_elements=[
                    Event.campaign_id,
                    Event.chat_id,
                    Event.message_id,
                ]
            )
            .returning(Event)
        )
        res = await session.execute(stmt)
        return res.scalar_one_or_none()

    @classmethod
    async def get_pending(cls, session: AsyncSession) -> list[Event]:
        """Получить все события со статусом PENDING"""
        stmt = select(Event).where(Event.status == StatusEnum.PENDING)
        res = await session.scalars(stmt)
        return list(res)

    @classmethod
    async def mark_completed(cls, session: AsyncSession):
        """Пометить все PENDING события как COMPLETED"""
        stmt = (
            update(Event)
            .where(Event.status == StatusEnum.PENDING)
            .values(status=StatusEnum.COMPLETED)
            .returning(Event)
        )
        res = await session.execute(stmt)
        return res.scalars().all()
