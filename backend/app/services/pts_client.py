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
            except httpx.HTTPStatusError as exc:
                detail = exc.response.text[:500] if exc.response.text else ""
                hint = ""
                if exc.response.status_code == 401:
                    hint = (
                        " Check PTS_USERNAME/PTS_PASSWORD and PTS_AUTH_MODE in backend/.env "
                        "(DIP switch 2 OFF = digest, ON = basic per PTS documentation)."
                    )
                raise PTSClientError(
                    f"PTS HTTP {exc.response.status_code}: {exc}{(' ' + detail) if detail else ''}.{hint}"
                ) from exc
            except httpx.HTTPError as exc:
                raise PTSClientError(f"PTS communication error: {exc}") from exc
        body = response.json()
        self._validate_pts_response(body)
        return body

    def _auth_tuple(self):
        mode = self.settings.pts_auth_mode.lower().strip()
        user = self.settings.pts_username
        password = self.settings.pts_password
        if mode == "digest":
            return httpx.DigestAuth(user, password)
        # basic (DIP switch 2 ON) or default
        return (user, password)

    @staticmethod
    def _validate_pts_response(body: dict[str, Any]) -> None:
        if "Packets" not in body:
            raise PTSClientError("Invalid PTS response: missing Packets")
        packets = body.get("Packets") or []
        if packets and packets[0].get("Type") == "Error":
            msg = packets[0].get("Message", "Unknown PTS error")
            raise PTSClientError(f"PTS error: {msg}")
