# -*- encoding: utf-8 -*-

from openerp import models, fields, api, _, exceptions
import openerp.addons.decimal_precision as dp


class product_template(models.Model):
    _inherit = 'product.template'

    is_report = fields.Boolean(string="Rapport")
    report_id = fields.Many2one(comodel_name="ir.actions.report.xml", string="Type", domain=[('is_product','=',True)])

product_template()


