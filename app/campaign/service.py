from campaign.schema import CampaignDTO, SCampaignModel
from campaign.repository import CampaignRepository
from core.db.uow import UnitOfWork
from events.repository import EventRepository
from events.schema import EventDTO


class CampaignService:
    def __init__(self, uow: UnitOfWork):
        self.repository = CampaignRepository
        self.uow = uow
        self.event_repository = EventRepository

    async def get_all(self):
        async with self.uow as uow:
            session = uow.session
            campaigns = await self.repository.get_all(session)
            return [CampaignDTO.model_validate(campaign) for campaign in campaigns]

    async def create(self, data: SCampaignModel) -> CampaignDTO:
        async with self.uow as uow:
            session = uow.session
            campaign = await self.repository.create(session, data.model_dump())
            await session.commit()
            return CampaignDTO.model_validate(campaign)

    async def get_or_create_active_campaign(self) -> int:
        async with self.uow as uow:
            session = uow.session
            campaigns = await self.repository.get_all(session)
            if len(campaigns) == 0:
                data = {"name": "Virality"}
                campaign = await self.repository.create(session, data)
            else:
                campaign = campaigns[0]
            return campaign.id

    async def get_campaign_events(self, id: int) -> list[EventDTO]:
        async with self.uow as uow:
            session = uow.session
            events = await self.event_repository.get_by_filters(
                session,
                {"campaign_id": id},
                one=False,
            )
            return [EventDTO.model_validate(event) for event in events]
