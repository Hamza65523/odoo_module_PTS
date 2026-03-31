import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.core.config import get_settings
from app.db.session import SessionLocal
from app.services.pts_client import PTSClient
from app.services.status_service import StatusService

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()


async def poll_device_status() -> None:
    db = SessionLocal()
    client = PTSClient()
    try:
        service = StatusService(db, client)
        await service.refresh_device_status()
    except Exception:
        logger.exception("Scheduler: poll_device_status failed")
    finally:
        db.close()
        try:
            await client.close()
        except Exception:
            pass


def start_scheduler() -> None:
    settings = get_settings()
    scheduler.add_job(
        poll_device_status,
        "interval",
        seconds=settings.poll_interval_seconds,
        id="poll_status",
        max_instances=1,
        misfire_grace_time=30,
    )
    scheduler.start()


def stop_scheduler() -> None:
    if scheduler.running:
        scheduler.shutdown(wait=False)
