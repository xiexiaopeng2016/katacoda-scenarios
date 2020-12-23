# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class PrototyperModuleDoc(models.Model):
    _name = 'prototyper.ir.module.module.doc'
    _inherit = 'prototyper.ir.module.module'
    _description = '模块文档'

    model_ids = fields.One2many(comodel_name='prototyper.ir.model.doc')
    access_ids = fields.One2many(comodel_name='prototyper.ir.model.access.doc')
    rule_ids = fields.One2many(comodel_name='prototyper.ir.rule.doc')
    group_ids = fields.One2many(comodel_name='prototyper.res.groups.doc')


class PrototyperModelDoc(models.Model):
    _name = 'prototyper.ir.model.doc'
    _inherit = 'prototyper.ir.model'
    _description = '模型文档'

    module_id = fields.Many2one(comodel_name='prototyper.ir.module.module.doc')
    field_ids = fields.One2many(comodel_name='prototyper.ir.model.fields.doc')
    other_field_ids = fields.One2many(comodel_name='prototyper.ir.model.fields.doc')
    method_ids = fields.One2many(comodel_name='prototyper.ir.model.method.doc')
    other_method_ids = fields.One2many(comodel_name='prototyper.ir.model.method.doc')
    access_ids = fields.One2many(comodel_name='prototyper.ir.model.access.doc')
    rule_ids = fields.One2many(comodel_name='prototyper.ir.rule.doc')
    sql_constraint_ids = fields.One2many(comodel_name='prototyper.ir.model.sql.constraint.doc')
    category_id = fields.Many2one(comodel_name='prototyper.ir.model.category.doc')
    image_ids = fields.One2many(
        string='原型图',
        comodel_name='prototyper.ir.model.doc.image',
        inverse_name='model_id')


class PrototyperModelFieldsDoc(models.Model):
    _name = 'prototyper.ir.model.fields.doc'
    _inherit = 'prototyper.ir.model.fields'
    _description = '模型字段文档'
    _order = 'sequence,id'

    model_id = fields.Many2one(comodel_name='prototyper.ir.model.doc')
    module_id = fields.Many2one(comodel_name='prototyper.ir.module.module.doc')
    serialization_field_id = fields.Many2one(comodel_name='prototyper.ir.model.fields.doc')
    tag_ids = fields.Many2many(
        string='标签',
        comodel_name='prototyper.ir.model.fields.tag',
        relation='prototyper_ir_model_fields_doc_tag_rel',
        column1='field_id',
        column2='tag_id')


class PrototyperIrModelMethodDoc(models.Model):
    _name = 'prototyper.ir.model.method.doc'
    _inherit = 'prototyper.ir.model.method'
    _description = '模型方法文档'
    _order = 'sequence,id'

    model_id = fields.Many2one(comodel_name='prototyper.ir.model.doc')
    module_id = fields.Many2one(comodel_name='prototyper.ir.module.module.doc')


class PrototyperModelSQLConstraintDoc(models.Model):
    _name = 'prototyper.ir.model.sql.constraint.doc'
    _inherit = 'prototyper.ir.model.sql.constraint'
    _description = 'SQL约束文档'

    model_id = fields.Many2one(comodel_name='prototyper.ir.model.doc')


class PrototyperRuleDoc(models.Model):
    _name = 'prototyper.ir.rule.doc'
    _inherit = 'prototyper.ir.rule'
    _description = '记录规则文档'

    model_id = fields.Many2one(comodel_name='prototyper.ir.model.doc')
    module_id = fields.Many2one(comodel_name='prototyper.ir.module.module.doc')
    groups = fields.Many2many(
        comodel_name='prototyper.res.groups.doc',
        relation='prototyper_rule_group_doc_rel')


class PrototyperModelAccessDoc(models.Model):
    _name = 'prototyper.ir.model.access.doc'
    _inherit = 'prototyper.ir.model.access'
    _description = '访问规则文档'

    model_id = fields.Many2one(comodel_name='prototyper.ir.model.doc')
    module_id = fields.Many2one(comodel_name='prototyper.ir.module.module.doc')
    group_id = fields.Many2one(comodel_name='prototyper.res.groups.doc')


class PrototyperResGroupsDoc(models.Model):
    _name = 'prototyper.res.groups.doc'
    _inherit = 'prototyper.res.groups'
    _description = '权限组文档'

    module_id = fields.Many2one(comodel_name='prototyper.ir.module.module.doc')


class PrototyperModelCategoryDoc(models.Model):
    _name = 'prototyper.ir.model.category.doc'
    _inherit = 'prototyper.ir.model.category'
    _description = '模型分类'

    module_id = fields.Many2one(comodel_name='prototyper.ir.module.module.doc')


class PrototyperIrModelDocImage(models.Model):
    _name = 'prototyper.ir.model.doc.image'
    _description = '原型图'

    url = fields.Char(string='URL')
    model_id = fields.Many2one(
        string='模型',
        comodel_name='prototyper.ir.model.doc',
        ondelete='cascade')
