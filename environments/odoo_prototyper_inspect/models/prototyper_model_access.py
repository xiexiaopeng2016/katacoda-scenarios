# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, api, fields


class PrototyperModelAccess(models.Model):
    _name = 'prototyper.ir.model.access'
    _description = '访问规则'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='名称')
    model_id = fields.Many2one(
        comodel_name='prototyper.ir.model',
        string='模型',
        required=True,
        domain=[('transient', '=', False)],
        index=True,
        ondelete='cascade')
    module_id = fields.Many2one(
        comodel_name='prototyper.ir.module.module',
        related='model_id.module_id',
        store=True,
        readonly=True,
        string='模块',
        ondelete='restrict')
    group_id = fields.Many2one(
        comodel_name='prototyper.res.groups',
        string='权限组',
        ondelete='cascade',
        index=True)
    perm_read = fields.Boolean(string='读权限')
    perm_write = fields.Boolean(string='写权限')
    perm_create = fields.Boolean(string='创建权限')
    perm_unlink = fields.Boolean(string='删除权限')
    active = fields.Boolean(string='激活', default=True)
    access_xml_id = fields.Char(
        string='规则XML-ID', compute='_compute_access_xml_id', store=True)
    message_qty = fields.Integer(
        string='消息数量',
        compute='_compute_message_qty',
        compute_sudo=True,
        store=True,
        readonly=True)
    activity_qty = fields.Integer(
        string='活动数量',
        compute='_compute_activity_qty',
        compute_sudo=True,
        store=True,
        readonly=True)


    @api.depends('message_ids')
    def _compute_message_qty(self):
        for rec in self:
            rec.message_qty = len(rec.message_ids)


    @api.depends('activity_ids')
    def _compute_activity_qty(self):
        for rec in self:
            rec.activity_qty = len(rec.activity_ids)


    @api.depends('group_id', 'group_id.name')
    def _compute_access_xml_id(self):
        for rec in self:
            model_name = self._name.replace('.', '_')
            group_name = rec.group_id.name or 'all'
            rec.access_xml_id = 'access_%s_%s' % (model_name, group_name)


    @api.onchange('group_id', 'group_id.name', 'perm_read', 'perm_write',
                  'perm_create', 'perm_unlink')
    def _onchange_group_right(self):
        for rec in self:
            group_name = rec.group_id.name if rec.group_id else u'所有用户'
            access_right = ''
            if rec.perm_read:
                access_right += '-读'
            if rec.perm_write:
                access_right += '-写'
            if rec.perm_create:
                access_right += '-建'
            if rec.perm_unlink:
                access_right += '-删'
            if not access_right:
                access_right = '没有任何权限'
            rec.name = '%s%s' % (group_name, access_right)

    @api.model
    def create(self, values):
        self = self.with_context(tracking_disable=True)
        return super(PrototyperModelAccess, self).create(values)
