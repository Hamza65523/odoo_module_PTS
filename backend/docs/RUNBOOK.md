# Operations Runbook

## Prerequisites
- Backend Python **3.11.x**, validated on **3.11.9** (see repository `README.md` and `.python-version`).

## Service restart
- `sudo systemctl restart pts-backend`
- `sudo systemctl status pts-backend`

## Connectivity issue
1. Check backend health: `GET /health`
2. Check device status endpoint.
3. Verify firewall routes to device IP and ports.
4. Validate PTS credentials in `.env`.

## Backup
- Backup DB file (SQLite) or DB dump (PostgreSQL).
- Keep `.env` and encryption key backed up securely.

## Recovery
1. Restore DB and `.env`.
2. Restart service.
3. Run status sync from Odoo UI.
