# -*- encoding: utf-8 -*-

from openerp import models, fields, api, _, exceptions
import datetime
from openerp.exceptions import except_orm, Warning, RedirectWarning

class sphere_company_fiscalyear(models.Model):
    _name = 'sphere.company.fiscalyear'

    name = fields.Char(string="Nom",related="fiscalyear_id.name")
    fiscalyear_id = fields.Many2one(comodel_name="account.fiscalyear", string="Exercice", required=True)
    sphere_company_id = fields.Many2one(comodel_name="sphere.company", string="Société", required=True)


    #finance
    capital = fields.Float(string="CAPITAL",digits=(6,2))
    turnover_y1 = fields.Float(string="TURNOVER YEAR -1",digits=(6,2))
    turnover_y2 = fields.Float(string="TURNOVER YEAR -2",digits=(6,2))
    net_result_y1 = fields.Float(string="NET RESULT YEAR -1",digits=(6,2))
    net_result_y2 = fields.Float(string="NET RESULT YEAR -2",digits=(6,2))
    scoring = fields.Char(string="@SPHERES ONGOING SCORING")
    #finance

    #ACTIONNAIRES
    company_shareholder_ids = fields.One2many(comodel_name="company.shareholder", inverse_name="company_fiscalyear_id", string="ACTINNAIRES", required=False, )
    act_comment = fields.Text(string="", required=False)
    #ACTIONNAIRES

    #DONNES FINANCIERES ET COMPTABLES
    origin = fields.Selection(string="ORIGINE DES DONNEES", selection=[('fin', 'Services Financiers de la Société'), ('local', 'Source Locale'), ('other','Autres') ], required=True)
    #Actif
    tr_bt = fields.Float(string="Terraints, Batîments...",digits=(6,2))
    fdc_br_log = fields.Float(string="Fds de Commerce, Brevets, Logiciels...", digits=(6, 2))
    ci = fields.Float(string="Charges Immobilisées",digits=(6,2))
    miia = fields.Float(string="Matériel Industriel, Instal, Agencements...",digits=(6,2))
    mdbmi = fields.Float(string="Matériels de Bureau, Mat. Informatique...",digits=(6,2))
    mdtem = fields.Float(string="Matériels de Transports et Mobiles",digits=(6,2))
    af = fields.Float(string="Actifs Financiers",digits=(6,2))
    other_actif = fields.Float(string="Autres (Avance sur Immob...)",digits=(6,2))
    total_actif_immobilise = fields.Float(string="ACTIF IMMOBILISE",digits=(6,2),compute="_total_actif_immobilise")
    stock = fields.Float(string="Stocks",digits=(6,2))
    fav = fields.Float(string="Fournisseurs avance versées",digits=(6,2))
    customers = fields.Float(string="Clients",digits=(6,2))
    cfes = fields.Float(string="Créances Fiscales et Sociales",digits=(6,2))
    ac = fields.Float(string="Autres Créances",digits=(6,2))
    cca = fields.Float(string="Charges Constatées d'avance, Ecart Conv",digits=(6,2))
    total_actif_circulant = fields.Float(string="ACTIF CIRCULANT",digits=(6,2),compute="_total_actif_circulant")
    bcctdp = fields.Float(string="Banques, Chèques, Caisse, Titres de placements",digits=(6,2))
    eca = fields.Float(string="Ecart de Conversion-Actif",digits=(6,2))
    total_treso_actif = fields.Float(string="TRESORERIE ACTIF",digits=(6,2),compute="_total_treso_actif")
    total_actif = fields.Float(string="Total Actif",digits=(6,2),compute="_total_actif")
    #Passif
    cs = fields.Float(string="Capital Social",digits=(6,2))
    act_cna = fields.Float(string="Actionnaire Capital Non Appelé",digits=(6,2))
    ran = fields.Float(string="Report A Nouveau",digits=(6,2))
    ra = fields.Float(string="Résultat Annuel",digits=(6,2))
    reserves = fields.Float(string="Réserves",digits=(6,2))
    arpc = fields.Float(string="Subvention, Primes, Ecart Reeval. Autres...",digits=(6,2))
    df = fields.Float(string="Dettes Financières",digits=(6,2))
    aycpr = fields.Float(string="Autres (Prov Fin. Risq et Ch.)",digits=(6,2))
    total_capitaux_perman = fields.Float(string="CAPITAUX PERMANENTS",digits=(6,2),compute="_total_capitaux_perman")
    cap = fields.Float(string="Clients Avances Perçues",digits=(6,2))
    dfr = fields.Float(string="Dettes Fournisseurs",digits=(6,2))
    dfes = fields.Float(string="Dettes Fiscales et Sociales",digits=(6,2))
    ad = fields.Float(string="Autres Dettes",digits=(6,2))
    pca = fields.Float(string="Produits Constatés d'Avance, Ecart Conv",digits=(6,2))
    total_passif_circulant = fields.Float(string="PASSIF CIRCULANT",digits=(6,2),compute="_total_passif_circulant")
    bcc = fields.Float(string="Banques, Chèques, Caisse...",digits=(6,2))
    ecp = fields.Float(string="Ecart de Conversion-Passif",digits=(6,2))
    total_treso_passif = fields.Float(string="TRESORERIE PASSIF",digits=(6,2),compute="_total_treso_passif")
    total_passif = fields.Float(string="Total Passif",digits=(6,2),compute="_total_passif")
    #COMPTE DE RESULTAT EN MONNAIE LOCALE
    #Charges
    ampmc = fields.Float(string="Achat de Mat. Prem, Marchandises et Consommables",digits=(6,2))
    vds = fields.Float(string="Variation de Stocks",digits=(6,2))
    other_charges = fields.Float(string="AUTRES DEPENSES",digits=(6,2),compute="_other_charges")
    td = fields.Float(string="Transport & Déplacement",digits=(6,2))
    seosa = fields.Float(string="Services Extérieur (OHADA Serv. A)",digits=(6,2))
    seosb = fields.Float(string="Services Extérieur (OHADA Serv. B)",digits=(6,2))
    ac1 = fields.Float(string="Autres Charges",digits=(6,2))
    it = fields.Float(string="IMPOTS et TAXES",digits=(6,2))
    cp = fields.Float(string="CHARGES DU PERSONNEL",digits=(6,2))
    ap = fields.Float(string="AMORTISSEMENT ET PROVISIONS",digits=(6,2))
    total_charges_exp = fields.Float(string="TOTAL CHARGES D'EXPLOITATION",digits=(6,2))
    reb = fields.Float(string="Résultat d'Exploitation Bénéficiaire",digits=(6,2),compute="_reb")
    cf = fields.Float(string="Charges Financières",digits=(6,2))
    rfb = fields.Float(string="Résultat Finiancier Bénéficiaire",digits=(6,2),compute="_rfb")
    ch = fields.Float(string="Charges HAO",digits=(6,2))
    rhb = fields.Float(string="Résultat HAO Bénéficiaire",digits=(6,2),compute="_rhb")
    total_charges = fields.Float(string="TOTAL DES CHARGES",digits=(6,2),compute="_total_charges")
    islr = fields.Float(string="Impôts sur le Résultat",digits=(6,2))
    rb = fields.Float(string="RESULTAT BENEFICIAIRE",digits=(6,2),compute="_rb")
    total_es = fields.Float(string="TOTAL DES EFFECTIFS ET SALAIRES",digits=(6,2))
    #Produits
    vmp = fields.Float(string="VENTES DE MARCHANDISES ET PRODUITS",digits=(6,2))
    stf = fields.Float(string="SERVICES ET TRAVAUX FACTURES",digits=(6,2))
    other_products = fields.Float(string="AUTRES REVENUS",digits=(6,2),compute="_other_products")
    pa = fields.Float(string="Produits Accessoires",digits=(6,2))
    subv = fields.Float(string="Subventions",digits=(6,2))
    ap1 = fields.Float(string="Autres Produits",digits=(6,2))
    psi = fields.Float(string="Production Stockée, Immobilisée...",digits=(6,2))
    tdc = fields.Float(string="TRANSFERT DE CHARGES",digits=(6,2))
    rap = fields.Float(string="REPRISE D'AMMORTISSEMENTS ET PROVISIONS",digits=(6,2))
    #aprov = fields.Float(string="AMMORTISSEMENTS ET PROVISIONS",digits=(6,2))
    total_exp_products = fields.Float(string="Total Produits d'Exploitation",digits=(6,2))
    red = fields.Float(string="Résultat d'Exploitation Déficitaire",digits=(6,2),compute="_red")
    pf = fields.Float(string="Produits Financiers",digits=(6,2))
    rfd = fields.Float(string="Résultat Financier Déficitaire",digits=(6,2),compute="_rfd")
    ph = fields.Float(string="Produits HAO",digits=(6,2))
    rhd = fields.Float(string="Résultat HAO Déficitaire",digits=(6,2),compute="_rhd")
    total_products = fields.Float(string="TOTAL DES PRODUITS",digits=(6,2),compute="_total_products")
    rd = fields.Float(string="RESULTAT DEFICITAIRE",digits=(6,2),compute="_rd")


    @api.one
    @api.depends('tr_bt','fdc_br_log','ci','miia','mdbmi','mdtem','af','other_actif')
    def _total_actif_immobilise(self):
        self.total_actif_immobilise = self.tr_bt + self.fdc_br_log + self.ci + self.miia + self.mdbmi + self.mdtem + self.af + self.other_actif

    @api.one
    @api.depends('stock','fav','customers','cfes','ac','cca')
    def _total_actif_circulant(self):
        self.total_actif_circulant = self.stock + self.fav + self.customers + self.cfes + self.ac + self.cca

    @api.one
    @api.depends('bcctdp')
    def _total_treso_actif(self):
        self.total_treso_actif = self.bcctdp

    @api.one
    @api.depends('total_actif_immobilise','total_actif_circulant','total_treso_actif')
    def _total_actif(self):
        self.total_actif = self.total_actif_immobilise +  self.total_actif_circulant + self.total_treso_actif

    @api.one
    @api.depends('cs','act_cna','ran','ra','reserves','arpc','df','aycpr')
    def _total_capitaux_perman(self):
        self.total_capitaux_perman = self.cs + self.act_cna + self.ran + self.ra + self.reserves + self.arpc + self.df + self.aycpr

    @api.one
    @api.depends('cap','dfr','dfes','ad','pca')
    def _total_passif_circulant(self):
        self.total_passif_circulant = self.cap + self.dfr + self.dfes + self.ad + self.pca

    @api.one
    @api.depends('bcc')
    def _total_treso_passif(self):
        self.total_treso_passif = self.bcc

    @api.one
    @api.depends('total_capitaux_perman','total_passif_circulant','total_treso_passif')
    def _total_passif(self):
        self.total_passif = self.total_capitaux_perman +  self.total_passif_circulant + self.total_treso_passif

    @api.one
    @api.depends('td','seosa','seosb','ac1')
    def _other_charges(self):
        self.other_charges = self.td + self.seosa + self.seosb + self.ac1

    @api.one
    @api.depends('ampmc','vds','other_charges','it','ap','total_charges_exp','cf','ch')
    def _total_charges(self):
        self.total_charges = self.ampmc + self.vds + self.other_charges + self.it + self.ap + self.total_charges_exp + self.cf + self.ch + self.cp

    @api.one
    @api.depends('total_charges','total_products')
    def _rb(self):
        rb = self.total_products - self.total_charges
        self.rb = rb > 0 and rb or 0.00

    @api.one
    @api.depends('pa','subv','ap1','psi')
    def _other_products(self):
        self.other_products = self.pa + self.subv + self.ap1 + self.psi

    @api.one
    @api.depends('vmp','stf','other_products','tdc','rap','total_exp_products','pf','ph')
    def _total_products(self):
        self.total_products = self.vmp + self.stf + self.other_products + self.tdc + self.rap + self.total_exp_products + self.pf + self.ph

    @api.one
    @api.depends('total_charges','total_products')
    def _rd(self):
        rd = self.total_products - self.total_charges
        self.rd = rd < 0 and rd or 0.00

    @api.one
    @api.constrains('cap','dfr','dfes','ad','pca','cs','act_cna','ran','ra','reserves','arpc','df','aycpr','bcc','stock','fav','customers','cfes','ac','cca','tr_bt','fdc_br_log','ci','miia','mdbmi','mdtem','af','other_actif','bcctdp')
    def _check_actif_passif(self):
        if self.total_actif != self.total_passif:
            raise exceptions.ValidationError("L'actif et le pasif ne sont pas équilibrés ( "+str(self.total_actif)+" / "+str(self.total_passif)+" )")

    @api.one
    @api.constrains('ra','vmp','stf','pa','subv','ap1','psi','tdc','rap','total_exp_products','pf','ph','ampmc','vds','td','seosa','seosb','ac1','it','ap','total_charges_exp','cf','ch')
    def _check_net_result(self):
        if self.ra != self.rd and self.ra != self.rb:
            raise exceptions.ValidationError("le résultat Net du Bilan et du Compte de résultat ne sont pas les mêmes ! ( "+str(self.ra)+" / "+str(self.rd != 0 and self.rd or self.rb)+" )")

    @api.one
    @api.depends('total_charges_exp','total_exp_products')
    def _reb(self):
        reb = self.total_exp_products - self.total_charges_exp
        self.reb = reb > 0 and reb or 0.00

    @api.one
    @api.depends('total_charges_exp','total_exp_products')
    def _red(self):
        red = self.total_exp_products - self.total_charges_exp
        self.red = red < 0 and red or 0.004

    @api.one
    @api.depends('pf','cf')
    def _rfb(self):
        rfb = self.pf - self.cf
        self.rfb = rfb > 0 and rfb or 0.00

    @api.one
    @api.depends('pf','cf')
    def _rfd(self):
        rfd = self.pf - self.cf
        self.rfd = rfd < 0 and rfd or 0.00


    @api.one
    @api.depends('ph','ch')
    def _rhb(self):
        rhb = self.ph - self.ch
        self.rhb = rhb > 0 and rhb or 0.00

    @api.one
    @api.depends('ph','ch')
    def _rhd(self):
        rhd = self.ph - self.ch
        self.rhd = rhd < 0 and rhd or 0.00

sphere_company_fiscalyear()

