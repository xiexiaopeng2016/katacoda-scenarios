# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class PrototyperModelNewWizard(models.TransientModel):
    _name = 'prototyper.model.new.wizard'
    _description = '创建模块向导'

    project_id = fields.Many2one(
        string='项目',
        comodel_name='prototyper.project',
        ondelete='set null',
        required=False)
    module_id = fields.Many2one(
        string='模块',
        comodel_name='prototyper.ir.module.module',
        ondelete='restrict',
        domain="[('project_id','=',project_id)]",
        required=True)
    name = fields.Char(string='模块名称')


    def button_new(self):
        self.env['prototyper.ir.model'].create({
            'name': self.name, 'module_id': self.module_id.id
        })
        return {'type': 'ir.actions.client', 'tag': 'reload'}
