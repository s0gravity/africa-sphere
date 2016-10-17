# -*- encoding: utf-8 -*-

from openerp import models, fields, api, _, exceptions
import datetime
from openerp.exceptions import except_orm, Warning, RedirectWarning

class company_shareholder(models.Model):
    _name = 'company.shareholder'

    name = fields.Char(string="ACTIONNAIRE", required=True)
    company_fiscalyear_id = fields.Many2one(comodel_name="company.sphere.fiscalyear", string="Exercice")
    shares_number = fields.Integer(string="Nombre de Parts")
    weight_percent = fields.Float(string="Poids en %",digits=(6,2))
    amount = fields.Float(string="Montants", digits=(6,2))




company_shareholder()

