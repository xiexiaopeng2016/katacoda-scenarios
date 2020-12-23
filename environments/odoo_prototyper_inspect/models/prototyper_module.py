# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, api, fields
from odoo.addons.odoo_prototyper_inspect.models.prototyper_constructor import PrototyperConstructor


class PrototyperModule(models.Model):
    _name = 'prototyper.ir.module.module'
    _description = '模块'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='技术名称', readonly=False, required=True, index=True)
    sequence = fields.Char(string='序号', default=10)
    category_id = fields.Many2one(
        comodel_name='prototyper.ir.module.category',
        string='模块类别',
        readonly=False,
        index=True)
    shortdesc = fields.Char(string='模块名称', readonly=False)
    summary = fields.Char(string='摘要', readonly=False)
    description = fields.Text(string='说明', readonly=False)
    author = fields.Char(string='作者', readonly=False, default='Xie Xiaopeng')
    maintainer = fields.Char(string='维护者', readonly=False, default='Xie Xiaopeng')
    contributors = fields.Text(string='贡献者', readonly=False)
    website = fields.Char(string='网站', readonly=False, default='2248079054@qq.com')
    latest_version = fields.Char(string='安装版本', readonly=False)
    published_version = fields.Char(string='发布版本', readonly=False, default='11.0.1.0.0')
    chapter_code = fields.Char(string='文档章节号', default=1.0)
    depends = fields.Char(string='依赖模块', default='base')
    auto_install = fields.Boolean(string='自动安装')
    demo = fields.Boolean(string='加载演示数据', default=False, readonly=False)
    license = fields.Selection(
        [('GPL-2', 'GPL Version 2'),
         ('GPL-2 or any later version', 'GPL-2 or later version'),
         ('GPL-3', 'GPL Version 3'),
         ('GPL-3 or any later version', 'GPL-3 or later version'),
         ('AGPL-3', 'Affero GPL-3'), ('LGPL-3', 'LGPL Version 3'),
         ('Other OSI approved licence', 'Other OSI Approved Licence'),
         ('OEEL-1', 'Odoo Enterprise Edition License v1.0'),
         ('OPL-1', 'Odoo Proprietary License v1.0'),
         ('Other proprietary', 'Other Proprietary')],
        string='许可证',
        default='LGPL-3',
        readonly=False)
    application = fields.Boolean(string='应用', readonly=False)
    model_ids = fields.One2many(
        comodel_name='prototyper.ir.model',
        inverse_name='module_id',
        string='对象')
    access_ids = fields.One2many(
        comodel_name='prototyper.ir.model.access',
        inverse_name='module_id',
        string='Access')
    rule_ids = fields.One2many(
        comodel_name='prototyper.ir.rule',
        inverse_name='module_id',
        string='记录规则')
    group_ids = fields.One2many(
        comodel_name='prototyper.res.groups',
        inverse_name='module_id',
        string='权限组')
    data = fields.Binary(string='默认', readonly=True)
    filename = fields.Char(
        string='文件名',
        compute='_compute_filename',
        store=True,
        readonly=True)
    project_id = fields.Many2one(
        string='项目',
        comodel_name='prototyper.project',
        ondelete='set null')
    menu_id = fields.Many2one(
        string='对应的菜单',
        comodel_name='prototyper.ir.ui.menu',
        ondelete='set null',
        help='技术字段,用于记录对应的菜单')
    menu2_id = fields.Many2one(
        string='模块信息菜单',
        comodel_name='ir.ui.menu',
        ondelete='set null',
        help='技术字段,用于记录对应的菜单')
    note = fields.Text(string='说明')

    @api.onchange('shortdesc')
    def _onchange_shortdesc(self):
        for rec in self:
            if not rec.summary:
                rec.summary = rec.shortdesc

    def button_module_export_action(self):
        PrototyperConstructor().action_export(self)

    @api.depends('name')
    def _compute_filename(self):
        for rec in self:
            rec.filename = '%s.zip' % rec.name

    def button_module_export_action2(self):
        module_path = '/opt/code/odoo-12.0/addons/account'
        result = self.env['prototyper.module.inspect'].parse_module_source(module_path)
        self.env['prototyper.module.reverser'].action_module_reverser(result)
        print(result)

    @api.model
    def create(self, values):
        self = self.with_context(tracking_disable=True)
        record = super(PrototyperModule, self).create(values)
        record.create_menu()
        return record

    def create_menu(self):
        self.ensure_one()
        parent_id = self.project_id.menu_id.id

        action_id = self.create_action().id
        values = {
            'name': self.shortdesc,
            'parent_id': parent_id,
            'action': 'ir.actions.act_window,%s' % action_id,
            'sequence': 10,
            'is_sider_menu': True,
        }
        self.menu_id = self.env['prototyper.ir.ui.menu'].create(values).id

        values = {
            'name': '模块信息',
            'parent_id': self.menu_id.id,
            'action': 'ir.actions.act_window,%s' % action_id,
            'web_icon': 'icon-home',
            'sequence': 10,
        }
        self.menu2_id = self.env['prototyper.ir.ui.menu'].create(values).id

    def create_action(self):
        self.ensure_one()
        values = {
            'name': self.shortdesc,
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
        }
        return self.env['ir.actions.act_window'].create(values)

    def unlink(self):
        for record in self:
            record.menu_id.action.unlink()
            record.menu_id.unlink()
            record.menu2_id.unlink()
        return super(PrototyperModule, self).unlink()

    def write(self, values):
        name = values.get('name', False)
        if name:
            for record in self:
                record.menu_id.action.name = name
                record.menu_id.name = name
                record.menu2_id.name = name
        return super(PrototyperModule, self).write(values)

    def get_uml_data(self):
        self.ensure_one()
        result = {'classes': {}, 'relations': []}
        for model in self.model_ids:
            result['classes'].update({
                model.model.replace('.', '_'): {
                    'name': model.model,
                    'type': model.model_type,
                    'position': model.position,
                    'attributes': [
                        '%s: %s %s' % (f.name, f.ttype, f.field_description)
                        for f in model.field_ids if f.name
                    ],
                    'methods': [
                        '%s: %s' % (m.name, m.description) for m in model.method_ids if m.name
                    ],
                }
            })

            # 继承
            # 关联 m2o, o2m, m2m, ref
            fields = model.field_ids.filtered(lambda f: f.ttype in ['many2one', 'one2many', 'many2many'])
            for field in fields:
                if not field.comodel_name:
                    continue
                relation = {'source': (model.model, field.name), 'target': (field.comodel_name, 'id')}
                result['relations'].append(relation)
        return result
