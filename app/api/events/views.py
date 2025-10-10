from fastapi import APIRouter

from utils.dependencies import EventServiceDep
from events.schema import EventDTO, SEventModel
from events.service import EventService

router = APIRouter()


@router.get("/")
async def get_events(
    service: EventService = EventServiceDep,
) -> list[EventDTO]:
    return await service.get_all()


@router.post("/", status_code=201)
async def create_event(
    data: SEventModel,
    service: EventService = EventServiceDep,
) -> EventDTO:
    return await service.create(data)
