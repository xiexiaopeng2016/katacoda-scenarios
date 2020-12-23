# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, api, fields
import json

class PrototyperModel(models.Model):
    _name = 'prototyper.ir.model'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = '原型模型'
    _order = 'sequence,id'

    name = fields.Char(string='模型说明')
    sequence = fields.Integer(string='序号')
    model = fields.Char(string='模型', required=True, index=True)
    class_name = fields.Char(string='类名', help='模型定义时的类名')
    order_field = fields.Char(string='排序字段', default='id')
    rec_name = fields.Char(string='记录名称', default='name')
    model_type = fields.Selection(
        string='类型',
        selection=[
            ('m', 'Model'),
            ('t', 'TransientModel'),
            ('a', 'AbstractModel'),
            ('c', 'Python Class')
        ],
        default='m')
    info = fields.Text(string='信息')
    transient = fields.Boolean(string='临时模型')
    is_inherit = fields.Boolean(string='继承')
    inherit = fields.Char(string='父模型')
    inherits = fields.Char(string='多父模型')
    create_auto = fields.Boolean(string='自动创建', default=True)
    state = fields.Selection(
        string='类别',
        selection=[
            ('manual', u'自定义对象'),
            ('base', u'基本对象')
        ],
        default='manual',
        readonly=True)
    module_id = fields.Many2one(
        comodel_name='prototyper.ir.module.module',
        string='模块',
        ondelete='restrict')
    field_ids = fields.One2many(
        string='字段',
        comodel_name='prototyper.ir.model.fields',
        inverse_name='model_id')
    other_field_ids = fields.One2many(
        string='其他字段',
        comodel_name='prototyper.ir.model.fields',
        compute='_compute_other_field_ids')
    method_ids = fields.One2many(
        string='方法',
        comodel_name='prototyper.ir.model.method',
        inverse_name='model_id')
    other_method_ids = fields.One2many(
        string='其他方法',
        comodel_name='prototyper.ir.model.method',
        compute='_compute_other_field_ids')
    access_ids = fields.One2many(
        comodel_name='prototyper.ir.model.access',
        inverse_name='model_id',
        string='访问规则')
    rule_ids = fields.One2many(
        comodel_name='prototyper.ir.rule',
        inverse_name='model_id',
        string='记录规则')
    have_menu = fields.Boolean(string='有菜单')
    sql_constraint_ids = fields.One2many(
        comodel_name='prototyper.ir.model.sql.constraint',
        inverse_name='model_id',
        string='SQL约束')
    menu_id = fields.Many2one(
        string='对应的菜单',
        comodel_name='prototyper.ir.ui.menu',
        ondelete='set null',
        help='技术字段,用于记录对应的菜单')
    position = fields.Char(string='UML图位置', default='20,20')
    category_id = fields.Many2one(
        string='分类',
        comodel_name='prototyper.ir.model.category',
        ondelete='restrict')
    note = fields.Text(string='说明')

    @api.onchange('have_menu')
    def _onchange_have_menu(self):
        menu_obj = self.env['prototyper.ir.ui.menu']
        for rec in self:
            menu = menu_obj.search([('model_name', '=', rec.model)])
            # 知识点 onchange 方法里面取不到record.id
            if rec.have_menu and not menu:
                menu_obj.with_context({}).create({'name': rec.name, 'model_name': rec.model})
            elif not rec.have_menu and menu:
                menu.write({'active': False})

    @api.model
    def create(self, values):
        self = self.with_context(tracking_disable=True)
        record = super(PrototyperModel, self).create(values)
        record.create_menu()
        return record

    def create_menu(self):
        self.ensure_one()
        parent_menu_id = self._context.get('parent_menu_id', False)
        if not parent_menu_id:
            # TODO 创建模型分类菜单
            parent_menu_id = self.module_id.menu_id.id

        values = {
            'name': self.model,
            'parent_id': parent_menu_id,
            'action': 'ir.actions.act_window,%s' % self.create_action().id,
            'web_icon': 'icon-heart',
            'sequence': 10,
        }
        self.menu_id = self.env['prototyper.ir.ui.menu'].create(values)

    def create_action(self):
        self.ensure_one()

        view_id = self.env.ref('odoo_prototyper_inspect.view_model_doc_form').id
        if self._context.get('is_js', False):
            view_id = self.env.ref('odoo_prototyper_inspect.view_model_doc_js_form').id

        values = {
            'name': self.model,
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'view_id': view_id
        }
        return self.env['ir.actions.act_window'].create(values)

    def unlink(self):
        for record in self:
            record.menu_id.action.unlink()
            record.menu_id.unlink()
        return super(PrototyperModel, self).unlink()

    def write(self, values):
        name = values.get('model', False)
        if name:
            for record in self:
                record.menu_id.name = name
                record.menu_id.action.name = name
        return super(PrototyperModel, self).write(values)

    def _compute_other_field_ids(self):
        for rec in self:
            try:
                inherits = rec.inherit and json.loads(rec.inherit.replace("\'",'\"')) or []
            except Exception as e:
                inherits = rec.inherit

            if isinstance(inherits, list):
                if 'mail.thread' in inherits:
                    inherits.remove('mail.thread')
                if 'mail.activity.mixin' in inherits:
                    inherits.remove('mail.activity.mixin')
            else:
                inherits = [inherits]

            rec.other_field_ids = self.other_field_ids.search(
                [('model_id.model', 'in', inherits), ('model_id', '!=', rec.id)], order='module_id,sequence')
            rec.other_method_ids = self.other_method_ids.search(
                [('model_id.model', '=', rec.model), ('model_id', '!=', rec.id)], order='module_id,sequence')

    def get_uml_data(self):
        self.ensure_one()

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.name or record.class_name))
        return result

    @api.returns('mail.message', lambda value: value and value.id)
    def message_post(self, **kwargs):
        channel_id = self.env.ref('mail.channel_all_employees', raise_if_not_found=False)
        channel_id = channel_id and channel_id.id or False
        for record in self:
            if not record.message_channel_ids:
                record.message_subscribe(channel_ids=[channel_id])

        return super(PrototyperModel, self).message_post(**kwargs)


class PrototyperModelSQLConstraint(models.Model):
    _name = 'prototyper.ir.model.sql.constraint'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'SQL约束'

    constraint_type = fields.Selection(
        selection=[
            ('unique', u'唯一约束'),
            ('check', u'检查约束'),
        ],
        string='约束类型')
    constraint_fields = fields.Char(string='约束字段')
    message = fields.Char(string='提示信息')
    model_id = fields.Many2one(
        comodel_name='prototyper.ir.model',
        string='模型',
        ondelete='cascade')

    @api.model
    def create(self, values):
        self = self.with_context(tracking_disable=True)
        return super(PrototyperModelSQLConstraint, self).create(values)


class PrototyperModelCategory(models.Model):
    _name = 'prototyper.ir.model.category'
    _description = '模型分类'

    name = fields.Char(string='名称')
    module_id = fields.Many2one(
        comodel_name='prototyper.ir.module.module',
        string='模块',
        ondelete='restrict')
