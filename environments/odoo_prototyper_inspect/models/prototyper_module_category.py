# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, api, fields


class PrototyperModuleCategory(models.Model):
    _name = 'prototyper.ir.module.category'
    _description = '模块类别'
    _order = 'name'

    name = fields.Char(string='名称', required=True)
    tech_name = fields.Char(string='技术名称', required=False)
    parent_id = fields.Many2one(
        comodel_name='prototyper.ir.module.category',
        string='上级应用',
        index=True)
    description = fields.Text(string='说明')
    sequence = fields.Integer(string='序号')
    visible = fields.Boolean(string='可见', default=True)
