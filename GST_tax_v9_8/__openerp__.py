# -*- coding: utf-8 -*-
# Copyright 2017 Vignesh @ Annadurai
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "GST  SGST Indian Tax system 2017 for SALES and PURCHASE v8 and v9",

    'summary': """
       GST / SGST Indian Tax system 2017 for VERSION 8 and 9. pls check for V10""",

    'author': " Vignesh ",
    'website': "viki2.odoo.com",
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'category': 'Tax',
    'version': '9.0.0.1',
    'depends': ['base', 'sale', 'purchase',
                ],
    'images': ['images/main_screenshot.png'],
    'data': [
        'views/sale_views.xml',
        'views/res_partner.xml',
        'views/purchase_view.xml',
        'views/sale_report.xml',
        'views/purchase_report.xml',
        'views/gst_tax_view.xml',
        'views/gst_tax_purchase_view.xml',
    ],
    'demo': [
    ],
}
