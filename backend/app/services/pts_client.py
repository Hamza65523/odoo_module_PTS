from __future__ import annotations

import asyncio
from typing import Any

import httpx

from app.core.config import get_settings


class PTSClientError(Exception):
    pass


class PTSClient:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._client = httpx.AsyncClient(verify=self.settings.pts_verify_ssl, timeout=20)
        self._lock = asyncio.Lock()

    async def close(self) -> None:
        await self._client.aclose()

    async def send(self, packet_type: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = {
            "Protocol": "jsonPTS",
            "Packets": [{"Id": 1, "Type": packet_type, "Data": data or {}}],
        }
        auth = self._auth_tuple()
        async with self._lock:
            try:
                response = await self._client.post(self.settings.pts_base_url, json=payload, auth=auth)
                response.raise_for_status()
            except httpx.HTTPError as exc:
                raise PTSClientError(f"PTS communication error: {exc}") from exc
        body = response.json()
        self._validate_pts_response(body)
        return body

    def _auth_tuple(self):
        mode = self.settings.pts_auth_mode.lower()
        if mode not in {"basic", "digest"}:
            return (self.settings.pts_username, self.settings.pts_password)
        return (self.settings.pts_username, self.settings.pts_password)

    @staticmethod
    def _validate_pts_response(body: dict[str, Any]) -> None:
        if "Packets" not in body:
            raise PTSClientError("Invalid PTS response: missing Packets")
        packets = body.get("Packets") or []
        if packets and packets[0].get("Type") == "Error":
            msg = packets[0].get("Message", "Unknown PTS error")
            raise PTSClientError(f"PTS error: {msg}")
