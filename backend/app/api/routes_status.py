from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_subject_or_api_key
from app.db.session import get_db
from app.schemas.status import BackendStatus, DeviceStatus
from app.services.pts_client import PTSClient
from app.services.status_service import StatusService

router = APIRouter(prefix="/status", tags=["status"])


@router.get("/backend", response_model=BackendStatus)
async def backend_status(
    _subject: str = Depends(get_subject_or_api_key), db: Session = Depends(get_db)
) -> BackendStatus:
    """Reports only that this FastAPI service is reachable (not PTS connectivity).

    PTS errors from the scheduler or `/status/device` are stored in the DB but must
    not appear here, or clients confuse \"backend\" with \"device\".
    """
    service = StatusService(db, None)
    service.touch_backend_check()
    return BackendStatus(
        backend_connected=True,
        checked_at=datetime.now(timezone.utc),
        message="Backend API is running",
    )


@router.get("/device", response_model=DeviceStatus)
async def device_status(
    _subject: str = Depends(get_subject_or_api_key), db: Session = Depends(get_db)
) -> DeviceStatus:
    client = PTSClient()
    service = StatusService(db, client)
    current = await service.refresh_device_status()
    await client.close()
    return DeviceStatus(
        device_connected=current.device_connected,
        checked_at=current.last_device_check,
        message=current.message,
    )
