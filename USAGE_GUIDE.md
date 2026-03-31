# PTS + Odoo System Guide

## Python requirement
- **Target / validated:** Python **3.11.9**
- **Supported line:** Python **3.11.x**
- Check your version:
  - Windows: `python --version`
  - Linux/macOS: `python3 --version`
- The repo root includes `.python-version` (`3.11.9`) for pyenv and similar tools.

## 1) What is implemented
- Local Python backend (`backend/`) that talks to PTS controller with jsonPTS.
- Odoo 19 module (`odoo_pts_bridge/`) for:
  - backend/device status indicators
  - fuel price retrieval/update (petrol, diesel, LPG)
  - retrieve all major values into Odoo (`all_values_json`)

## 2) One-command deployment

### Windows (PowerShell)
```powershell
cd c:\Users\INTEL\Music\app\odoo\odoo_module
powershell -ExecutionPolicy Bypass -File .\scripts\deploy_and_start.ps1
```

### Linux/macOS
```bash
cd /path/to/odoo_module
chmod +x ./scripts/deploy_and_start.sh
./scripts/deploy_and_start.sh .
```

This will:
- create virtual env
- install dependencies
- create `.env` from `.env.example` if missing
- start backend service

## 3) Backend configuration
Edit `backend/.env`:
- `PTS_BASE_URL` (example: `https://<device-ip>/jsonPTS`)
- `PTS_USERNAME`
- `PTS_PASSWORD`
- `PTS_AUTH_MODE` — must match the PTS controller (per documentation: DIP switch 2 **OFF** = **Digest**, **ON** = **Basic**). If this is wrong you will see **HTTP 401** on every call to the device.
- `PTS_VERIFY_SSL` (`false` when using self-signed cert in test)
- `API_KEY`
- `JWT_SECRET_KEY`
- `CORS_ORIGINS` (comma-separated list of allowed browser origins, or leave empty to allow all `*`)

### Understanding status endpoints
- `GET /api/v1/status/backend` — only confirms **this FastAPI service** is up. It does **not** call the PTS device. The `message` field is always a short operational note, not a PTS error.
- `GET /api/v1/status/device` — calls the PTS (`GetDateTime`). If you get **401 Unauthorized** here, fix `PTS_USERNAME`, `PTS_PASSWORD`, and `PTS_AUTH_MODE` in `backend/.env`, then restart the backend.

### Troubleshooting PTS 401 Unauthorized
1. Confirm URL: `https://<ip>/jsonPTS` (or `http://` if HTTPS is disabled on the controller).
2. Set `PTS_AUTH_MODE=digest` or `basic` to match DIP switch 2.
3. Verify username/password in the PTS user configuration.
4. Restart the backend after changing `.env`.

## 4) How Odoo reaches the backend (important)

Calls from Odoo to the backend are made **from the Odoo server** (Python `requests`), not from your browser.

| Where Odoo runs | What to put in **Backend URL** |
|-----------------|--------------------------------|
| **Odoo.sh** (cloud) | A **public URL** that forwards to your laptop, e.g. **ngrok**, **Cloudflare Tunnel**, or a VPS where the backend runs. `http://localhost:8000` will **not** work from Odoo.sh. |
| **Odoo on the same PC** as the backend | `http://127.0.0.1:8000` |
| **Odoo in Docker on the same host** | Often `http://host.docker.internal:8000` (Docker Desktop) or the host LAN IP, e.g. `http://192.168.1.10:8000` |

**Expose local backend quickly (example — ngrok):**

1. Start the backend on port 8000.
2. Run: `ngrok http 8000` (install ngrok from [ngrok.com](https://ngrok.com)).
3. Copy the HTTPS forwarding URL (e.g. `https://abc123.ngrok-free.app`).
4. In Odoo **Backend URL**, use that value **with no trailing slash** (e.g. `https://abc123.ngrok-free.app`).

**CORS** in `backend/.env` only affects **browser** calls. Odoo server-side HTTP does not use CORS, so you can leave `CORS_ORIGINS` empty for Odoo-only integration.

## 5) Install Odoo module (Odoo.sh or local)

1. Add the folder `odoo_pts_bridge` to your **custom addons** path (same Git repo Odoo.sh builds from, or your local `addons` path).
2. **Update Apps List**, remove **Apps** filter, search **PTS Backend Bridge**, **Install**.
3. Open **PTS Integration → Backend Settings** and create **one** configuration record.

## 6) Backend Settings — exact fields

| Field | What to enter |
|-------|----------------|
| **Name** | Any label, e.g. `Production PTS` |
| **Backend URL** | Public or reachable base URL, e.g. `https://your-tunnel.example` or `http://192.168.1.10:8000` — **no** `/api/v1` suffix |
| **Username** | Must match **`PTS_USERNAME`** in `backend/.env` (the backend’s `/api/v1/auth/token` checks **these same** credentials — they are not separate “Odoo users”). |
| **Password** | Must match **`PTS_PASSWORD`** in `backend/.env` |
| **API key** | Same value as **`API_KEY`** in `backend/.env` (recommended). The module sends `Authorization: Bearer …` and `X-API-Key` when this is filled; either auth mode is accepted by the backend. |
| **Petrol / Diesel / LPG grade ID** | Defaults `1`, `2`, `3` — adjust if your PTS uses different `FuelGradeId` values (see PTS or `GetFuelGradesConfiguration`). |

After saving, use the form buttons in this order for a first test:

1. **Get Token** — should succeed without error (if this fails, URL, username, password, or network path is wrong).
2. **Sync Status** — should set **Backend connected** / **Device connected** if the backend can reach the PTS.
3. **Fetch Fuel Prices** — fills **Petrol / Diesel / LPG** price fields from `GET /api/v1/fuel-prices`.
4. **Fetch All Values** — fills **All Retrieved Values** with a large JSON snapshot.

**JWT expiry:** The token expires after `JWT_EXPIRE_MINUTES` (default 60) in `.env`. If API calls start failing with 401, click **Get Token** again.

## 7) How to use in Odoo (buttons)

- **Get Token** — obtain JWT from `POST /api/v1/auth/token`.
- **Sync Status** — `GET` status/backend and status/device; updates flags and appends **Status History**.
- **Fetch Fuel Prices** — reads prices into Odoo fields.
- **Update Fuel Prices** — `PUT` edited prices to the backend (global fuel-grade prices).
- **Fetch All Values** — status, fuel prices, pumps, probes, transactions → `all_values_json`.

Scheduled job **PTS Status Sync** (cron) runs **Sync Status** every minute for active configs; it uses the stored token — refresh the token periodically or increase `JWT_EXPIRE_MINUTES` if cron keeps failing after an hour.

## 8) API test quick checks (curl / browser)
1. `GET /health`
2. `POST /api/v1/auth/token`
3. `GET /api/v1/status/backend`
4. `GET /api/v1/status/device`
5. `GET /api/v1/fuel-prices`
6. `PUT /api/v1/fuel-prices`

See details in `backend/docs/API.md`.

## 9) Why only some PDF APIs were implemented first
The PDF contains a very large protocol surface. The first delivery intentionally implemented a production-safe MVP:
- core connectivity and status
- selected operations
- stable API skeleton + Odoo integration

This reduces risk and allows validation with your real remote device before enabling many control/reporting endpoints. The architecture is already modular, so additional PDF endpoints can now be added incrementally.

## 10) Recommended test flow with your real device
1. Verify backend `GET /health`.
2. Verify `GET /api/v1/status/device` becomes connected.
3. Fetch fuel prices in Odoo.
4. Update one price in Odoo and confirm on device side.
5. Run `Fetch All Values` and verify JSON payload in Odoo.
6. Enable cron sync and monitor status history.
