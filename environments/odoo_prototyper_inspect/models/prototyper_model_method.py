# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, api, fields


class PrototyperIrModelMethod(models.Model):
    _name = 'prototyper.ir.model.method'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = '模型方法'
    _order='sequence,id'

    name = fields.Char(string='名称', required=True, copy=False)
    description = fields.Text(string='说明')
    code = fields.Text(string='代码')
    sequence = fields.Integer(string='序号', default=10)
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

    @api.model
    def create(self, values):
        self = self.with_context(tracking_disable=True)
        return super(PrototyperIrModelMethod, self).create(values)


    @api.depends('message_ids')
    def _compute_message_qty(self):
        for rec in self:
            rec.message_qty = len(rec.message_ids)


    @api.depends('activity_ids')
    def _compute_activity_qty(self):
        for rec in self:
            rec.activity_qty = len(rec.activity_ids)


    @api.returns('mail.message', lambda value: value and value.id)
    def message_post(self, **kwargs):
        channel_id = self.env.ref('mail.channel_all_employees', raise_if_not_found=False)
        channel_id = channel_id and channel_id.id or False
        for record in self:
            if not record.message_channel_ids:
                record.message_subscribe(channel_ids=[channel_id])

        return super(PrototyperIrModelMethod, self).message_post(**kwargs)
