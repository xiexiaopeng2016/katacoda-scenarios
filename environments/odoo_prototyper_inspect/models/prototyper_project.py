# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, api, fields


class PrototyperProject(models.Model):
    _name = 'prototyper.project'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = '项目'

    name = fields.Char(string='项目名称')
    description = fields.Text(string='描述')
    module_ids = fields.One2many(
        string='模块',
        comodel_name='prototyper.ir.module.module',
        inverse_name='project_id')
    menu_id = fields.Many2one(
        string='对应的菜单',
        comodel_name='prototyper.ir.ui.menu',
        ondelete='set null',
        help='技术字段,用于记录对应的菜单')
    menu2_id = fields.Many2one(
        string='项目需求菜单',
        comodel_name='prototyper.ir.ui.menu',
        ondelete='set null',
        help='技术字段,用于记录对应的菜单')

    @api.model
    def create(self, values):
        self = self.with_context(tracking_disable=True)
        record = super(PrototyperProject, self).create(values)

        if self._context.get('create_menu', False):
            record.create_menu()

        return record


    def create_menu(self):
        self.ensure_one()
        values = {
            'name': self.name,
            'parent_id': self.env.ref('odoo_prototyper_inspect.menu_prototyper_project').id,
            'sequence': 10,
        }
        self.menu_id = self.env['prototyper.ir.ui.menu'].create(values).id

        values = {
            'name': '项目需求',
            'parent_id': self.menu_id.id,
            'action': 'ir.actions.act_window,%s' % self.create_action().id,
            'sequence': 10,
        }
        self.menu2_id = self.env['prototyper.ir.ui.menu'].create(values).id


    def create_action(self):
        self.ensure_one()
        values = {
            'name': '项目需求',
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
        }
        return self.env['ir.actions.act_window'].create(values)


    def unlink(self):
        for record in self:
            record.menu_id.unlink()
            record.menu2_id.action.unlink()
            record.menu2_id.unlink()
        return super(PrototyperProject, self).unlink()


    def write(self, values):
        name = values.get('name', False)
        if name:
            for record in self:
                record.menu_id.name = name
        return super(PrototyperProject, self).write(values)
