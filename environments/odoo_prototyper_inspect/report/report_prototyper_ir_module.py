# -*- coding: utf-8 -*-
# © 2016 Yopark Corp (http://www.yopark.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import odoo
from odoo.addons.report_docx.report.report_docx import ReportDocx


class ReportPrototyperIrModule(ReportDocx):
    def generate_docx_data(self, cr, uid, ids, data, context):
        renting_in_order_id = data['renting_in_order']

        convert_data = []
        env = odoo.api.Environment(cr, uid, context)

        module = env['renting.in.order'].browse(
            renting_in_order_id)

        convert_data.append(self._obj2dict(module, data))

        return convert_data

    def _obj2dict(self, obj, data):
        memberlist = [m for m in dir(obj)]
        context = {}
        for m in memberlist:
            if m[0] != "_" and not callable(m):
                context[m] = getattr(obj, m)

        return context

ReportPrototyperIrModule(
    'report.prototyper.ir.module', 'report.docx.template',
)
