import logging
import random

from sqlalchemy.ext.asyncio import AsyncSession
from core.db.uow import UnitOfWork
from events.repository import EventRepository
from events.schema import SEventModel, EventDTO

log = logging.getLogger(__name__)


class EventExistsError(Exception):
    pass


class EventService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.repository = EventRepository

    async def get_all(self):
        async with self.uow as uow:
            session = uow.session
            events = await self.repository.get_all(session)
            return [EventDTO.model_validate(e) for e in events]

    @classmethod
    def _generate_random_event_values(cls) -> dict:
        return {
            "account_id": random.randint(1, 10000),
            "chat_id": random.randint(1, 10000),
            "message_id": random.randint(1, 10000),
        }

    async def _validate_input_data(self, session: AsyncSession, data: dict) -> bool:
        filters = {
            "account_id": data["account_id"],
            "chat_id": data["chat_id"],
            "message_id": data["message_id"],
        }
        log.debug(f"Validating event by filters: {filters}")
        exists = await self.repository.get_by_filters(
            session,
            filters,
        )
        log.debug(f"Got: {exists}")
        return exists is not None

    async def create(
        self,
        data: SEventModel,
    ) -> EventDTO:
        async with self.uow as uow:
            session = uow.session
            exists = await self._validate_input_data(session, data.model_dump())
            if exists:
                raise EventExistsError("Event already exists")
            res = await self.repository.create(session, data.model_dump())
            await session.commit()
            return EventDTO.model_validate(res)

    async def create_random_event(self, campaign_id: int) -> EventDTO | None:
        """
        Создаёт событие, если такой комбинации (campaign_id, chat_id, message_id)
         ещё нет. Возвращает созданный объект или None,
         если событие уже существует.
        """
        if campaign_id < 1:
            return None
        async with self.uow as uow:
            session = uow.session
            data_to_create = self._generate_random_event_values()
            data_to_create.update(campaign_id=campaign_id)
            exists = await self._validate_input_data(session, data_to_create)
            if exists:
                log.debug(f"Event already exists.Skipped")
                return None
            event = await self.repository.create(session, data_to_create)
            log.debug(f"Created new event: {event}")
            await session.commit()
            return event

    async def mark_all_pending_events_completed(self):
        async with self.uow as uow:
            session = uow.session
            await self.repository.mark_completed(session)
            await session.commit()
