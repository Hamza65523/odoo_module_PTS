from odoo import fields, models


class PtsStatusSnapshot(models.Model):
    _name = "pts.status.snapshot"
    _description = "PTS Status Snapshot"
    _order = "create_date desc"

    config_id = fields.Many2one("pts.backend.config", required=True, ondelete="cascade")
    backend_connected = fields.Boolean()
    device_connected = fields.Boolean()
