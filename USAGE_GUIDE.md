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

## 4) Install Odoo module (Odoo.sh)
1. Push `odoo_pts_bridge` into custom addons repository.
2. Update Apps List in Odoo.
3. Install **PTS Backend Bridge**.
4. Open **PTS Integration > Backend Settings** and create a record:
   - backend URL
   - username/password
   - API key (optional)
   - grade id mapping for petrol/diesel/LPG

## 5) How to use in Odoo
- **Get Token**: auth against backend.
- **Sync Status**: updates `backend_connected` and `device_connected`.
- **Fetch Fuel Prices**: reads prices from backend/PTS into Odoo fields.
- **Update Fuel Prices**: sends edited petrol/diesel/LPG prices to PTS through backend.
- **Fetch All Values**: pulls status, fuel prices, pumps, probes, transactions and stores JSON in `all_values_json`.

## 6) API test quick checks
1. `GET /health`
2. `POST /api/v1/auth/token`
3. `GET /api/v1/status/backend`
4. `GET /api/v1/status/device`
5. `GET /api/v1/fuel-prices`
6. `PUT /api/v1/fuel-prices`

See details in `backend/docs/API.md`.

## 7) Why only some PDF APIs were implemented first
The PDF contains a very large protocol surface. The first delivery intentionally implemented a production-safe MVP:
- core connectivity and status
- selected operations
- stable API skeleton + Odoo integration

This reduces risk and allows validation with your real remote device before enabling many control/reporting endpoints. The architecture is already modular, so additional PDF endpoints can now be added incrementally.

## 8) Recommended test flow with your real device
1. Verify backend `GET /health`.
2. Verify `GET /api/v1/status/device` becomes connected.
3. Fetch fuel prices in Odoo.
4. Update one price in Odoo and confirm on device side.
5. Run `Fetch All Values` and verify JSON payload in Odoo.
6. Enable cron sync and monitor status history.
