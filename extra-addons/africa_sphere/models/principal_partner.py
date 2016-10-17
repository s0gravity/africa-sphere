# -*- encoding: utf-8 -*-

from openerp import models, fields, api, _, exceptions
import datetime
from openerp.exceptions import except_orm, Warning, RedirectWarning

class principal_partner(models.Model):
    _name = 'principal.partner'

    name = fields.Char(string="DENOMINATION", required=True)
    country = fields.Char(string="PAYS", required=True)
    type_id = fields.Many2one(comodel_name="principal.partner.type", string="TYPE", required=True)
    comment = fields.Char(string="Commentaire", required=True)
    sale_order_id = fields.Many2one(comodel_name="sale.order", string="Devis/Bon de commande")




principal_partner()

class principal_partner_type(models.Model):
    _name = 'principal.partner.type'

    name = fields.Char(string="Type",required=True)

principal_partner_type()
