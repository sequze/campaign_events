from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.db.base_repository import SQlAlchemyRepository
from core.models import Campaign
from events.schema import EventDTO


class CampaignRepository(SQlAlchemyRepository):
    model = Campaign

    @classmethod
    async def get_by_name(cls, session: AsyncSession, name: str) -> Campaign | None:
        stmt = select(Campaign).where(Campaign.name == name)
        res = await session.execute(stmt)
        return res.scalar_one_or_none()
