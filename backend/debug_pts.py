"""Quick diagnostic: test PTS Digest auth (manual + httpx built-in)."""

import asyncio
import hashlib
import json
import os
import re
import ssl
import httpx

PTS_URL = "https://192.168.1.117/jsonPTS"
USERNAME = "admin"
PASSWORD = "admin"

PAYLOAD = {
    "Protocol": "jsonPTS",
    "Packets": [{"Id": 1, "Type": "GetDateTime", "Data": {}}],
}


def parse_challenge(www_auth: str) -> dict:
    def _v(key):
        m = re.search(rf'{key}="?([^",]+)"?', www_auth, re.IGNORECASE)
        return m.group(1) if m else ""
    return {"realm": _v("realm"), "nonce": _v("nonce"), "qop": _v("qop") or "auth", "opaque": _v("opaque")}


def build_digest_header(challenge: dict, nc: int = 1) -> str:
    nc_str = f"{nc:08x}"
    cnonce = hashlib.md5(os.urandom(16)).hexdigest()[:16]
    realm = challenge["realm"]
    nonce = challenge["nonce"]
    qop = challenge["qop"].split(",")[0].strip()
    ha1 = hashlib.md5(f"{USERNAME}:{realm}:{PASSWORD}".encode()).hexdigest()
    ha2 = hashlib.md5(f"POST:/jsonPTS".encode()).hexdigest()
    response = hashlib.md5(f"{ha1}:{nonce}:{nc_str}:{cnonce}:{qop}:{ha2}".encode()).hexdigest()
    parts = [
        f'username="{USERNAME}"', f'realm="{realm}"', f'nonce="{nonce}"',
        f'uri="/jsonPTS"', f'response="{response}"', f"qop={qop}",
        f"nc={nc_str}", f'cnonce="{cnonce}"',
    ]
    if challenge["opaque"]:
        parts.append(f'opaque="{challenge["opaque"]}"')
    return "Digest " + ", ".join(parts)


async def main():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    body = json.dumps(PAYLOAD).encode("utf-8")
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/json; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
    }

    async with httpx.AsyncClient(verify=ctx, timeout=15) as client:
        # Step 1: get challenge
        print("=== Step 1: POST without auth (expect 401) ===")
        try:
            r1 = await client.post(PTS_URL, content=body, headers=headers)
            print(f"  Status: {r1.status_code}")
            www_auth = r1.headers.get("www-authenticate", "")
            print(f"  WWW-Authenticate: {www_auth}")
            if r1.status_code != 401:
                print(f"  Body: {r1.text[:500]}")
                return
        except Exception as e:
            print(f"  FAILED: {type(e).__name__}: {e}")
            return

        # Step 2: compute digest and retry
        challenge = parse_challenge(www_auth)
        print(f"\n  Parsed: realm={challenge['realm']}, nonce={challenge['nonce']}, qop={challenge['qop']}")
        auth_header = build_digest_header(challenge)
        print(f"  Auth header: {auth_header[:120]}...")

        print("\n=== Step 2: POST with manual Digest auth ===")
        try:
            r2 = await client.post(PTS_URL, content=body, headers={**headers, "Authorization": auth_header})
            print(f"  Status: {r2.status_code}")
            print(f"  Body: {r2.text[:1000]}")
        except Exception as e:
            print(f"  FAILED: {type(e).__name__}: {e}")

        # Step 3: try httpx built-in DigestAuth for comparison
        print("\n=== Step 3: httpx built-in DigestAuth ===")
        try:
            r3 = await client.post(PTS_URL, content=body, headers=headers, auth=httpx.DigestAuth(USERNAME, PASSWORD))
            print(f"  Status: {r3.status_code}")
            print(f"  Body: {r3.text[:500]}")
        except Exception as e:
            print(f"  FAILED: {type(e).__name__}: {e}")


asyncio.run(main())
