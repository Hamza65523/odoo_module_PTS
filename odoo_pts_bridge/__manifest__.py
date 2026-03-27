{
    "name": "PTS Backend Bridge",
    "version": "19.0.1.0.0",
    "summary": "Integrate Odoo with local PTS backend",
    "depends": ["base", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_cron_data.xml",
        "views/pts_backend_views.xml",
        "views/pts_dashboard_views.xml",
        "views/menu_views.xml",
    ],
    "application": True,
    "installable": True,
    "license": "LGPL-3",
}
