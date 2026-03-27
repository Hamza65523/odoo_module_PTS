from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.models import CommandAudit
from app.services.pts_client import PTSClient, PTSClientError

ALLOWED_ACTIONS = {
    "pump_stop": "PumpStop",
    "pump_emergency_stop": "PumpEmergencyStop",
    "pump_authorize": "PumpAuthorize",
    "pump_close_transaction": "PumpCloseTransaction",
}


class CommandService:
    def __init__(self, db: Session, pts_client: PTSClient):
        self.db = db
        self.pts_client = pts_client

    async def execute(self, action: str, payload: dict, requested_by: str) -> dict:
        if action not in ALLOWED_ACTIONS:
            raise ValueError(f"Unsupported action: {action}")

        command_name = ALLOWED_ACTIONS[action]
        audit = CommandAudit(
            command_name=command_name,
            requested_by=requested_by,
            status="started",
            request_payload=payload,
        )
        self.db.add(audit)
        self.db.commit()
        self.db.refresh(audit)

        try:
            response = await self.pts_client.send(command_name, payload)
            audit.status = "success"
            audit.response_payload = response
            self.db.add(audit)
            self.db.commit()
            return response
        except PTSClientError as exc:
            audit.status = "failed"
            audit.error_detail = str(exc)
            self.db.add(audit)
            self.db.commit()
            raise
