# -*- encoding: utf-8 -*-

from openerp import models, fields, api, _, exceptions
import datetime
from openerp.exceptions import except_orm, Warning, RedirectWarning

class company_leader(models.Model):
    _name = 'company.leader'

    name = fields.Char(string="Dirigeant", required=True)
    sphere_company_id = fields.Many2one(comodel_name="company.sphere", string="Société")
    poste = fields.Char(string="Fonction")



company_leader()

