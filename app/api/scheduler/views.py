from fastapi import APIRouter
from scheduler_manager import scheduler_manager

router = APIRouter()


@router.post("/start")
async def start_scheduler():
    result = await scheduler_manager.start()
    return result


@router.post("/stop")
async def stop_scheduler():
    result = await scheduler_manager.stop()
    return result


@router.get("/status")
async def scheduler_status():
    return scheduler_manager.status()
