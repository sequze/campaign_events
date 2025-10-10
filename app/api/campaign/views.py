from fastapi import APIRouter

from events.schema import EventDTO
from utils.dependencies import CampaignServiceDep
from campaign.schema import SCampaignModel, CampaignDTO
from campaign.service import CampaignService

router = APIRouter()


@router.post("/", status_code=201)
async def create_campaign(
    data: SCampaignModel,
    service: CampaignService = CampaignServiceDep,
) -> CampaignDTO:
    return await service.create(data)


@router.get("/")
async def get_campaigns(
    service: CampaignService = CampaignServiceDep,
) -> list[CampaignDTO]:
    return await service.get_all()


@router.get("/{campaign_id}/events")
async def get_campaign_events(
    campaign_id: int,
    service: CampaignService = CampaignServiceDep,
) -> list[EventDTO]:
    return await service.get_campaign_events(campaign_id)
