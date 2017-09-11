# -*- coding: utf-8 -*-
# Copyright 2017 vicky @ Annadurai
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    gst_in = fields.Char(string="GSTIN Number")
    ignore_gstin = fields.Boolean(string="Ignore GSTIN")
