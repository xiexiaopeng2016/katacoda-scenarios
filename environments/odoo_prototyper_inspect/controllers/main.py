# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import http
from odoo.http import request
import logging
import json

_logger = logging.getLogger(__name__)


class ModuleInspect(http.Controller):
    @http.route('/module/inspect', type='http', auth='none')
    def module_inspect(self, module_name, **kwargs):
        module_path = '/opt/code/odoo-11.0/addons/%s' % module_name
        result = request.env['prototyper.module.inspect'].parse_module_source(module_path)
        return json.dumps(result)
