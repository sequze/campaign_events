from fastapi import APIRouter
from .events import router as events_router
from .campaign import router as campaign_router
from .scheduler import router as scheduler_router
from core.config import settings

router = APIRouter()

router.include_router(
    events_router,
    prefix=settings.api_prefix.events,
    tags=["events"],
)

router.include_router(
    campaign_router,
    prefix=settings.api_prefix.campaigns,
    tags=["campaign"],
)

router.include_router(
    scheduler_router,
    prefix=settings.api_prefix.scheduler,
    tags=["scheduler"],
)
