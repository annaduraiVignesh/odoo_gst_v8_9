# -*- coding: utf-8 -*-
# Copyright 2017 vicky @ Annadurai
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class GstTax(models.Model):

    _name = 'gst.tax'

    tax_name = fields.Char(string="Tax_name", Required=True)
    gst_tax_percent = fields.Float(string="GST Percent")
    sgst_tax_percent = fields.Float(string="SGST Percent")
