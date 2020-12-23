# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, api, fields


class PrototyperIrUiView(models.Model):
    _name = 'prototyper.ir.ui.view'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = '原型视图'

    model_id = fields.Many2one(
        comodel_name='prototyper.ir.model',
        string='模型',
        required=True,
        index=True,
        ondelete='cascade')
