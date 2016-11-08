# -*- encoding: utf-8 -*-

from openerp import models, fields, api, _, exceptions
from datetime import datetime
from openerp.exceptions import except_orm, Warning, RedirectWarning
from dateutil.relativedelta import relativedelta
from dateutil import parser

class sphere_company(models.Model):
    _name = 'sphere.company'

    name = fields.Char(string="Company name", required=True)
    partner_id = fields.Many2one(comodel_name="res.partner", string="Related customer",domain=[('customer','=',True),('is_company','=',True)])
    country_id = fields.Many2one(comodel_name="res.country", string="COUNTRY ORIGIN")
    country_phone_code = fields.Char(string="Country phone code")
    registration_number = fields.Char(string="Registration number")
    central_bank_activity_code = fields.Char(string="Central bank activity code")
    l_bank_activity_main = fields.Char(string="L bank activity main")
    activity_wording = fields.Char(string="Activity wording")
    tpype = fields.Char(string="TPYPE")
    standard_email = fields.Char(string="Standard email")
    phone = fields.Char(string="Phone")
    fax = fields.Char(string="Fax")
    geo_situation_address = fields.Char(string="GEO. SITUATION / ADDRESS")
    po_box = fields.Char(string="PO/BOX")
    ppal_contact = fields.Char(string="Principal contact")
    ppal_function = fields.Char(string="Function")
    ppal_email = fields.Char(string="Email Ppal contact")
    direct_line = fields.Char(string="Direct line")
    other = fields.Text(string="Other")
    company_fiscalyear_ids = fields.One2many(comodel_name="sphere.company.fiscalyear", inverse_name="sphere_company_id", string="Exercices")
    company_leader_ids = fields.One2many(comodel_name="company.leader", inverse_name="sphere_company_id", string="Dirigeants")

    sigle = fields.Char(string="Sigle")
    creation_date = fields.Date(string="ANNEE DE CREATION")
    nb_years_existance = fields.Integer(string="DUREE EXISTANCE EN ANNEES",readonly=True,compute="_calculate_years_of_existance")
    legal_form = fields.Char(string="Forme Légale")
    num_rccm_kbis = fields.Char(string="Num. RCCM-KBIS")
    city = fields.Char(string="Ville")
    bp = fields.Char(string="BP")
    siege_social = fields.Char(string="Siège Social")
    code_act = fields.Char(string="Code Activité BANQ. CENTR.")
    name_act = fields.Char(string="Nom Activité BANQ. CENTR.")
    maison_mere = fields.Char(string="Maison Mère")
    maison_weight = fields.Float(string="Poids des Actions en %",digits=(6,2))
    history = fields.Text(string="")

    @api.one
    @api.depends('creation_date')
    def _calculate_years_of_existance(self):
        if self.creation_date:
            self.nb_years_existance = relativedelta(datetime.now().date(), parser.parse(self.creation_date).date()).years
        else:
            self.nb_years_existance = 0




sphere_company()