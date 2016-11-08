# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'AFRICA SPHERE',
    'version': '1.0',
    'author': 'UKNOWN',
    'summary': 'AFRICA SPHERE SPEC',
    'description': """
        AFRICA SPHERE SPEC""",

    'website': '',

    'depends': ['base','sale','knowledge'],

    'category': 'other',
    'demo': [],
    'data': [
             "security/ir.model.access.csv",
             "views/sphere_company.xml",
             "views/product.xml",
             "views/ir_actions_report_xml.xml",
             "views/sale_order.xml",
             "views/sphere_company_fiscalyear.xml",
             "views/sphere_reporting_history.xml",
             "wizard/report_order/report_order_wizard_view.xml",
             "reports/product_A.xml",
             "reports/product_B.xml",
            ],

    'application':True,
    'installable':True,
 }
