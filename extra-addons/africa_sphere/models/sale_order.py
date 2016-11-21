# -*- encoding: utf-8 -*-

from openerp import models, fields, api, _, exceptions
import openerp.addons.decimal_precision as dp
from datetime import datetime
import time
import re

class sale_order(models.Model):
    _inherit = 'sale.order'

    companies_string = fields.Char(string="Companies" )
    #informations sur commande
    document_to = fields.Char(string="DOCUMENT A L'USAGE EXCLUSIF DE")
    partners_ref = fields.Char(string="Références Clients / Ref. De la commande")
    request_date = fields.Date(string="Date de la requête")
    response_date = fields.Date(string="Date de réponse de @SPHERES")
    response_delay = fields.Integer(string="Delais de Réponse (en jours)")
    customer_internal_code = fields.Char(string="CODE CLIENT INTERNE")
    credit_solicite = fields.Float(string="ENCOURS CREDIT SOLICITE",digits=(6,2))
    credit_rec = fields.Float(string="ENCOURS CREDIT RECOMMANDE PAR @SPHERE",digits=(6,2))
    credit_approval_percent = fields.Float(string="% Accord Crédit @SPHERE",digits=(6,2))
    comment_sphere = fields.Text(string="COMMENTAIRES")
    principal_partner_ids = fields.One2many(comodel_name="principal.partner", inverse_name="sale_order_id", string="PARTENAIRES PRINCIPAUX")
    strenght1 = fields.Text(string="1")
    strenght2 = fields.Text(string="2")
    strenght3 = fields.Text(string="3")
    strenght4 = fields.Text(string="4")
    strenght5 = fields.Text(string="5")
    weakness1 = fields.Text(string="1")
    weakness2 = fields.Text(string="2")
    weakness3 = fields.Text(string="3")
    weakness4 = fields.Text(string="4")
    weakness5 = fields.Text(string="5")
    short_term_dyn = fields.Text(string="Dynamisme à Court Terme")
    short_term_risks = fields.Text(string="Risques Potentiels à Court Terme")
    company_fiscalyear_id1 = fields.Many2one(comodel_name="account.fiscalyear", string="Exercice N")
    company_fiscalyear_id2 = fields.Many2one(comodel_name="account.fiscalyear", string="Exercice N-1")
    #informations sur commande

    #Couleurs ratios
    ratio_fond_roulement = fields.Selection(string="FOND DE ROULEMENT NET = FDR", selection=[('green', 'Vert'), ('orange', 'Orange'),('red','Rouge') ])
    ratio_rotation_stock = fields.Selection(string="ROTATION DES STOCKS en jours", selection=[('green', 'Vert'), ('orange', 'Orange'),('red','Rouge') ])
    ratio_besoin_fond_roulement = fields.Selection(string="BESOIN EN FOND DE ROULEMENT = BFR", selection=[('green', 'Vert'), ('orange', 'Orange'),('red','Rouge') ])
    ratio_clients = fields.Selection(string="ROTATION DES CLIENTS en jours", selection=[('green', 'Vert'), ('orange', 'Orange'),('red','Rouge') ])
    ratio_treso_net = fields.Selection(string="TRESORERIE NETTE", selection=[('green', 'Vert'), ('orange', 'Orange'),('red','Rouge') ])
    ratio_rotation_fournisseurs = fields.Selection(string="ROTATION DES FOURNISSEURS en jours", selection=[('green', 'Vert'), ('orange', 'Orange'),('red','Rouge') ])
    ratio_liquid_test = fields.Selection(string="LIQUIDITE 'Liquid Test' EN % (> 1)", selection=[('green', 'Vert'), ('orange', 'Orange'),('red','Rouge') ])
    ratio_degree_endettement = fields.Selection(string="DEGRE ENDETTEMENT EN %", selection=[('green', 'Vert'), ('orange', 'Orange'),('red','Rouge') ])
    ratio_autonomie_financiere = fields.Selection(string="DEGRE AUTONOMIE FINANCIERE (= ou > 20%)", selection=[('green', 'Vert'), ('orange', 'Orange'),('red','Rouge') ])
    ratio_dettes_fin_cafg = fields.Selection(string="DETTES FIN. / CAFG", selection=[('green', 'Vert'), ('orange', 'Orange'),('red','Rouge') ])
    ratio_rn_caff_ht = fields.Selection(string="RN / CAFF HT % (> 0%)", selection=[('green', 'Vert'), ('orange', 'Orange'),('red','Rouge') ])
    ratio_cont_exp = fields.Selection(string="CONTINUE EXPLOITATION EN % (> 50%)", selection=[('green', 'Vert'), ('orange', 'Orange'),('red','Rouge') ])
    ratio_capacite_fin = fields.Selection(string="Capacité d'autofinancement ou CAFG", selection=[('green', 'Vert'), ('orange', 'Orange'),('red','Rouge') ])
    #Couleurs ratios


    @api.v8
    def sale_order_print_auto(self,report_name):
        html = self.env['report'].with_context({'active_ids':[self.id]}).get_html(self,report_name)
        context = self._context.copy()
        context['active_ids'] = self.ids
        pdf = self.pool.get('report').get_pdf(self._cr, self._uid, self.ids,report_name,html,context=context)
        return True

    @api.multi
    def _get_product_A_infos(self):
        infos = []
        current_year = datetime.now().strftime('%Y')
        if self.companies_string != '':
            company_ids = self.companies_string.split(',')
            for c_id in company_ids:
                company = self.env['sphere.company'].browse(int(c_id))
                vals ={
                    'name': company.name,
                    'country_phone_code': company.country_phone_code,
                    'country_name': company.country_id and company.country_id.name or '',
                    'central_bank_activity_code':company.central_bank_activity_code,
                    'l_bank_activity_main':company.l_bank_activity_main,
                    'activity_wording':company.activity_wording,
                    'name':company.name,
                    'registration_number':company.registration_number,
                    'capital':'-',
                    'turnover_y1':'-',
                    'turnover_y2':'-',
                    'net_result_y1':'-',
                    'net_result_y2':'-',
                    'scoring':'-',
                }
                if self.company_fiscalyear_id1:
                    company_fiscalyear = self.env['sphere.company.fiscalyear'].search([('sphere_company_id', '=', int(c_id)),
                                                                                       ('fiscalyear_id', '=', self.company_fiscalyear_id1.id)])
                    if company_fiscalyear:
                        vals['capital'] = company_fiscalyear.capital
                        vals['turnover_y1'] = company_fiscalyear.turnover_y1
                        vals['net_result_y1'] = company_fiscalyear.net_result_y1
                        vals['turnover_y2'] = company_fiscalyear.turnover_y2
                        vals['net_result_y2'] = company_fiscalyear.net_result_y2
                        vals['scoring'] = company_fiscalyear.scoring
                infos.append(vals)
        return infos

    @api.multi
    def _get_header_infos(self):
        vals = {
            'current_date': time.strftime('%Y/%m/%d %H:%M'),
            'current_year': time.strftime('%Y'),
        }
        return vals

    @api.multi
    def sep_f(self, float, thou=" ", dec=","):
        float = "%.1f" % float
        integer, decimal = float.split(".")
        integer = re.sub(r"\B(?=(?:\d{3})+$)", thou, integer)
        return integer + dec + decimal

    @api.multi
    def sep_i(self, float, thou=" ", dec=","):
        float = "%.1f" % float
        integer, decimal = float.split(".")
        integer = re.sub(r"\B(?=(?:\d{3})+$)", thou, integer)
        return integer

    @api.multi
    def _get_product_B_infos(self):
        infos = []
        current_year = datetime.now().strftime('%Y')
        if self.companies_string != '':
            company_ids = self.companies_string.split(',')
            for c_id in company_ids:
                company = self.env['sphere.company'].browse(int(c_id))
                vals = {
                    'current_date': time.strftime('%Y/%m/%d %H:%M'),
                    'current_year': time.strftime('%Y'),
                    'name': company.name,
                    'creation_date': company.creation_date and company.creation_date.split('-')[0] or '',
                    'nb_years_existance': company.nb_years_existance,
                    'sigle': company.sigle,
                    'legal_form': company.legal_form,
                    'num_rccm_kbis': company.num_rccm_kbis,
                    'country_id': company.country_id,
                    'city': company.city,
                    'registration_number': company.registration_number,
                    'siege_social': company.siege_social,
                    'code_act': company.code_act,
                    'name_act': company.name_act,
                    'bp': company.bp,
                    'phone': company.phone,
                    'fax': company.fax,
                    'fax': company.fax,
                    'maison_mere': company.maison_mere,
                    'maison_weight': company.maison_weight,
                    'history': company.history,
                    'company_leader_ids': company.company_leader_ids,
                    'company_shareholder_ids': False,
                    'year_n': self.company_fiscalyear_id1.name or '-',
                    'year_n_1': self.company_fiscalyear_id2.name or '-',
                    'origin': False,
                    # actif N
                    'total_ai_n': 0,
                    'total_ac_n': 0,
                    'total_ta_n': 0,
                    'total_actif_n': 0,
                    'total_ai_n_1': 0,
                    'total_ac_n_1': 0,
                    'total_ta_n_1': 0,
                    'total_actif_n_1': 0,
                    'total_ai_var': 0,
                    'total_ac_var': 0,
                    'total_ta_var': 0,
                    'total_actif_var': 0,
                    'tr_bt_n': 0,
                    'fdc_br_log_n': 0,
                    'ci_n': 0,
                    'miia_n': 0,
                    'mdbmi_n': 0,
                    'mdtem_n': 0,
                    'af_n': 0,
                    'other_actif_n': 0,
                    'stock_n': 0,
                    'fav_n': 0,
                    'customers_n': 0,
                    'cfes_n': 0,
                    'ac_n': 0,
                    'cca_n': 0,
                    'bcctdp_n': 0,
                    # passif N
                    'total_cp_n': 0,
                    'total_pc_n': 0,
                    'total_tp_n': 0,
                    'total_passif_n': 0,
                    'total_cp_n_1': 0,
                    'total_pc_n_1': 0,
                    'total_tp_n_1': 0,
                    'total_passif_n_1': 0,
                    'total_cp_var': 0,
                    'total_pc_var': 0,
                    'total_tp_var': 0,
                    'eca_var':0,
                    'ecp_var':0,
                    'total_passif_var': 0,
                    'cs_n': 0,
                    'act_cna_n': 0,
                    'ran_n': 0,
                    'ra_n': 0,
                    'reserves_n': 0,
                    'arpc_n': 0,
                    'df_n': 0,
                    'aycpr_n': 0,
                    'cap_n': 0,
                    'dfr_n': 0,
                    'dfes_n': 0,
                    'ad_n': 0,
                    'pca_n': 0,
                    'bcc_n': 0,
                    # actif N-1
                    'tr_bt_n_1': 0,
                    'fdc_br_log_n_1': 0,
                    'ci_n_1': 0,
                    'miia_n_1': 0,
                    'mdbmi_n_1': 0,
                    'mdtem_n_1': 0,
                    'af_n_1': 0,
                    'other_actif_n_1': 0,
                    'stock_n_1': 0,
                    'fav_n_1': 0,
                    'customers_n_1': 0,
                    'cfes_n_1': 0,
                    'ac_n_1': 0,
                    'cca_n_1': 0,
                    'bcctdp_n_1': 0,
                    # passif N-1
                    'cs_n_1': 0,
                    'act_cna_n_1': 0,
                    'ran_n_1': 0,
                    'ra_n_1': 0,
                    'reserves_n_1': 0,
                    'arpc_n_1': 0,
                    'df_n_1': 0,
                    'aycpr_n_1': 0,
                    'cap_n_1': 0,
                    'dfr_n_1': 0,
                    'dfes_n_1': 0,
                    'ad_n_1': 0,
                    'pca_n_1': 0,
                    'bcc_n_1': 0,
                    # Charge N
                    'ampmc_n': 0,
                    'vds_n': 0,
                    'td_n': 0,
                    'seosa_n': 0,
                    'seosb_n': 0,
                    'ac1_n': 0,
                    'it_n': 0,
                    'cp_n': 0,
                    'ap_n': 0,
                    'total_charges_exp_n': 0,
                    'reb_n': 0,
                    'cf_n': 0,
                    'rfb_n': 0,
                    'ch_n': 0,
                    'rhb_n': 0,
                    'islr_n': 0,
                    'total_es_n': 0,
                    'total_autre_charges_n': 0,
                    'total_charges_n': 0,
                    'total_beneficiaire_n': 0,
                    'ampmc_var': 0,
                    'total_autre_charges_var': 0,
                    'it_var': 0,
                    'cp_var': 0,
                    'ap_var': 0,
                    'total_charges_exp_var': 0,
                    'cf_var': 0,
                    'ch_var': 0,
                    'total_charges_var': 0,
                    'total_beneficiaire_var': 0,
                    'islr_var': 0,
                    'total_es_var': 0,
                    # Charge N-1
                    'ampmc_n_1': 0,
                    'vds_n_1': 0,
                    'td_n_1': 0,
                    'seosa_n_1': 0,
                    'seosb_n_1': 0,
                    'ac1_n_1': 0,
                    'it_n_1': 0,
                    'cp_n_1': 0,
                    'ap_n_1': 0,
                    'total_charges_exp_n_1': 0,
                    'reb_n_1': 0,
                    'cf_n_1': 0,
                    'rfb_n_1': 0,
                    'ch_n_1': 0,
                    'rhb_n_1': 0,
                    'islr_n_1': 0,
                    'total_es_n_1': 0,
                    'total_autre_charges_n_1': 0,
                    'total_charges_n_1': 0,
                    'total_beneficiaire_n_1': 0,
                    # Produit N
                    'vmp_n': 0,
                    'stf_n': 0,
                    'pa_n': 0,
                    'subv_n': 0,
                    'ap1_n': 0,
                    'tdc_n': 0,
                    'cp_n': 0,
                    'rap_n': 0,
                    'total_exp_products_n': 0,
                    'red_n': 0,
                    'pf_n': 0,
                    'rfd_n': 0,
                    'ph_n': 0,
                    'rhd_n': 0,
                    'total_autre_produits_n': 0,
                    'total_produits_n': 0,
                    'total_deficitaire_n': 0,
                    'vmp_var': 0,
                    'total_autre_produits_var': 0,
                    'tdc_var': 0,
                    'rap_var': 0,
                    'total_exp_products_var': 0,
                    'pf_var': 0,
                    'ph_var': 0,
                    'total_produits_var': 0,
                    # Produit N-1
                    'vmp_n_1': 0,
                    'stf_n_1': 0,
                    'pa_n_1': 0,
                    'subv_n_1': 0,
                    'ap1_n_1': 0,
                    'tdc_n_1': 0,
                    'cp_n_1': 0,
                    'rap_n_1': 0,
                    'total_exp_products_n_1': 0,
                    'red_n_1': 0,
                    'pf_n_1': 0,
                    'rfd_n_1': 0,
                    'ph_n_1': 0,
                    'rhd_n_1': 0,
                    'total_autre_produits_n_1': 0,
                    'total_produits_n_1': 0,
                    # ratios N
                    'fdr_n': 0,
                    'amc_n': 0,
                    'rsd_n': 0,
                    'sttc_n': 0,
                    'bfr_n': 0,
                    'rcd_n': 0,
                    'tn_n': 0,
                    'rfd_n': 0,
                    'dclt_n': 0,
                    'lt_n': 0,
                    'de_n': 0,
                    'cafg_n': 0,
                    'daf_n': 0,
                    'dfcafg_n': 0,
                    'rncaff_n': 0,
                    'cexp_n': 0,
                    'cappro_n': 0,
                    'mrcaf_n': 0,
                    # ratios N-1
                    'fdr_n_1': 0,
                    'amc_n_1': 0,
                    'rsd_n_1': 0,
                    'sttc_n_1': 0,
                    'bfr_n_1': 0,
                    'rcd_n_1': 0,
                    'tn_n_1': 0,
                    'rfd_n_1': 0,
                    'dclt_n_1': 0,
                    'lt_n_1': 0,
                    'de_n_1': 0,
                    'cafg_n_1': 0,
                    'daf_n_1': 0,
                    'dfcafg_n_1': 0,
                    'rncaff_n_1': 0,
                    'cexp_n_1': 0,
                    'cappro_n_1': 0,
                    'mrcaf_n_1': 0,
                    # ratios var
                    'fdr_var': 0,
                    'rsd_var': 0,
                    'bfr_var': 0,
                    'rcd_var': 0,
                    'tn_var': 0,
                    'rfd_var': 0,
                    'lt_var': 0,
                    'de_var': 0,
                    'cafg_var': 0,
                    'daf_var': 0,
                    'dfcafg_var': 0,
                    'rncaff_var': 0,
                    'cexp_var': 0,
                }
                tva=18
                if self.company_fiscalyear_id1:
                    company_fiscalyear_n = self.env['sphere.company.fiscalyear'].search(
                        [('sphere_company_id', '=', int(c_id)),
                         ('fiscalyear_id', '=', self.company_fiscalyear_id1.id)])
                    if company_fiscalyear_n:
                        vals['company_shareholder_ids'] = company_fiscalyear_n.company_shareholder_ids
                        vals['origin']=company_fiscalyear_n.origin
                        vals['act_comment'] = company_fiscalyear_n.act_comment
                        # actif N
                        vals['tr_bt_n']= company_fiscalyear_n.tr_bt
                        vals['fdc_br_log_n'] = company_fiscalyear_n.fdc_br_log
                        vals['ci_n']=company_fiscalyear_n.ci
                        vals['miia_n']=company_fiscalyear_n.miia
                        vals['mdbmi_n']=company_fiscalyear_n.mdbmi
                        vals['mdtem_n']=company_fiscalyear_n.mdtem
                        vals['af_n']=company_fiscalyear_n.af
                        vals['other_actif_n']=company_fiscalyear_n.other_actif
                        vals['stock_n']=company_fiscalyear_n.stock
                        vals['fav_n']=company_fiscalyear_n.fav
                        vals['customers_n']=company_fiscalyear_n.customers
                        vals['cfes_n']=company_fiscalyear_n.cfes
                        vals['ac_n']=company_fiscalyear_n.ac
                        vals['cca_n']=company_fiscalyear_n.cca
                        vals['bcctdp_n']=company_fiscalyear_n.bcctdp
                        vals['eca_n']=company_fiscalyear_n.eca
                        vals['total_ai_n']=company_fiscalyear_n.total_actif_immobilise
                        vals['total_ac_n']=company_fiscalyear_n.total_actif_circulant
                        vals['total_ta_n']=company_fiscalyear_n.total_treso_actif
                        vals['total_actif_n']=company_fiscalyear_n.total_actif
                        # passif N
                        vals['cs_n']=company_fiscalyear_n.cs
                        vals['act_cna_n']=company_fiscalyear_n.act_cna
                        vals['ran_n']=company_fiscalyear_n.ran
                        vals['ra_n']=company_fiscalyear_n.ra
                        vals['reserves_n']=company_fiscalyear_n.reserves
                        vals['arpc_n']=company_fiscalyear_n.arpc
                        vals['df_n']=company_fiscalyear_n.df
                        vals['aycpr_n']=company_fiscalyear_n.aycpr
                        vals['cap_n']=company_fiscalyear_n.cap
                        vals['dfr_n']=company_fiscalyear_n.dfr
                        vals['dfes_n']=company_fiscalyear_n.dfes
                        vals['ad_n']=company_fiscalyear_n.ad
                        vals['pca_n']=company_fiscalyear_n.pca
                        vals['bcc_n']=company_fiscalyear_n.bcc
                        vals['ecp_n']=company_fiscalyear_n.ecp
                        vals['total_cp_n']=company_fiscalyear_n.total_capitaux_perman
                        vals['total_pc_n']=company_fiscalyear_n.total_passif_circulant
                        vals['total_tp_n']=company_fiscalyear_n.total_treso_passif
                        vals['total_passif_n']=company_fiscalyear_n.total_passif
                        # Charge N
                        vals['ampmc_n']=company_fiscalyear_n.ampmc
                        vals['vds_n']=company_fiscalyear_n.vds
                        vals['td_n']=company_fiscalyear_n.td
                        vals['seosa_n']=company_fiscalyear_n.seosa
                        vals['seosb_n']=company_fiscalyear_n.seosb
                        vals['ac1_n']=company_fiscalyear_n.ac1
                        vals['it_n']=company_fiscalyear_n.it
                        vals['cp_n']=company_fiscalyear_n.cp
                        vals['ap_n']=company_fiscalyear_n.ap
                        vals['total_charges_exp_n']=company_fiscalyear_n.total_charges_exp
                        vals['reb_n']=company_fiscalyear_n.reb
                        vals['cf_n']=company_fiscalyear_n.cf
                        vals['rfb_n']=company_fiscalyear_n.rfb
                        vals['ch_n']=company_fiscalyear_n.ch
                        vals['rhb_n']=company_fiscalyear_n.rhb
                        vals['islr_n']=company_fiscalyear_n.islr
                        vals['total_es_n']=company_fiscalyear_n.total_es
                        vals['total_autre_charges_n']=company_fiscalyear_n.other_charges
                        vals['total_charges_n']=company_fiscalyear_n.total_charges
                        #vals['total_beneficiaire_n']=vals['']
                        # Produit N
                        vals['vmp_n']=company_fiscalyear_n.vmp
                        vals['stf_n']=company_fiscalyear_n.stf
                        vals['pa_n']=company_fiscalyear_n.pa
                        vals['subv_n']=company_fiscalyear_n.subv
                        vals['ap1_n']=company_fiscalyear_n.ap1
                        vals['psi_n']=company_fiscalyear_n.psi
                        vals['tdc_n']=company_fiscalyear_n.tdc
                        vals['cp_n']=company_fiscalyear_n.cp
                        vals['rap_n']=company_fiscalyear_n.rap
                        vals['total_exp_products_n']=company_fiscalyear_n.total_exp_products
                        vals['red_n']=company_fiscalyear_n.red
                        vals['pf_n']=company_fiscalyear_n.pf
                        vals['rfd_n']=company_fiscalyear_n.rfd
                        vals['ph_n']=company_fiscalyear_n.ph
                        vals['rhd_n']=company_fiscalyear_n.rhd
                        vals['total_autre_produits_n']=company_fiscalyear_n.other_products
                        vals['total_produits_n']=company_fiscalyear_n.total_products
                        # ratios N
                        vals['fdr_n']=vals['total_cp_n']-vals['total_ai_n']
                        vals['amc_n']=int(round(vals['ampmc_n']+(vals['ampmc_n']*tva)/100))
                        if vals['amc_n']!=0:
                            vals['rsd_n']=int(round((vals['stock_n']/vals['amc_n'])*365))
                        vals['sttc_n']=int(round(vals['vmp_n']+(vals['vmp_n']*tva)/100))
                        vals['bfr_n']=vals['total_ac_n']-vals['total_pc_n']
                        if vals['sttc_n'] != 0:
                            vals['rcd_n'] = int(round((vals['customers_n'] / vals['sttc_n']) * 365))
                        vals['tn_n'] = vals['fdr_n'] - vals['bfr_n']
                        vals['pttc_n'] = vals['amc_n']
                        if vals['pttc_n'] != 0:
                            vals['rfd_n'] = int(round((vals['dfes_n'] / vals['pttc_n']) * 365))
                        if vals['total_pc_n'] != 0:
                            vals['lt_n'] = round((vals['total_ac_n'] / vals['total_pc_n'])*100,2)
                        vals['dclt_n']=vals['total_pc_n']+vals['df_n']
                        if vals['total_ac_n'] != 0:
                            vals['de_n'] = round((vals['dclt_n'] / vals['total_actif_n'])*100,1)
                        vals['cafg_n']=vals['ra_n']+vals['ap_n']-vals['rap_n']+vals['ch_n']-vals['ph_n']
                        if vals['total_actif_n'] != 0:
                            vals['daf_n'] = int(round((vals['total_cp_n'] / vals['total_actif_n']) * 100))
                        if vals['cafg_n'] != 0:
                            vals['dfcafg_n'] = vals['df_n'] / vals['cafg_n']
                        if vals['vmp_n'] != 0:
                            vals['rncaff_n'] = round((vals['ra_n'] / vals['vmp_n']) * 100,2)
                        vals['cappro_n'] = vals['total_cp_n'] - vals['df_n']
                        if vals['cs_n'] != 0:
                            vals['cexp_n'] = round((vals['cappro_n'] / vals['cs_n']) * 100,2)
                        vals['mrcaf_n']=vals['cappro_n']/2-vals['total_cp_n']

                if self.company_fiscalyear_id2:
                    company_fiscalyear_n_1 = self.env['sphere.company.fiscalyear'].search(
                        [('sphere_company_id', '=', int(c_id)),
                         ('fiscalyear_id', '=', self.company_fiscalyear_id2.id)])
                    if company_fiscalyear_n_1:
                        # actif N-1
                        vals['tr_bt_n_1']=company_fiscalyear_n_1.tr_bt
                        vals['fdc_br_log_n_1'] = company_fiscalyear_n_1.fdc_br_log
                        vals['ci_n_1']=company_fiscalyear_n_1.ci
                        vals['miia_n_1']=company_fiscalyear_n_1.miia
                        vals['mdbmi_n_1']=company_fiscalyear_n_1.mdbmi
                        vals['mdtem_n_1']=company_fiscalyear_n_1.mdtem
                        vals['af_n_1']=company_fiscalyear_n_1.af
                        vals['other_actif_n_1']=company_fiscalyear_n_1.other_actif
                        vals['stock_n_1']=company_fiscalyear_n_1.stock
                        vals['fav_n_1']=company_fiscalyear_n_1.fav
                        vals['customers_n_1']=company_fiscalyear_n_1.customers
                        vals['cfes_n_1']=company_fiscalyear_n_1.cfes
                        vals['ac_n_1']=company_fiscalyear_n_1.ac
                        vals['cca_n_1']=company_fiscalyear_n_1.cca
                        vals['bcctdp_n_1']=company_fiscalyear_n_1.bcctdp
                        vals['eca_n_1']=company_fiscalyear_n_1.eca
                        vals['total_ai_n_1']=company_fiscalyear_n_1.total_actif_immobilise
                        vals['total_ac_n_1']=company_fiscalyear_n_1.total_actif_circulant
                        vals['total_ta_n_1']=company_fiscalyear_n_1.total_treso_actif
                        vals['total_actif_n_1']=company_fiscalyear_n_1.total_actif
                        # passif N-1
                        vals['cs_n_1']=company_fiscalyear_n_1.cs
                        vals['act_cna_n_1'] = company_fiscalyear_n_1.act_cna
                        vals['ran_n_1']=company_fiscalyear_n_1.ran
                        vals['ra_n_1']=company_fiscalyear_n_1.ra
                        vals['reserves_n_1']=company_fiscalyear_n_1.reserves
                        vals['arpc_n_1']=company_fiscalyear_n_1.arpc
                        vals['df_n_1']=company_fiscalyear_n_1.df
                        vals['aycpr_n_1']=company_fiscalyear_n_1.aycpr
                        vals['cap_n_1']=company_fiscalyear_n_1.cap
                        vals['dfr_n_1']=company_fiscalyear_n_1.dfr
                        vals['dfes_n_1']=company_fiscalyear_n_1.dfes
                        vals['ad_n_1']=company_fiscalyear_n_1.ad
                        vals['pca_n_1']=company_fiscalyear_n_1.pca
                        vals['bcc_n_1']=company_fiscalyear_n_1.bcc
                        vals['ecp_n_1']=company_fiscalyear_n_1.ecp
                        vals['total_cp_n_1']=company_fiscalyear_n_1.total_capitaux_perman
                        vals['total_pc_n_1']=company_fiscalyear_n_1.total_passif_circulant
                        vals['total_tp_n_1']=company_fiscalyear_n_1.total_treso_passif
                        vals['total_passif_n_1']=company_fiscalyear_n_1.total_passif
                        # Charge N-1
                        vals['ampmc_n_1'] = company_fiscalyear_n_1.ampmc
                        vals['vds_n_1'] = company_fiscalyear_n_1.vds
                        vals['td_n_1'] = company_fiscalyear_n_1.td
                        vals['seosa_n_1'] = company_fiscalyear_n_1.seosa
                        vals['seosb_n_1'] = company_fiscalyear_n_1.seosb
                        vals['ac1_n_1'] = company_fiscalyear_n_1.ac1
                        vals['it_n_1'] = company_fiscalyear_n_1.it
                        vals['cp_n_1'] = company_fiscalyear_n_1.cp
                        vals['ap_n_1'] = company_fiscalyear_n_1.ap
                        vals['total_charges_exp_n_1'] = company_fiscalyear_n_1.total_charges_exp
                        vals['reb_n_1'] = company_fiscalyear_n_1.reb
                        vals['cf_n_1'] = company_fiscalyear_n_1.cf
                        vals['rfb_n_1'] = company_fiscalyear_n_1.rfb
                        vals['ch_n_1'] = company_fiscalyear_n_1.ch
                        vals['rhb_n_1'] = company_fiscalyear_n_1.rhb
                        vals['islr_n_1'] = company_fiscalyear_n_1.islr
                        vals['total_es_n_1'] = company_fiscalyear_n_1.total_es
                        vals['total_autre_charges_n_1'] = company_fiscalyear_n_1.other_charges
                        vals['total_charges_n_1'] = company_fiscalyear_n_1.total_charges
                        #vals['total_beneficiaire_n_1'] = vals['']
                        # Produit N-1
                        vals['vmp_n_1'] = company_fiscalyear_n_1.vmp
                        vals['stf_n_1'] = company_fiscalyear_n_1.stf
                        vals['pa_n_1'] = company_fiscalyear_n_1.pa
                        vals['subv_n_1'] = company_fiscalyear_n_1.subv
                        vals['ap1_n_1'] = company_fiscalyear_n_1.ap1
                        vals['psi_n_1']=company_fiscalyear_n_1.psi
                        vals['tdc_n_1'] = company_fiscalyear_n_1.tdc
                        vals['cp_n_1'] = company_fiscalyear_n_1.cp
                        vals['rap_n_1'] = company_fiscalyear_n_1.rap
                        vals['total_exp_products_n_1'] = company_fiscalyear_n_1.total_exp_products
                        vals['red_n_1'] = company_fiscalyear_n_1.red
                        vals['pf_n_1'] = company_fiscalyear_n_1.pf
                        vals['rfd_n_1'] = company_fiscalyear_n_1.rfd
                        vals['ph_n_1'] = company_fiscalyear_n_1.ph
                        vals['rhd_n_1'] = company_fiscalyear_n_1.rhd
                        vals['total_autre_produits_n_1'] = company_fiscalyear_n_1.other_products
                        vals['total_produits_n_1'] = company_fiscalyear_n_1.total_products
                        # ratios N-1
                        vals['fdr_n_1'] = vals['total_cp_n_1'] - vals['total_ai_n_1']
                        vals['amc_n_1'] = int(round(vals['ampmc_n_1'] + (vals['ampmc_n_1'] * tva) / 100))
                        if vals['amc_n_1'] != 0:
                            vals['rsd_n_1'] = int(round((vals['stock_n_1'] / vals['amc_n_1']) * 365))
                        vals['sttc_n_1'] = int(round(vals['vmp_n_1'] + (vals['vmp_n_1'] * tva) / 100))
                        vals['bfr_n_1'] = vals['total_ac_n_1'] - vals['total_pc_n_1']
                        if vals['sttc_n_1'] != 0:
                            vals['rcd_n_1'] = int(round((vals['customers_n_1'] / vals['sttc_n_1']) * 365))
                        vals['tn_n_1'] = vals['fdr_n_1'] - vals['bfr_n_1']
                        vals['pttc_n_1'] = vals['amc_n_1']
                        if vals['pttc_n_1'] != 0:
                            vals['rfd_n_1'] = int(round((vals['dfes_n_1'] / vals['pttc_n_1']) * 365))
                        if vals['total_pc_n_1'] != 0:
                            vals['lt_n_1'] = round((vals['total_ac_n_1'] / vals['total_pc_n_1'])*100, 2)
                        vals['dclt_n_1'] = vals['total_pc_n_1'] + vals['df_n_1']
                        if vals['total_ac_n_1'] != 0:
                            vals['de_n_1'] = round((vals['dclt_n_1'] / vals['total_actif_n_1']) * 100, 1)
                        vals['cafg_n_1'] = vals['ra_n_1'] + vals['ap_n_1'] - vals['rap_n_1'] + vals['ch_n_1'] - vals['ph_n_1']
                        if vals['total_actif_n_1'] != 0:
                            vals['daf_n_1'] = int(round((vals['total_cp_n_1'] / vals['total_actif_n_1']) * 100))
                        if vals['cafg_n_1'] != 0:
                            vals['dfcafg_n_1'] = vals['df_n_1'] / vals['cafg_n_1']
                        if vals['vmp_n_1'] != 0:
                            vals['rncaff_n_1'] = round((vals['ra_n_1'] / vals['vmp_n_1']) * 100,2)
                        vals['cappro_n_1'] = vals['total_cp_n_1'] - vals['df_n_1']
                        if vals['cs_n_1'] != 0:
                            vals['cexp_n_1'] = round((vals['cappro_n_1'] / vals['cs_n_1']) * 100,2)
                        vals['mrcaf_n_1'] = vals['cappro_n_1'] / 2 - vals['total_cp_n_1']

                # var actif
                if isinstance(vals['total_ai_n'], float) == True and isinstance(vals['total_ai_n_1'], float) == True and vals['total_ai_n_1'] != 0:
                    vals['total_ai_var']=int(round(((vals['total_ai_n']-vals['total_ai_n_1'])/vals['total_ai_n_1'])*100))
                if isinstance(vals['total_ac_n'], float) == True and isinstance(vals['total_ac_n_1'], float) == True and vals['total_ac_n_1'] != 0:
                    vals['total_ac_var'] = int(round(((vals['total_ac_n']-vals['total_ac_n_1'])/vals['total_ac_n_1'])*100))
                if isinstance(vals['total_ta_n'], float) == True and isinstance(vals['total_ta_n_1'], float) == True and vals['total_ta_n_1'] != 0:
                    vals['total_ta_var'] = int(round((((vals['total_ta_n'] - vals['total_ta_n_1']) / vals['total_ta_n_1']) * 100)))
                if isinstance(vals['total_actif_n'], float) == True and isinstance(vals['total_actif_n_1'], float) == True and vals['total_actif_n_1'] != 0:
                    vals['total_actif_var'] = int(round((((vals['total_actif_n'] - vals['total_actif_n_1']) / vals['total_actif_n_1']) * 100)))
                if isinstance(vals['eca_n'], float) == True and isinstance(vals['eca_n_1'], float) == True and vals['eca_n_1'] != 0:
                    vals['eca_var'] = int(round((((vals['eca_n'] - vals['eca_n_1']) / vals['eca_n_1']) * 100)))
                # var passif
                if isinstance(vals['total_cp_n'], float) == True and isinstance(vals['total_cp_n_1'], float) == True and vals['total_cp_n_1'] != 0:
                    vals['total_cp_var'] = int(round((((vals['total_cp_n'] - vals['total_cp_n_1']) / vals['total_cp_n_1']) * 100)))
                if isinstance(vals['total_pc_n'], float) == True and isinstance(vals['total_pc_n_1'], float) == True and vals['total_pc_n_1'] != 0:
                    vals['total_pc_var'] = int(round((((vals['total_pc_n'] - vals['total_pc_n_1']) / vals['total_pc_n_1']) * 100)))
                if isinstance(vals['total_tp_n'], float) == True and isinstance(vals['total_tp_n_1'], float) == True and vals['total_tp_n_1'] != 0:
                    vals['total_tp_var'] = int(round((((vals['total_tp_n'] - vals['total_tp_n_1']) / vals['total_tp_n_1']) * 100)))
                if isinstance(vals['total_passif_n'], float) == True and isinstance(vals['total_passif_n_1'], float) == True and vals['total_passif_n_1'] != 0:
                    vals['total_passif_var'] = int(round((((vals['total_passif_n'] - vals['total_passif_n_1']) / vals['total_passif_n_1']) * 100)))
                if isinstance(vals['ecp_n'], float) == True and isinstance(vals['ecp_n_1'], float) == True and vals['ecp_n_1'] != 0:
                    vals['ecp_var'] = int(round((((vals['ecp_n'] - vals['ecp_n_1']) / vals['ecp_n_1']) * 100)))
                # var charges
                if isinstance(vals['ampmc_n'], float)==True and isinstance(vals['ampmc_n_1'], float)==True and vals['ampmc_n_1'] != 0:
                    vals['ampmc_var'] = int(round((((vals['ampmc_n'] - vals['ampmc_n_1']) / vals['ampmc_n_1']) * 100)))
                if isinstance(vals['total_autre_charges_n'], float) and isinstance(vals['total_autre_charges_n_1'], float) and vals['total_autre_charges_n_1'] != 0:
                    vals['total_autre_charges_var'] = int(round((((vals['total_autre_charges_n'] - vals['total_autre_charges_n_1']) / vals['total_autre_charges_n_1']) * 100)))
                if isinstance(vals['it_n'], float) and isinstance(vals['it_n_1'], float) and vals['it_n_1'] != 0:
                    vals['it_var'] = int(round((((vals['it_n'] - vals['it_n_1']) / vals['it_n_1']) * 100)))
                if isinstance(vals['cp_n'], float) and isinstance(vals['cp_n_1'], float) and vals['cp_n_1'] != 0:
                    vals['cp_var'] = int(round((((vals['cp_n'] - vals['cp_n_1']) / vals['cp_n_1']) * 100)))
                if isinstance(vals['ap_n'], float) and isinstance(vals['ap_n_1'], float) and vals['ap_n_1'] != 0:
                    vals['ap_var'] = int(round((((vals['ap_n'] - vals['ap_n_1']) / vals['ap_n_1']) * 100)))
                if isinstance(vals['total_charges_exp_n'], float) and isinstance(vals['total_charges_exp_n_1'], float) and vals['total_charges_exp_n_1'] != 0:
                    vals['total_charges_exp_var'] = int(round((((vals['total_charges_exp_n'] - vals['total_charges_exp_n_1']) / vals['total_charges_exp_n_1']) * 100)))
                if isinstance(vals['cf_n'], float) and isinstance(vals['cf_n_1'], float) and vals['cf_n_1'] != 0:
                    vals['cf_var'] = int(round((((vals['cf_n'] - vals['cf_n_1']) / vals['cf_n_1']) * 100)))
                if isinstance(vals['ch_n'], float) and isinstance(vals['ch_n_1'], float) and vals['ch_n_1'] != 0:
                    vals['ch_var'] = int(round((((vals['ch_n'] - vals['ch_n_1']) / vals['ch_n_1']) * 100)))
                if isinstance(vals['total_charges_n'], float) and isinstance(vals['total_charges_n_1'], float) and vals['total_charges_n_1'] != 0:
                    vals['total_charges_var'] = int(round((((vals['total_charges_n'] - vals['total_charges_n_1']) / vals['total_charges_n_1']) * 100)))
                if isinstance(vals['total_beneficiaire_n'], float) and isinstance(vals['total_beneficiaire_n_1'], float) and vals['total_beneficiaire_n_1'] != 0:
                    vals['total_beneficiaire_var'] = int(round((((vals['total_beneficiaire_n'] - vals['total_beneficiaire_n_1']) / vals['total_beneficiaire_n_1']) * 100)))
                if isinstance(vals['islr_n'], float) and isinstance(vals['islr_n_1'], float) and vals['islr_n_1'] != 0:
                    vals['islr_var'] = int(round((((vals['islr_n'] - vals['islr_n_1']) / vals['islr_n_1']) * 100)))
                if isinstance(vals['total_es_n'], float) and isinstance(vals['total_es_n_1'], float) and vals['total_es_n_1'] != 0:
                    vals['total_es_var'] = int(round((((vals['total_es_n'] - vals['total_es_n_1']) / vals['total_es_n_1']) * 100)))
                # var produits
                if isinstance(vals['vmp_n'], float) and isinstance(vals['vmp_n_1'], float) and vals['vmp_n_1'] != 0:
                    vals['vmp_var'] = int(round((((vals['vmp_n'] - vals['vmp_n_1']) / vals['vmp_n_1']) * 100)))
                if isinstance(vals['total_autre_produits_n'], float) and isinstance(vals['total_autre_produits_n_1'], float) and vals['total_autre_produits_n_1'] != 0:
                    vals['total_autre_produits_var'] = int(round((((vals['total_autre_produits_n'] - vals['total_autre_produits_n_1']) / vals['total_autre_produits_n_1']) * 100)))
                if isinstance(vals['tdc_n'], float) and isinstance(vals['tdc_n_1'], float) and vals['tdc_n_1'] != 0:
                    vals['tdc_var'] = int(round((((vals['tdc_n'] - vals['tdc_n_1']) / vals['tdc_n_1']) * 100)))
                if isinstance(vals['rap_n'], float) and isinstance(vals['rap_n_1'], float) and vals['rap_n_1'] != 0:
                    vals['rap_var'] = int(round((((vals['rap_n'] - vals['rap_n_1']) / vals['rap_n_1']) * 100)))
                if isinstance(vals['total_exp_products_n'], float) and isinstance(vals['total_exp_products_n_1'], float) and vals['total_exp_products_n_1'] != 0:
                    vals['total_exp_products_var'] = int(round((((vals['total_exp_products_n'] - vals['total_exp_products_n_1']) / vals['total_exp_products_n_1']) * 100)))
                if isinstance(vals['pf_n'], float) and isinstance(vals['pf_n_1'], float) and vals['pf_n_1'] != 0:
                    vals['pf_var'] = int(round((((vals['pf_n'] - vals['pf_n_1']) / vals['pf_n_1']) * 100)))
                if isinstance(vals['ph_n'], float) and isinstance(vals['ph_n_1'], float) and vals['ph_n_1'] != 0:
                    vals['ph_var'] = int(round((((vals['ph_n'] - vals['ph_n_1']) / vals['ph_n_1']) * 100)))
                if isinstance(vals['total_produits_n'], float) and isinstance(vals['total_produits_n_1'], float) and vals['total_produits_n_1'] != 0:
                    vals['total_produits_var'] = int(round((((vals['total_produits_n'] - vals['total_produits_n_1']) / vals['total_produits_n_1']) * 100)))
                # var ratios
                if isinstance(vals['fdr_n'], float) and isinstance(vals['fdr_n_1'], float) and vals['fdr_n_1'] != 0:
                    vals['fdr_var'] = int(round((((vals['fdr_n'] - vals['fdr_n_1']) / vals['fdr_n_1']) * 100)))
                if isinstance(vals['rsd_n'], int) and isinstance(vals['rsd_n_1'], int) and vals['rsd_n_1'] != 0:
                    vals['rsd_var'] = int(round((((vals['rsd_n'] - vals['rsd_n_1']) / float(vals['rsd_n_1'])) * 100)))
                if isinstance(vals['bfr_n'], float) and isinstance(vals['bfr_n_1'], float) and vals['bfr_n_1'] != 0:
                    vals['bfr_var'] = int(round((((vals['bfr_n'] - vals['bfr_n_1']) / vals['bfr_n_1']) * 100)))
                if isinstance(vals['rsd_n'], int) and isinstance(vals['rsd_n_1'], int) and vals['rsd_n_1'] != 0:
                    vals['rcd_var'] = int(round((((vals['rcd_n'] - vals['rcd_n_1']) / float(vals['rcd_n_1'])) * 100)))
                if isinstance(vals['tn_n'], float) and isinstance(vals['tn_n_1'], float) and vals['tn_n_1'] != 0:
                    vals['tn_var'] = int(round((((vals['tn_n'] - vals['tn_n_1']) / vals['tn_n_1']) * 100)))
                if isinstance(vals['rfd_n'], int) and isinstance(vals['rfd_n_1'], int) and vals['rsd_n_1'] != 0:
                    vals['rfd_var'] = int(round((((vals['rfd_n'] - vals['rfd_n_1']) / float(vals['rfd_n_1'])) * 100)))
                if isinstance(vals['lt_n'], float) and isinstance(vals['lt_n_1'], float) and vals['lt_n_1'] != 0:
                    vals['lt_var'] = int(round((((vals['lt_n'] - vals['lt_n_1']) / vals['lt_n_1']) * 100)))
                if isinstance(vals['de_n'], float) and isinstance(vals['de_n_1'], float) and vals['de_n_1'] != 0:
                    vals['de_var'] = int(round((((vals['de_n'] - vals['de_n_1']) / vals['de_n_1']) * 100)))
                if isinstance(vals['cafg_n'], float) and isinstance(vals['cafg_n_1'], float) and vals['cafg_n_1'] != 0:
                    vals['cafg_var'] = int(round((((vals['cafg_n'] - vals['cafg_n_1']) / vals['cafg_n_1']) * 100)))
                if isinstance(vals['daf_n'], int) and isinstance(vals['daf_n_1'], int) and vals['daf_n_1'] != 0:
                    vals['daf_var'] = int(round((((vals['daf_n'] - vals['daf_n_1']) / float(vals['daf_n_1'])) * 100)))
                if isinstance(vals['dfcafg_n'], float) and isinstance(vals['dfcafg_n_1'], float) and vals['dfcafg_n_1'] != 0:
                    vals['dfcafg_var'] = int(round((((vals['dfcafg_n'] - vals['dfcafg_n_1']) / float(vals['dfcafg_n_1'])) * 100)))
                if isinstance(vals['rncaff_n'], float) and isinstance(vals['rncaff_n_1'], float) and vals['rncaff_n_1'] != 0:
                    vals['rncaff_var'] = int(round((((vals['rncaff_n'] - vals['rncaff_n_1']) / vals['rncaff_n_1']) * 100)))
                if isinstance(vals['cexp_n'], float) and isinstance(vals['cexp_n_1'], float) and vals['cexp_n_1'] != 0:
                    vals['cexp_var'] = int(round((((vals['cexp_n'] - vals['cexp_n_1']) / vals['cexp_n_1']) * 100)))

                infos.append(vals)
        return infos

sale_order()


