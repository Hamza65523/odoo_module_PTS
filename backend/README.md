# PTS Backend Service

Python FastAPI backend for Odoo 19 integration with a remote PTS controller.

## Features
- JWT-based API authentication
- API key guard support
- jsonPTS transport adapter over HTTP/HTTPS
- Hybrid-ready websocket ingest endpoint (`/ws/pts`)
- Status polling scheduler
- Command auditing and status persistence

## Quick Start
1. Create virtualenv and install dependencies:
   - `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and adjust values.
3. Run:
   - `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

## Main API
- `GET /health`
- `POST /api/v1/auth/token`
- `GET /api/v1/status/backend`
- `GET /api/v1/status/device`
- `GET /api/v1/pumps`
- `GET /api/v1/probes`
- `GET /api/v1/transactions`
- `GET /api/v1/fuel-prices`
- `PUT /api/v1/fuel-prices`
- `POST /api/v1/commands/{action}`

## Supported actions
- `pump_stop`
- `pump_emergency_stop`
- `pump_authorize`
- `pump_close_transaction`
