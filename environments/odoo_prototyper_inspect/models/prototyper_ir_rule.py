# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class PrototyperRule(models.Model):
    _name = 'prototyper.ir.rule'
    _description = '记录规则'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='名称')
    model_id = fields.Many2one(
        comodel_name='prototyper.ir.model',
        string='模型',
        ondelete='cascade',
        index=True,
        required=True)
    module_id = fields.Many2one(
        comodel_name='prototyper.ir.module.module',
        related='model_id.module_id',
        store=True,
        readonly=True,
        string='模块',
        ondelete='restrict')
    groups = fields.Many2many(
        comodel_name='prototyper.res.groups',
        relation='prototyper_rule_group_rel',
        column1='rule_id',
        column2='group_id',
        string='权限组')
    domain_force = fields.Text(string='筛选条件')
    perm_read = fields.Boolean(string='应用在读取', default=True)
    perm_write = fields.Boolean(string='应用在写入', default=True)
    perm_create = fields.Boolean(string='应用在新建', default=True)
    perm_unlink = fields.Boolean(string='应用在删除', default=True)
    active = fields.Boolean(sting=u'激活', default=True)

    @api.model
    def create(self, values):
        self = self.with_context(tracking_disable=True)
        return super(PrototyperRule, self).create(values)
