# -*- encoding: utf-8 -*-

from openerp import models, fields, api, _, exceptions
import datetime
from openerp.exceptions import except_orm, Warning, RedirectWarning

class sphere_reporting_history(models.Model):
    _name = 'sphere.reporting.history'
    _order = 'date desc'

    name = fields.Char(string="Nom",related="product_id.name")
    date = fields.Datetime(string="Date génération")
    partner_id = fields.Many2one(comodel_name="res.partner", string="Client")
    product_id = fields.Many2one(comodel_name="product.product", string="Article")
    order_id = fields.Many2one(comodel_name="sale.order", string="Bon de commande")
    type = fields.Selection(string="Type", selection=[('new', 'Nouveau BC'), ('merge', 'Fusion')])

sphere_reporting_history()

