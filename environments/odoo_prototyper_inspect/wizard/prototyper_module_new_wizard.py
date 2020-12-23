# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class PrototyperModuleNewWizard(models.TransientModel):
    _name = 'prototyper.module.new.wizard'
    _description = '创建模块向导'

    project_id = fields.Many2one(
        string='项目',
        comodel_name='prototyper.project',
        ondelete='set null',
        required=False)
    name = fields.Char(string='模块名称')


    def button_new(self):
        project_id = self.project_id.id
        self.env['prototyper.ir.module.module'].create({
            'name': self.name, 'project_id': project_id
        })
        return {'type': 'ir.actions.client', 'tag': 'reload'}
