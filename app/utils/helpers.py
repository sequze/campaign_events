from utils.dependencies import get_event_service, get_campaign_service

event_service = get_event_service()
campaign_service = get_campaign_service()


async def process_all_pending_events():
    await event_service.mark_all_pending_events_completed()


async def generate_random_event(id):
    await event_service.create_random_event(id)
