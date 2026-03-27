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
    service = StatusService(db, PTSClient())
    current = service.current_status()
    return BackendStatus(
        backend_connected=current.backend_connected,
        checked_at=current.last_backend_check,
        message=current.message,
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
