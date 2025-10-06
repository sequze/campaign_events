from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.base_repository import SQlAlchemyRepository
from core.models import Event
from core.models.event import StatusEnum


class EventRepository(SQlAlchemyRepository):
    model = Event

    # @classmethod
    # async def create_unique(cls, session: AsyncSession, data: dict):
    #     """
    #     Создаёт событие, если такого (campaign_id, chat_id, message_id) ещё нет.
    #     Возвращает созданный объект или None, если дубликат.
    #     """
    #     stmt = select(Event).where(
    #         Event.campaign_id == data["campaign_id"],
    #         Event.chat_id == data["chat_id"],
    #         Event.message_id == data["message_id"],
    #     )
    #     existing = await session.execute(stmt)
    #     if existing.scalar_one_or_none():
    #         return None
    #
    #     return await cls.create(session, data)

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
