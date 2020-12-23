# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class PrototyperModuleReverserWizard(models.TransientModel):
    _name = 'prototyper.module.reverser.wizard'
    _description = '模块逆向向导'

    project_id = fields.Many2one(
        string='项目',
        comodel_name='prototyper.project',
        ondelete='set null',
        required=False)
    module_path = fields.Char(
        string='模块路径',
        required=True,
        default='/home/odoo/odoo-13/odoo_addons_boss/')

    def button_module_reverser(self):
        module_path = self.module_path
        project_id = self.project_id.id
        self.env['prototyper.module.reverser'].action_module_reverser(module_path, project_id)
        return {'type': 'ir.actions.client', 'tag': 'reload'}

    @api.onchange('project_id')
    def _onchange_project_id(self):
        if self.project_id.name == '社区版':
            self.module_path = '/home/odoo/odoo-13/addons/'
        elif self.project_id.name == '企业版':
            self.module_path = '/home/odoo/odoo-13/enterprise/'
        else:
            self.module_path = '/home/odoo/odoo-13/odoo_addons_boss/'
