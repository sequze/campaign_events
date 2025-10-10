from utils.dependencies import get_event_service


async def process_all_pending_events():
    event_service = get_event_service()
    await event_service.mark_all_pending_events_completed()


async def generate_random_event(id):
    event_service = get_event_service()
    await event_service.create_random_event(id)
