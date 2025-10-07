from fastapi import Depends

from campaign.service import CampaignService
from core.db.uow import UnitOfWork
from core.db import db_helper
from events.service import EventService


def unit_of_work() -> UnitOfWork:
    return UnitOfWork(db_helper.session_factory)


def get_campaign_service() -> CampaignService:
    return CampaignService(unit_of_work())


def get_event_service() -> EventService:
    return EventService(unit_of_work())


CampaignServiceDep = Depends(get_campaign_service)
EventServiceDep = Depends(get_event_service)
