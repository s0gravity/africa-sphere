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
    scoring = fields.Float(string="@SPHERE ONGOING SCORING",digits=(6,2))
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
    total_actif_immobilise = fields.Float(string="ACTIF IMMOBILISE",digits=(6,2))
    stock = fields.Float(string="Stocks",digits=(6,2))
    fav = fields.Float(string="Fournisseurs avance versées",digits=(6,2))
    customers = fields.Float(string="Clients",digits=(6,2))
    cfes = fields.Float(string="Créances Fiscales et Sociales",digits=(6,2))
    ac = fields.Float(string="Autres Créances",digits=(6,2))
    cca = fields.Float(string="Charges Constatées d'avance, Ecart Conv",digits=(6,2))
    total_actif_circulant = fields.Float(string="ACTIF CIRCULANT",digits=(6,2))
    bcctdp = fields.Float(string="Banques, Chèques, Caisse, Titres de placements",digits=(6,2))
    total_treso_actif = fields.Float(string="TRESORERIE ACTIF",digits=(6,2))
    total_actif = fields.Float(string="Total Actif",digits=(6,2))
    #Passif
    cs = fields.Float(string="Capital Social",digits=(6,2))
    act_cna = fields.Float(string="Actionnaire Capital Non Appelé",digits=(6,2))
    ran = fields.Float(string="Report A Nouveau",digits=(6,2))
    ra = fields.Float(string="Résultat Annuel",digits=(6,2))
    reserves = fields.Float(string="Réserves",digits=(6,2))
    arpc = fields.Float(string="Subvention, Primes, Ecart Reeval. Autres...",digits=(6,2))
    df = fields.Float(string="Dettes Financières",digits=(6,2))
    aycpr = fields.Float(string="Autres (Prov Fin. Risq et Ch.)",digits=(6,2))
    total_capitaux_perman = fields.Float(string="CAPITAUX PERMANENTS",digits=(6,2))
    cap = fields.Float(string="Clients Avances Perçues",digits=(6,2))
    dfr = fields.Float(string="Dettes Fournisseurs",digits=(6,2))
    dfes = fields.Float(string="Dettes Fiscales et Sociales",digits=(6,2))
    ad = fields.Float(string="Autres Dettes",digits=(6,2))
    pca = fields.Float(string="Produits Constatés d'Avance, Ecart Conv",digits=(6,2))
    total_passif_circulant = fields.Float(string="PASSIF CIRCULANT",digits=(6,2))
    bcc = fields.Float(string="Banques, Chèques, Caisse...",digits=(6,2))
    total_treso_passif = fields.Float(string="TRESORERIE PASSIF",digits=(6,2))
    total_passif = fields.Float(string="Total Passif",digits=(6,2))
    #COMPTE DE RESULTAT EN MONNAIE LOCALE
    #Charges
    ampmc = fields.Float(string="Achat de Mat. Prem, Marchandises et Consommables",digits=(6,2))
    vds = fields.Float(string="Variation de Stocks",digits=(6,2))
    other_charges = fields.Float(string="Autres Charges",digits=(6,2))
    td = fields.Float(string="Transport & Déplacement",digits=(6,2))
    seosa = fields.Float(string="Services Extérieur (Ohada Serv. A)",digits=(6,2))
    seosb = fields.Float(string="Services Extérieur (Ohada Serv. B)",digits=(6,2))
    ac1 = fields.Float(string="Autres Charges",digits=(6,2))
    it = fields.Float(string="IMPOTS et TAXES",digits=(6,2))
    cp = fields.Float(string="CHARGES DU PERSONNEL",digits=(6,2))
    ap = fields.Float(string="AMORTISSEMENT ET PROVISIONS",digits=(6,2))
    total_charges_exp = fields.Float(string="TOTAL CHARGES D'EXPLOITATION",digits=(6,2))
    reb = fields.Float(string="Résultat d'Exploitation Bénéficiaire",digits=(6,2))
    cf = fields.Float(string="Charges Financières",digits=(6,2))
    rfb = fields.Float(string="Résultat Finiancier Bénéficiaire",digits=(6,2))
    ch = fields.Float(string="Charges HAD",digits=(6,2))
    rhb = fields.Float(string="Résultat HAD Bénéficiaire",digits=(6,2))
    total_charges = fields.Float(string="TOTAL DES CHARGES",digits=(6,2))
    islr = fields.Float(string="Impôts sur le Résultat",digits=(6,2))
    rb = fields.Float(string="RESULTAT BENEFICIAIRE",digits=(6,2))
    total_es = fields.Float(string="TOTAL DES EFFECTIFS ET SALAIRES",digits=(6,2))
    #Produits
    vmp = fields.Float(string="VNETES DE MARCHANDISES ET PRODUITS",digits=(6,2))
    stf = fields.Float(string="SERVICES ET TRAVAUX FACTURES",digits=(6,2))
    other_products = fields.Float(string="AUTRES PRODUITS",digits=(6,2))
    pa = fields.Float(string="Produits Accessoires",digits=(6,2))
    subv = fields.Float(string="Subventions",digits=(6,2))
    ap1 = fields.Float(string="Autres Produits",digits=(6,2))
    tdc = fields.Float(string="TRANSFERT DE CHARGES",digits=(6,2))
    rap = fields.Float(string="REPRISE D'AMMORTISSEMENTS ET PROVISIONS",digits=(6,2))
    total_exp_products = fields.Float(string="Total Produits d'Exploitation",digits=(6,2))
    red = fields.Float(string="Résultat d'Exploitation Déficitaire",digits=(6,2))
    pf = fields.Float(string="Produits Financiers",digits=(6,2))
    rfd = fields.Float(string="Résultat Financier Déficitaire",digits=(6,2))
    ph = fields.Float(string="Produits HAD",digits=(6,2))
    rhd = fields.Float(string="Résultat HAD Déficitaire",digits=(6,2))
    total_products = fields.Float(string="TOTAL DES PRODUITS",digits=(6,2))
    rd = fields.Float(string="RESULTAT DEFICITAIRE",digits=(6,2))









sphere_company_fiscalyear()

