# -*- coding: utf-8 -*-
import odoo
from odoo import http
from odoo.addons.web.controllers.database import Database
from odoo.tools import file_open
from odoo.addons.base.models.ir_qweb import render as qweb_render
from lxml import html


class CamtelDatabase(Database):
    """Override Database controller to use Camtel_SMS branded templates"""

    def _render_template(self, **d):
        d.setdefault('manage', True)
        d['insecure'] = odoo.tools.config.verify_admin_password('admin')
        d['list_db'] = odoo.tools.config['list_db']
        d['langs'] = odoo.service.db.exp_list_lang()
        d['countries'] = odoo.service.db.exp_list_countries()
        from odoo.addons.web.controllers.database import DBNAME_PATTERN
        d['pattern'] = DBNAME_PATTERN
        
        # databases list
        try:
            d['databases'] = http.db_list()
            d['incompatible_databases'] = odoo.service.db.list_db_incompatible(d['databases'])
        except odoo.exceptions.AccessDenied:
            d['databases'] = [http.request.db] if http.request.db else []

        templates = {}

        # Use custom Camtel_SMS branded templates
        try:
            with file_open("camtel_theme/static/src/public/database_manager.qweb.html", "r") as fd:
                templates['database_manager'] = fd.read()
        except FileNotFoundError:
            # Fallback to default template if custom not found
            with file_open("web/static/src/public/database_manager.qweb.html", "r") as fd:
                templates['database_manager'] = fd.read()
        
        with file_open("web/static/src/public/database_manager.master_input.qweb.html", "r") as fd:
            templates['master_input'] = fd.read()
        with file_open("web/static/src/public/database_manager.create_form.qweb.html", "r") as fd:
            templates['create_form'] = fd.read()

        def load(template_name):
            # Handle None or missing template names by returning database_manager
            if template_name is None or template_name not in templates:
                template_name = 'database_manager'
            fromstring = html.document_fromstring if template_name == 'database_manager' else html.fragment_fromstring
            return (fromstring(templates[template_name]), template_name)

        return qweb_render('database_manager', d, load)
