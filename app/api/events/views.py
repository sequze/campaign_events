from fastapi import APIRouter, HTTPException, status

from utils.dependencies import EventServiceDep
from events.schema import EventDTO, SEventModel
from events.service import EventService, EventExistsError

router = APIRouter()


@router.get("/")
async def get_events(
    service: EventService = EventServiceDep,
) -> list[EventDTO]:
    return await service.get_all()


@router.post("/")
async def create_event(
    data: SEventModel,
    service: EventService = EventServiceDep,
) -> EventDTO:
    try:
        return await service.create(data)
    except EventExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
