# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, api, fields


class ProjectRequirementLine(models.Model):
    _name = 'project.requirement.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = '业务需求明细'
    _order = 'sequence,id'

    name = fields.Char(string='名称', required=True, copy=False)
    description = fields.Text(string='描述')
    sequence = fields.Integer(string='序号', default=10)
    project_id = fields.Many2one(
        string='项目',
        comodel_name='prototyper.project',
        ondelete='restrict')
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

    @api.depends('message_ids')
    def _compute_message_qty(self):
        for rec in self:
            rec.message_qty = len(rec.message_ids)

    @api.depends('activity_ids')
    def _compute_activity_qty(self):
        for rec in self:
            rec.activity_qty = len(rec.activity_ids)


class PrototyperProject(models.Model):
    _inherit = 'prototyper.project'

    requirement_line_ids = fields.One2many(
        string='业务需求明细',
        comodel_name='project.requirement.line',
        inverse_name='project_id')
