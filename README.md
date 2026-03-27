# PTS + Odoo 19 Integration

This workspace contains:

- `backend/`: FastAPI backend that connects to the remote PTS device via jsonPTS.
- `odoo_pts_bridge/`: Odoo 19 module for Odoo.sh to display status and trigger sync.

## Python version
- Required: Python `3.10+`
- Recommended: Python `3.10.x` (validated in this workspace)

## Backend run
- Configure `backend/.env` from `backend/.env.example`.
- Install requirements and run uvicorn:
  - `pip install -r backend/requirements.txt`
  - `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` (from `backend/`)

## Automated deploy/start
- Windows: `scripts/deploy_and_start.ps1`
- Linux/macOS: `scripts/deploy_and_start.sh`

## Odoo module install
- Add `odoo_pts_bridge` to your custom addons repository.
- Update apps list and install **PTS Backend Bridge**.
- Configure backend URL and credentials in **PTS Integration > Backend Settings**.

## Full guide
- See `USAGE_GUIDE.md` for complete setup, operation, and testing steps.
