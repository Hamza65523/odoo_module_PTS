import logging
import json

import requests
from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class PtsBackendConfig(models.Model):
    _name = "pts.backend.config"
    _description = "PTS Backend Configuration"

    name = fields.Char(default="Default Backend", required=True)
    active = fields.Boolean(default=True)
    backend_url = fields.Char(required=True, help="Example: https://backend.example.com")
    username = fields.Char(required=True)
    password = fields.Char(required=True)
    api_key = fields.Char()
    token = fields.Char(readonly=True)
    token_expiry = fields.Datetime(readonly=True)
    backend_connected = fields.Boolean(readonly=True)
    device_connected = fields.Boolean(readonly=True)
    last_sync_at = fields.Datetime(readonly=True)
    last_error = fields.Text(readonly=True)
    petrol_grade_id = fields.Integer(default=1, required=True)
    diesel_grade_id = fields.Integer(default=2, required=True)
    lpg_grade_id = fields.Integer(default=3, required=True)
    petrol_price = fields.Float(digits=(16, 3))
    diesel_price = fields.Float(digits=(16, 3))
    lpg_price = fields.Float(digits=(16, 3))
    all_values_json = fields.Text(readonly=True)

    def _headers(self):
        self.ensure_one()
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        return headers

    def action_get_token(self):
        self.ensure_one()
        endpoint = f"{self.backend_url.rstrip('/')}/api/v1/auth/token"
        try:
            response = requests.post(
                endpoint,
                json={"username": self.username, "password": self.password},
                timeout=15,
            )
            response.raise_for_status()
            payload = response.json()
            self.write({"token": payload.get("access_token")})
        except requests.RequestException as exc:
            raise UserError(_("Authentication failed: %s") % exc) from exc

    def _fetch_status(self):
        self.ensure_one()
        headers = self._headers()
        backend_resp = requests.get(
            f"{self.backend_url.rstrip('/')}/api/v1/status/backend", headers=headers, timeout=15
        )
        device_resp = requests.get(
            f"{self.backend_url.rstrip('/')}/api/v1/status/device", headers=headers, timeout=15
        )
        backend_resp.raise_for_status()
        device_resp.raise_for_status()
        return backend_resp.json(), device_resp.json()

    def _fetch_fuel_prices(self):
        self.ensure_one()
        headers = self._headers()
        resp = requests.get(f"{self.backend_url.rstrip('/')}/api/v1/fuel-prices", headers=headers, timeout=20)
        resp.raise_for_status()
        return resp.json().get("items", [])

    def action_sync_status(self):
        self.ensure_one()
        if not self.token:
            self.action_get_token()
        try:
            backend_payload, device_payload = self._fetch_status()
            self.write(
                {
                    "backend_connected": backend_payload.get("backend_connected", False),
                    "device_connected": device_payload.get("device_connected", False),
                    "last_sync_at": fields.Datetime.now(),
                    "last_error": False,
                }
            )
            self.env["pts.status.snapshot"].create(
                {
                    "config_id": self.id,
                    "backend_connected": self.backend_connected,
                    "device_connected": self.device_connected,
                }
            )
        except requests.RequestException as exc:
            _logger.exception("PTS sync failed")
            self.write({"last_error": str(exc), "last_sync_at": fields.Datetime.now()})

    def action_fetch_fuel_prices(self):
        self.ensure_one()
        if not self.token:
            self.action_get_token()
        try:
            items = self._fetch_fuel_prices()
            price_by_id = {int(item.get("fuel_grade_id")): float(item.get("price", 0.0)) for item in items}
            self.write(
                {
                    "petrol_price": price_by_id.get(self.petrol_grade_id, 0.0),
                    "diesel_price": price_by_id.get(self.diesel_grade_id, 0.0),
                    "lpg_price": price_by_id.get(self.lpg_grade_id, 0.0),
                    "last_error": False,
                }
            )
        except requests.RequestException as exc:
            raise UserError(_("Failed to fetch fuel prices: %s") % exc) from exc

    def action_update_fuel_prices(self):
        self.ensure_one()
        if not self.token:
            self.action_get_token()
        endpoint = f"{self.backend_url.rstrip('/')}/api/v1/fuel-prices"
        payload = {
            "items": [
                {"fuel_grade_id": self.petrol_grade_id, "name": "Petrol", "price": self.petrol_price},
                {"fuel_grade_id": self.diesel_grade_id, "name": "Diesel", "price": self.diesel_price},
                {"fuel_grade_id": self.lpg_grade_id, "name": "LPG", "price": self.lpg_price},
            ]
        }
        try:
            resp = requests.put(endpoint, headers=self._headers(), json=payload, timeout=20)
            resp.raise_for_status()
            self.write({"last_error": False})
        except requests.RequestException as exc:
            raise UserError(_("Failed to update fuel prices: %s") % exc) from exc

    def action_fetch_all_values(self):
        self.ensure_one()
        if not self.token:
            self.action_get_token()
        base = self.backend_url.rstrip("/")
        headers = self._headers()
        try:
            payload = {
                "status_backend": requests.get(f"{base}/api/v1/status/backend", headers=headers, timeout=20).json(),
                "status_device": requests.get(f"{base}/api/v1/status/device", headers=headers, timeout=20).json(),
                "fuel_prices": requests.get(f"{base}/api/v1/fuel-prices", headers=headers, timeout=20).json(),
                "pumps": requests.get(f"{base}/api/v1/pumps", headers=headers, timeout=20).json(),
                "probes": requests.get(f"{base}/api/v1/probes", headers=headers, timeout=20).json(),
                "transactions": requests.get(f"{base}/api/v1/transactions", headers=headers, timeout=20).json(),
            }
            self.write({"all_values_json": json.dumps(payload, indent=2), "last_error": False})
        except requests.RequestException as exc:
            raise UserError(_("Failed to fetch all values: %s") % exc) from exc

    @api.model
    def cron_sync_status(self):
        for config in self.search([("active", "=", True)]):
            config.action_sync_status()
