from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import SystemStatus
from app.services.pts_client import PTSClient, PTSClientError

logger = logging.getLogger(__name__)


class StatusService:
    def __init__(self, db: Session, pts_client: PTSClient | None = None):
        self.db = db
        self.pts_client = pts_client

    def _get_or_create_status(self) -> SystemStatus:
        status = self.db.scalar(select(SystemStatus).where(SystemStatus.id == 1))
        if status is None:
            status = SystemStatus(id=1, backend_connected=True, device_connected=False)
            self.db.add(status)
            self.db.commit()
            self.db.refresh(status)
        return status

    async def refresh_device_status(self) -> SystemStatus:
        if self.pts_client is None:
            raise RuntimeError("PTS client is required for device status refresh")
        status = self._get_or_create_status()
        status.last_backend_check = datetime.now(timezone.utc)
        status.backend_connected = True
        try:
            await self.pts_client.send("GetDateTime")
            status.device_connected = True
            status.message = "Device reachable"
            status.last_device_check = datetime.now(timezone.utc)
        except PTSClientError as exc:
            status.device_connected = False
            status.message = str(exc)
            status.last_device_check = datetime.now(timezone.utc)
        self.db.add(status)
        self.db.commit()
        self.db.refresh(status)
        return status

    def touch_backend_check(self) -> SystemStatus:
        """Record that something successfully called the backend API (not PTS)."""
        status = self._get_or_create_status()
        status.backend_connected = True
        status.last_backend_check = datetime.now(timezone.utc)
        self.db.add(status)
        self.db.commit()
        self.db.refresh(status)
        return status

    def current_status(self) -> SystemStatus:
        return self._get_or_create_status()

    async def get_pumps(self) -> list[dict[str, Any]]:
        if self.pts_client is None:
            raise RuntimeError("PTS client is required")
        result = await self.pts_client.send("PumpGetStatus", {"Pump": 0})
        return result.get("Packets", [])

    async def get_probes(self) -> list[dict[str, Any]]:
        if self.pts_client is None:
            raise RuntimeError("PTS client is required")
        result = await self.pts_client.send("ProbeGetMeasurements", {"Probe": 1})
        return result.get("Packets", [])

    async def get_transactions(self) -> list[dict[str, Any]]:
        if self.pts_client is None:
            raise RuntimeError("PTS client is required")
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        result = await self.pts_client.send(
            "ReportGetPumpTransactions",
            {"Pump": 0, "DateTimeStart": now, "DateTimeEnd": now},
        )
        return result.get("Packets", [])

    async def get_fuel_grades(self) -> list[dict[str, Any]]:
        if self.pts_client is None:
            raise RuntimeError("PTS client is required")
        result = await self.pts_client.send("GetFuelGradesConfiguration")
        packets = result.get("Packets", [])
        if not packets:
            return []
        data = packets[0].get("Data", {})
        return data.get("FuelGrades", [])

    async def set_fuel_grades_prices(self, prices: list[dict[str, Any]]) -> dict[str, Any]:
        if self.pts_client is None:
            raise RuntimeError("PTS client is required")
        payload = {"FuelGradesPrices": prices}
        return await self.pts_client.send("SetFuelGradesPrices", payload)

    # ---- Per-pump prices (PumpGetPrices / PumpSetPrices) ---------------

    async def pump_set_prices(self, pump: int, prices: list[float]) -> dict[str, Any]:
        """Send PumpSetPrices to set nozzle prices on a specific pump."""
        if self.pts_client is None:
            raise RuntimeError("PTS client is required")
        return await self.pts_client.send(
            "PumpSetPrices", {"Pump": pump, "Prices": prices}
        )

    async def pump_get_prices(
        self, pump: int, *, retries: int = 6, interval: float = 1.0
    ) -> dict[str, Any]:
        """Request prices and poll PumpGetStatus until PumpPrices is returned.

        PumpGetPrices is async on the PTS side: it returns OK immediately,
        then the actual PumpPrices data appears in a subsequent PumpGetStatus
        response.  We poll up to `retries` times with `interval` seconds between.
        """
        if self.pts_client is None:
            raise RuntimeError("PTS client is required")

        await self.pts_client.send("PumpGetPrices", {"Pump": pump})

        for _ in range(retries):
            await asyncio.sleep(interval)
            result = await self.pts_client.send("PumpGetStatus", {"Pump": pump})
            for pkt in result.get("Packets", []):
                if pkt.get("Type") == "PumpPrices":
                    return pkt.get("Data", {})

        raise PTSClientError(
            f"PumpPrices response not received for pump {pump} after {retries} polls"
        )
