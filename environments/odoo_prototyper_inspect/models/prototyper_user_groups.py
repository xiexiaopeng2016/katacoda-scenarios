# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, api, fields


class PrototyperResGroups(models.Model):
    _name = 'prototyper.res.groups'
    _description = '权限组'

    name = fields.Char(string='名称', required=True)
    tech_name = fields.Char(string='技术名称', required=True)
    comment = fields.Text(string='说明')
    category_id = fields.Many2one(
        string='应用',
        comodel_name='prototyper.ir.module.category',
        index=True)
    color = fields.Integer(string='颜色')
    share = fields.Boolean(string='共享组')
    module_id = fields.Many2one(
        string='模块',
        comodel_name='prototyper.ir.module.module',
        ondelete='restrict')
