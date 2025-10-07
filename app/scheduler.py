import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from core.config import settings
from core.db import db_helper
from utils.dependencies import get_campaign_service
from utils.helpers import generate_random_event, process_all_pending_events


logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format,
)

scheduler = AsyncIOScheduler()


async def start_scheduler():
    campaign_service = get_campaign_service()
    campaign_id = await campaign_service.get_or_create_active_campaign()

    scheduler.add_job(
        generate_random_event,
        args=(campaign_id,),
        trigger=IntervalTrigger(seconds=5),
        id="generate_random_event",
        replace_existing=True,
    )

    scheduler.add_job(
        process_all_pending_events,
        trigger=IntervalTrigger(minutes=2),
        id="process_all_pending_events",
        replace_existing=True,
    )

    scheduler.start()
    logging.info("APScheduler started")

    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logging.info("Stopping scheduler")
        scheduler.shutdown()
        await db_helper.dispose()
        logging.info("Scheduler stopped")


if __name__ == "__main__":
    asyncio.run(start_scheduler())
