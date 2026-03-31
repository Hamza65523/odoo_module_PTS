from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import os
import re
import ssl
from typing import Any

import httpx

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class PTSClientError(Exception):
    pass


class _DigestState:
    """Tracks nonce/nc across requests so we can reuse a server nonce."""

    def __init__(self) -> None:
        self.nonce: str = ""
        self.realm: str = ""
        self.qop: str = ""
        self.opaque: str = ""
        self.nc: int = 0

    def parse_challenge(self, www_authenticate: str) -> None:
        def _val(key: str) -> str:
            m = re.search(rf'{key}="?([^",]+)"?', www_authenticate, re.IGNORECASE)
            return m.group(1) if m else ""

        self.realm = _val("realm")
        self.nonce = _val("nonce")
        self.qop = _val("qop").split(",")[0].strip() if _val("qop") else "auth"
        self.opaque = _val("opaque")
        self.nc = 0

    def build_header(self, method: str, uri: str, username: str, password: str) -> str:
        self.nc += 1
        nc_str = f"{self.nc:08x}"
        cnonce = hashlib.md5(os.urandom(16)).hexdigest()[:16]

        ha1 = hashlib.md5(f"{username}:{self.realm}:{password}".encode()).hexdigest()
        ha2 = hashlib.md5(f"{method}:{uri}".encode()).hexdigest()
        response = hashlib.md5(
            f"{ha1}:{self.nonce}:{nc_str}:{cnonce}:{self.qop}:{ha2}".encode()
        ).hexdigest()

        parts = [
            f'username="{username}"',
            f'realm="{self.realm}"',
            f'nonce="{self.nonce}"',
            f'uri="{uri}"',
            f'response="{response}"',
            f"qop={self.qop}",
            f"nc={nc_str}",
            f'cnonce="{cnonce}"',
        ]
        if self.opaque:
            parts.append(f'opaque="{self.opaque}"')
        return "Digest " + ", ".join(parts)


class PTSClient:
    """HTTP client for the jsonPTS protocol on PTS-2 forecourt controllers."""

    def __init__(self) -> None:
        self.settings = get_settings()

        timeout = httpx.Timeout(connect=5.0, read=10.0, write=5.0, pool=5.0)

        verify: bool | ssl.SSLContext = self.settings.pts_verify_ssl
        if not verify:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            verify = ctx

        self._client = httpx.AsyncClient(verify=verify, timeout=timeout)
        self._lock = asyncio.Lock()
        self._digest = _DigestState()

    async def close(self) -> None:
        await self._client.aclose()

    # ------------------------------------------------------------------
    async def send(
        self,
        packet_type: str,
        data: dict[str, Any] | None = None,
        *,
        packets: list[dict[str, Any]] | None = None,
        validate: bool = True,
    ) -> dict[str, Any]:
        if packets is not None:
            payload: dict[str, Any] = {"Protocol": "jsonPTS", "Packets": packets}
        else:
            payload = {
                "Protocol": "jsonPTS",
                "Packets": [{"Id": 1, "Type": packet_type, "Data": data or {}}],
            }

        async with self._lock:
            try:
                response = await self._post_with_auth(payload)
            except httpx.TimeoutException as exc:
                raise PTSClientError(
                    f"PTS request timed out ({type(exc).__name__}). "
                    f"Verify PTS_BASE_URL ({self.settings.pts_base_url}) is reachable."
                ) from exc
            except httpx.HTTPStatusError as exc:
                detail = exc.response.text[:500] if exc.response.text else ""
                hint = ""
                if exc.response.status_code == 401:
                    hint = (
                        " Check PTS_USERNAME/PTS_PASSWORD and PTS_AUTH_MODE in backend/.env "
                        "(DIP switch 2 OFF = digest, ON = basic per PTS documentation)."
                    )
                raise PTSClientError(
                    f"PTS HTTP {exc.response.status_code}: {exc}"
                    f"{(' ' + detail) if detail else ''}.{hint}"
                ) from exc
            except httpx.HTTPError as exc:
                raise PTSClientError(f"PTS communication error: {exc}") from exc

        body = response.json()
        if validate:
            self._validate_pts_response(body)
        return body

    # ------------------------------------------------------------------
    async def _post_with_auth(self, payload: dict[str, Any]) -> httpx.Response:
        url = self.settings.pts_base_url
        mode = self.settings.pts_auth_mode.lower().strip()
        body_bytes = json.dumps(payload).encode("utf-8")
        base_headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/json; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
        }

        if mode != "digest":
            resp = await self._client.post(
                url,
                content=body_bytes,
                headers=base_headers,
                auth=(self.settings.pts_username, self.settings.pts_password),
            )
            resp.raise_for_status()
            return resp

        uri = "/jsonPTS"
        user = self.settings.pts_username
        pwd = self.settings.pts_password

        if self._digest.nonce:
            headers = {
                **base_headers,
                "Authorization": self._digest.build_header("POST", uri, user, pwd),
            }
            resp = await self._client.post(url, content=body_bytes, headers=headers)
            if resp.status_code != 401:
                resp.raise_for_status()
                return resp
            logger.debug("Cached nonce rejected, re-authenticating")

        resp_challenge = await self._client.post(
            url, content=body_bytes, headers=base_headers
        )
        if resp_challenge.status_code != 401:
            resp_challenge.raise_for_status()
            return resp_challenge

        www_auth = resp_challenge.headers.get("www-authenticate", "")
        if not www_auth:
            raise PTSClientError(
                "PTS returned 401 without WWW-Authenticate header. "
                "Cannot perform Digest authentication."
            )
        logger.debug("Digest challenge: %s", www_auth)
        self._digest.parse_challenge(www_auth)

        headers = {
            **base_headers,
            "Authorization": self._digest.build_header("POST", uri, user, pwd),
        }
        resp = await self._client.post(url, content=body_bytes, headers=headers)
        resp.raise_for_status()
        return resp

    # ------------------------------------------------------------------
    @staticmethod
    def _validate_pts_response(body: dict[str, Any]) -> None:
        if "Packets" not in body:
            raise PTSClientError("Invalid PTS response: missing Packets")
        packets = body.get("Packets") or []
        for pkt in packets:
            if pkt.get("Error"):
                code = pkt.get("Code", "?")
                msg = pkt.get("Message", "Unknown PTS error")
                raise PTSClientError(f"PTS error [{code}]: {msg}")
