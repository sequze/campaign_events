import logging
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from utils.dependencies import get_campaign_service
from utils.helpers import generate_random_event, process_all_pending_events

scheduler = AsyncIOScheduler()

log = logging.getLogger(__name__)


class SchedulerManager:
    def __init__(self):
        self.scheduler = None
        self.running = False
        self._campaign_id = None
        self.campaign_service = get_campaign_service()

    async def _init_campaign(self):
        self._campaign_id = await self.campaign_service.get_or_create_active_campaign()

    async def start(self):
        if self.running:
            log.info("Scheduler is already running.")
            return {"status": "already running"}

        await self._init_campaign()
        self.scheduler = AsyncIOScheduler()

        self.scheduler.add_job(
            generate_random_event,
            args=(self._campaign_id,),
            trigger=IntervalTrigger(seconds=5),
            id="generate_random_event",
            replace_existing=True,
            next_run_time=datetime.now(),
        )

        self.scheduler.add_job(
            process_all_pending_events,
            trigger=IntervalTrigger(minutes=2),
            id="process_all_pending_events",
            replace_existing=True,
            next_run_time=datetime.now(),
        )

        self.scheduler.start()
        self.running = True
        log.info("Scheduler started")
        return {"status": "started"}

    async def stop(self):
        if not self.running or not self.scheduler:
            log.info("Scheduler is not running.")
            return {"status": "not running"}
        self.scheduler.shutdown(wait=False)
        self.running = False
        log.info("Scheduler stopped")
        return {"status": "stopped"}

    def status(self):
        return {"status": "running" if self.running else "not running"}


scheduler_manager = SchedulerManager()
