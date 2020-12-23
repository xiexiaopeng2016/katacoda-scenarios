# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, api, fields


class PrototyperModelFields(models.Model):
    _name = 'prototyper.ir.model.fields'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = '字段'
    _order = 'sequence,id'

    sequence = fields.Integer(string='序号', default=10)
    is_extend = fields.Boolean(string='拓展原字段')
    name = fields.Char(string='字段名', index=True)
    model = fields.Char(string='对象名', index=True)
    model_id = fields.Many2one(
        comodel_name='prototyper.ir.model',
        string='模型',
        ondelete='cascade')
    module_id = fields.Many2one(
        comodel_name='prototyper.ir.module.module',
        string='模块',
        ondelete='restrict',
        related='model_id.module_id',
        store=True,
        readonly=True)
    # 公共字段属性
    field_description = fields.Char(string='字段标签', track_visibility='onchange')
    help = fields.Char(string='帮助', size=255)
    ttype = fields.Selection(
        selection='_get_field_types', string='字段类型')
    selection = fields.Text(
        string='选项',
        default="""[
    ('1', u'1'),
    ('2', u'2'),
    ('3', u'3')
]""")
    selection_add = fields.Text(string='附加选项')
    can_copy = fields.Boolean(string='复制', default=True)
    required = fields.Boolean(string='必填')
    readonly = fields.Boolean(string='只读', default=False)
    index = fields.Boolean(string='索引')
    translate = fields.Boolean(string='翻译')
    track_visibility = fields.Selection(
        selection=[
            ('', ''),
            ('onchange', 'onchange'),
            ('always', 'always'),
        ],
        string='追踪值的变化')
    # 字符串字段属性
    size = fields.Integer(string='字符长度')
    # Float字段属性
    digits = fields.Char(string='小数位数')
    groups = fields.Char(string='权限组')
    # selectable = fields.Boolean(default=True)
    # 关系字段
    comodel_name = fields.Char(
        string='关联对象',
        help="For relationship fields, the technical name of the target model")
    comodel_name_link = fields.Char(
        string='关联对象链接',
        compute='_compute_comodel_name_link',
        compute_sudo=True,
        store=True,
        readonly=True)
    inverse_name = fields.Char(string='反向字段')
    on_delete = fields.Selection(
        selection=[
            ('restrict', 'Restrict'),
            ('cascade', 'Cascade'),
            ('set null', 'Set NULL')],
        string='删除时',
        default='restrict',
        help='On delete property for many2one fields')
    domain = fields.Char(string='过滤')
    relation_field = fields.Char(string='关联字段')
    serialization_field_id = fields.Many2one(
        comodel_name='prototyper.ir.model.fields',
        string='Serialization Field',
        domain="[('ttype','=','serialized')]",
        ondelete='cascade',
        help="If set, this field will be stored in the sparse "
             "structure of the serialization field, instead "
             "of having its own database column. This cannot be "
             "changed after creation.")
    relation_table = fields.Char(
        help="Used for custom many2many fields to define a custom relation table name"
    )
    column1 = fields.Char(
        string='Column 1',
        help="Column referring to the record in the model table")
    column2 = fields.Char(
        string="Column 2",
        help="Column referring to the record in the comodel table")
    auto_join = fields.Boolean(string='生成联接', help=u'是否在该字段搜索时生成联接')
    limit = fields.Integer(string='读取条数')
    # 计算字段属性
    is_compute_field = fields.Boolean(string='计算字段')
    depends_fields = fields.Char(
        string='计算依赖字段',
        help="Dependencies of compute method; "
             "a list of comma-separated field names, like\n\n"
             "    name, partner_id.name")
    compute_method = fields.Char(
        string='计算方法',
        help="Code to compute the value of the field.\n"
             "Iterate on the recordset 'self' and assign the field's value:\n\n"
             "    for record in self:\n"
             "        record['size'] = len(record.name)\n\n"
             "Modules time, datetime, dateutil are available.")
    inverse_method = fields.Char(string='反算方法')
    search_method = fields.Char(string='搜索方法')
    store = fields.Boolean(
        string='保存在数据库',
        default=True,
        help='Whether the value is stored in the database.')
    compute_sudo = fields.Boolean(string='计算时绕过权限控制')
    # 关联字段
    is_related_field = fields.Boolean(string='关联字段')
    related_field = fields.Char(
        string='关联的字段',
        help='The corresponding related field, if any. This must be a dot-separated list of field names.')
    related_sudo = fields.Boolean(string='关联时绕过权限控制')
    default_value = fields.Char(string='默认值', default=' ')
    is_default_now = fields.Boolean(string='默认当前日期')
    is_prefetch = fields.Boolean(string='预取')
    is_attachment = fields.Boolean(string='保存为附件')
    currency_field = fields.Char(string='币别字段')
    # sparse
    state = fields.Selection(
        selection=[('manual', 'Custom Field'), ('base', 'Base Field')],
        string='Type',
        default='manual',
        required=True,
        readonly=True,
        index=True)
    tag_ids = fields.Many2many(
        string='标签',
        comodel_name='prototyper.ir.model.fields.tag',
        relation='prototyper_ir_model_fields_tag_rel',
        column1='field_id',
        column2='tag_id')
    message_qty = fields.Integer(
        string='消息数量',
        compute='_compute_message_qty',
        compute_sudo=True,
        store=False,
        readonly=True)
    activity_qty = fields.Integer(
        string='活动数量',
        compute='_compute_activity_qty',
        compute_sudo=True,
        store=False,
        readonly=True)
    note = fields.Text(string='说明')
    change_default = fields.Boolean(
        string='change_default',
        help='该字段是否可能触发user-onchange')
    company_dependent = fields.Boolean(
        string='company_dependent')
    group_operator = fields.Char(
        string='group_operator',
        help='用于汇总值的运算符 sum, svg')
    group_expand = fields.Char(
        string='group_expand',
        help='在read_group()中展开组的方法的名称')
    states = fields.Char(
        string='states',
        help='依赖state字段设置只读和必填属性')
    depends = fields.Char(
        string='depends',
        help='字段依赖关系的集合')

    @api.model
    def _get_field_types(self):
        # retrieve the possible field types from the field classes' metaclass
        return sorted((key, key) for key in fields.MetaField.by_type)


    @api.onchange('is_compute_field')
    def _onchange_is_compute_field(self):
        for rec in self:
            if rec.is_compute_field:
                rec.compute_method = '_compute_%s' % rec.name
                rec.readonly = True
                rec.is_related_field = False
            else:
                rec.compute_method = ''
                rec.readonly = False


    @api.onchange('is_related_field')
    def _onchange_is_related_field(self):
        for rec in self:
            if rec.is_related_field:
                rec.is_compute_field = False


    @api.onchange('is_default_now')
    def _onchange_is_default_now(self):
        for rec in self:
            is_default = rec.is_default_now
            if rec.ttype == 'date':
                rec.default_value = 'fields.Date.today' if is_default else ''
            elif rec.ttype == 'datetime':
                rec.default_value = 'fields.datetime.now' if is_default else ''


    @api.onchange('name')
    def _onchange_name(self):
        for rec in self:
            if rec.name == 'name':
                rec.field_description = '名称'
                rec.ttype = 'char'
            elif rec.name == 'sequence':
                rec.field_description = '序号'
                rec.ttype = 'integer'
            elif rec.name == 'description':
                rec.field_description = '说明'
                rec.ttype = 'text'
            elif rec.name == 'active':
                rec.field_description = '归档'
                rec.default_value = 'True'
                rec.ttype = 'boolean'
            elif rec.name == 'partner_id':
                rec.field_description = '业务伙伴'
                rec.ttype = 'many2one'
                rec.comodel_name = 'res.partner'
            elif rec.name == 'user_id':
                rec.field_description = '用户'
                rec.ttype = 'many2one'
                rec.comodel_name = 'res.users'
            elif rec.name == 'priority':
                rec.field_description = '优先级'
                rec.ttype = 'selection'
                rec.selection = """[
    ('0', u'0 星'),
    ('1', u'1 星'),
    ('2', u'2 星'),
    ('3', u'3 星'),
    ('4', u'4 星'),
    ('5', u'5 星'),
]"""
            elif rec.name == 'tag_ids':
                rec.ttype = 'many2many'
            elif rec.name == 'company_id':
                rec.field_description = '公司'
                rec.ttype = 'many2one'
                rec.comodel_name = 'res.company'
            elif rec.name == 'parent_id':
                rec.field_description = '父记录'
                rec.ttype = 'many2one'
                rec.comodel_name = rec.model_id.model or ''
            elif rec.name == 'child_ids':
                rec.field_description = '子记录'
                rec.ttype = 'one2many'
                rec.comodel_name = rec.model_id.model or ''
                rec.inverse_name = 'parent_id'
            elif rec.name == 'color':
                rec.field_description = '颜色'
                rec.ttype = 'integer'
                rec.default_value = '10'
            elif (rec.name or '').endswith('_id'):
                rec.ttype = 'many2one'
            elif (rec.name or '').endswith('_ids'):
                rec.ttype = 'one2many'
            elif (rec.name or '').endswith('_count'):
                rec.ttype = 'integer'
            elif (rec.name or '').endswith('_date'):
                rec.ttype = 'date'
            elif (rec.name or '').endswith('_time'):
                rec.ttype = 'datetime'


    @api.depends('message_ids')
    def _compute_message_qty(self):
        for rec in self:
            rec.message_qty = len(rec.message_ids)


    @api.depends('activity_ids')
    def _compute_activity_qty(self):
        for rec in self:
            rec.activity_qty = len(rec.activity_ids)

    @api.model
    def create(self, values):
        self = self.with_context(tracking_disable=True)
        return super(PrototyperModelFields, self).create(values)


    @api.depends('comodel_name')
    def _compute_comodel_name_link(self):
        menu_obj = self.env['prototyper.ir.ui.menu']
        for rec in self:
            if not rec.comodel_name:
                continue
            menu = menu_obj.search([('name', '=', rec.comodel_name), ('action', '!=', False)], limit=1)
            if menu:
                rec.comodel_name_link = '/web#menu_id=%s&action=%s' % (menu.id, menu.action.id)


    @api.returns('mail.message', lambda value: value and value.id)
    def message_post(self, **kwargs):
        channel_id = self.env.ref('mail.channel_all_employees', raise_if_not_found=False)
        channel_id = channel_id and channel_id.id or False
        for record in self:
            if not record.message_channel_ids:
                record.message_subscribe(channel_ids=[channel_id])

        return super(PrototyperModelFields, self).message_post(**kwargs)


class PrototyperModelFieldsTag(models.Model):
    _name = 'prototyper.ir.model.fields.tag'
    _description = '字段标签'

    name = fields.Char(string='名称')
    color = fields.Integer(string='颜色')
