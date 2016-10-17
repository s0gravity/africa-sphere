# -*- encoding: utf-8 -*-

from openerp import models, fields, api, _, exceptions
import openerp.addons.decimal_precision as dp


class ir_actions_report_xml(models.Model):
    _inherit = 'ir.actions.report.xml'

    is_product = fields.Boolean(string="Est un produit ?")

ir_actions_report_xml()




