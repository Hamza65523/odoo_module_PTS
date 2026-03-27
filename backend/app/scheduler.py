from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.core.config import get_settings
from app.db.session import SessionLocal
from app.services.pts_client import PTSClient
from app.services.status_service import StatusService

scheduler = AsyncIOScheduler()


async def poll_device_status() -> None:
    db = SessionLocal()
    client = PTSClient()
    try:
        service = StatusService(db, client)
        await service.refresh_device_status()
    finally:
        db.close()
        await client.close()


def start_scheduler() -> None:
    settings = get_settings()
    scheduler.add_job(poll_device_status, "interval", seconds=settings.poll_interval_seconds, id="poll_status")
    scheduler.start()


def stop_scheduler() -> None:
    if scheduler.running:
        scheduler.shutdown(wait=False)
