# PTS + Odoo 19 Integration

This workspace contains:

- `backend/`: FastAPI backend that connects to the remote PTS device via jsonPTS.
- `odoo_pts_bridge/`: Odoo 19 module for Odoo.sh to display status and trigger sync.

## Python version
- **Target / validated:** Python **3.11.9** (use this version for the backend in production and local dev).
- **Supported line:** Python **3.11.x** (other 3.11 patch releases are expected to work).
- Check: `python --version` or `python3 --version`

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
- **Odoo.sh:** the backend must be reachable from the cloud (tunnel/VPS); JWT login uses the same **`PTS_USERNAME` / `PTS_PASSWORD`** as in `backend/.env`. See **sections 4–7** in `USAGE_GUIDE.md`.

## Full guide
- See `USAGE_GUIDE.md` for complete setup, operation, and testing steps.
