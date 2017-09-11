# -*- coding: utf-8 -*-
# Copyright 2017 vicky @ Annadurai
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import api, fields, models, _


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    gst = fields.Boolean(
        string="GST",
        copy=False,
        help="Check this to calculate GST for Purchase Order")
    sgst = fields.Boolean(string="SGST", copy=False, readonly=True)
    gst_in = fields.Char(string="GSTIN Number", copy=False)
    gst_total = fields.Float(String="GST TOTAL")
    sgst_total = fields.Float(String="SGST TOTAL")
    manual_calculate = fields.Boolean(string="Manual calculate tax")

    @api.depends('order_line.price_total')
    def _amount_all(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            gst_total = sgst_total = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                if order.company_id.tax_calculation_rounding_method == 'round_globally':
                    taxes = line.taxes_id.compute_all(
                        line.price_unit,
                        line.order_id.currency_id,
                        line.product_qty,
                        product=line.product_id,
                        partner=line.order_id.partner_id)
                    amount_tax += sum(t.get('amount', 0.0)
                                      for t in taxes.get('taxes', []))
                    gst_total += line.gst_line
                    sgst_total += line.sgst_line
                else:
                    amount_tax += line.price_tax
                    gst_total += line.gst_line
                    sgst_total += line.sgst_line
            order.update({
                'amount_untaxed': order.currency_id.round(amount_untaxed),
                'amount_tax': order.currency_id.round(amount_tax),
                'amount_total': amount_untaxed + amount_tax + gst_total + sgst_total,
                'gst_total': gst_total,
                'sgst_total': sgst_total,
            })

    @api.onchange(
        'order_line',
        'gst',
        'order_line.price_subtotal',
        'order_line.product_uom_qty',
        'order_line.price_unit',
        'order_line.product_id',
        'manual_calculate',
        'order_line.gst_line_manual')
    def onchange_gst(self):
        if self.gst:
            self.sgst = True
            self.manual_calculate = False
            tax_mod = self.env['gst.tax'].browse(1)
            for line in self:
                for order in line.order_line:
                    order.write(
                        {'gst_line': (order.price_subtotal / 100) * (tax_mod.gst_tax_percent)})
                    order.write(
                        {'sgst_line': (order.price_subtotal / 100) * (tax_mod.sgst_tax_percent)})
        if self.manual_calculate:
            self.gst = False
            self.sgst = False
            for line in self:
                for order in line.order_line:
                    order.write(
                        {'gst_line': (order.price_subtotal / 100) * (order.gst_line_manual)})
                    order.write(
                        {'sgst_line': (order.price_subtotal / 100) * (order.sgst_line_manual)})
        if self.gst == False and self.manual_calculate == False:
            self.sgst = False
            for line in self:
                for order in line.order_line:
                    order.write({'gst_line': None})
                    order.write({'sgst_line': None})
                    order.write({'gst_line_manual': None})
                    order.write({'sgst_line_manual': None})

    @api.onchange('partner_id')
    def onchange_partnerid(self):
        if self.partner_id.gst_in:
            self.gst_in = self.partner_id.gst_in
        if not self.partner_id.gst_in:
            self.gst_in = None


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    gst_line = fields.Float(
        string="GST Amount",
        store=True,
        copy=False,
        readonly=True)
    sgst_line = fields.Float(
        string="SGST Amount",
        store=True,
        copy=False,
        readonly=True)
    gst_line_manual = fields.Float(
        string="GST % manual", store=True, copy=False)
    sgst_line_manual = fields.Float(
        string="SGST % manual", store=True, copy=False)
