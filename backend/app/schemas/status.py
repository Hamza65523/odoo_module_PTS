from datetime import datetime

from pydantic import BaseModel


class BackendStatus(BaseModel):
    backend_connected: bool
    checked_at: datetime | None = None
    message: str | None = None


class DeviceStatus(BaseModel):
    device_connected: bool
    checked_at: datetime | None = None
    message: str | None = None
