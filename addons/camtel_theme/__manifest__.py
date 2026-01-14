# -*- coding: utf-8 -*-
{
    "name": "CAMTEL Theme",
    "version": "1.1",
    "summary": "Custom CAMTEL theme with Camtel_SMS branding",
    "description": """
        Custom theme module for CAMTEL that provides:
        - Blue buttons with white text
        - Removal of Manage Databases option from login page
        - Changes all "Odoo" references to "Camtel_SMS" in page titles and branding
        - Custom page title service to display "Camtel_SMS" instead of "Odoo"
        - Updated footer and brand promotion messages
    """,
    "author": "CAMTEL",
    "website": "https://www.camtel.cm",
    "category": "Theme",
    "depends": ["web", "auth_signup"],
    "data": [
        "views/webclient_templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "camtel_theme/static/src/scss/login_theme.scss",
            "camtel_theme/static/src/js/title_service.js",
        ],
        "web.assets_common": [
            "camtel_theme/static/src/scss/login_theme.scss",
        ],
        "web.assets_backend": [
            "camtel_theme/static/src/js/title_service.js",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
    "license": "LGPL-3",
}
