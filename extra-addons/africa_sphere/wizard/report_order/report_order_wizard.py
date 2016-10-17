# -*- encoding: utf-8 -*-

from openerp import models, fields, api, exceptions, _
import datetime
import os
from cStringIO import StringIO
import base64
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Alignment, Font

class report_order_wizard(models.TransientModel):
    _name = 'report.order.wizard'

    partner_id = fields.Many2one(comodel_name="res.partner", string="Client", domain=[('is_company','=',True),('customer','=',True)])
    product_id = fields.Many2one(comodel_name="product.product", string="Article", domain=[('is_report','=',True)])
    action = fields.Selection(string="Action", selection=[('new', 'Nouveau BC'), ('merge', 'Fusionner'), ], default='new')
    sale_order_id = fields.Many2one(comodel_name="sale.order", string="Bon de commande", domain=[('state','=','draft')])
    company_fiscalyear_id1 = fields.Many2one(comodel_name="account.fiscalyear", string="Exercice N")
    company_fiscalyear_id2 = fields.Many2one(comodel_name="account.fiscalyear", string="Exercice N-1")
    def _print_excel(self,report_name,model,res_id):

        if report_name == "africa_sphere.product_A_template":
            buf=StringIO()
            #############formatage des cellules###############################"
            ft= Font(name='Calibri',size=14,bold=True,italic=True,vertAlign=None,underline='none',strike=False,color='FF000000')
            ft2= Font(name='Calibri',size=12,bold=True,italic=False,vertAlign=None,underline='none',strike=False,color='FF000000')
            fl=PatternFill(fill_type='solid',start_color='FF2AF21C',end_color='FF2AF21C')
            ###############################definition du fichier excel##############
            wb = Workbook(guess_types=True)
            ws = wb.active
            ws.title = "Rapport"
            ####################################remplir la feuille excel avec les données########################################
            title1 = unicode('AFRICA SHPERE (PRODUCT A)', "utf8")
            ce=ws.cell(column=4, row=2, value=title1)
            ce.font=ft
            header = ['Country Phone code','Country name','CENTRAL BANK Activity CODE','CENTRAL BANK Activity MAIN NAME','Activity wording','COMPANY NAME',
                      'REGISTRATION NUMBER','CAPITAL = SHARES','TURNOVER YEAR-1','TURNOVER YEAR-2','NET RESULT YEAR-1','NET RESULT YEAR-2','@SPHERE ONGOING SCORING']
            header_mapping = ['country_phone_code','country_id.name','central_bank_activity_code','l_bank_activity_main','activity_wording','name',
                              'registration_number','capital','turnover_y1','turnover_y2','net_result_y1','net_result_y2','scoring']
            i = 1
            for val in header:
                ce=ws.cell(column=i, row=4, value=val)
                ce.font=ft
                ce.fill=fl
                i+=1

            j= 5
            companies = self.env['sphere.company'].search([('id','in',self._context['active_ids'])])
            for c in companies:
                i = 1
                for fld in header_mapping:
                    exec "ce=ws.cell(column=i, row=j, value=c."+fld+")"
                    ce.font=ft2
                    i+=1
                j+=1


            ###################################enrgistrement du fichier####################################
            wb.save(buf)
            fichier = self.product_id.name+".xlsx"
            out=base64.encodestring(buf.getvalue())
            buf.close()
            ###################################Pièce jointe####################################
            ir_attachment = self.env['ir.attachment'].create(
                                                              {'name': fichier,
                                                               'datas': out,
                                                               'datas_fname': fichier,
                                                               'res_model': model,
                                                               'res_id':res_id
                                                               })


        return True


    @api.multi
    def apply_pricelist(self, pricelist, product_id, qty, amount, date):
        product = self.env['product.product'].browse(product_id)
        if not pricelist:
            return amount
        else:
            ctx = dict(
                uom=product.uom_id.id,
                date=date,
            )
            #taxes
            account = product.property_account_income or product.categ_id.property_account_income_categ
            taxes = product.taxes_id or account.tax_ids
            fpos = self.env['account.fiscal.position'].browse(False)
            fp_taxes = fpos.map_tax(taxes)
            #taxes
            price = self.pool.get('product.pricelist').price_get(self._cr, self._uid, [pricelist],
                    product.id, qty or 1.0, self.partner_id.id, ctx)[pricelist]
            if price is False:
                return amount
            else:
                price = self.pool['account.tax']._fix_tax_included_price(self._cr, self._uid, price, taxes, fp_taxes.ids)
                amount = price
                #print "price unit 3 =",price_unit
                return amount

    @api.multi
    def action_make_order(self):

        if self.action == 'new':

            sale_obj = self.env['sale.order']
            payment_term = self.partner_id.property_payment_term and self.partner_id.property_payment_term.id or False
            partner_addr = self.pool.get('res.partner').address_get(self._cr, self._uid, [self.partner_id.id],['default', 'invoice', 'delivery', 'contact'])
            pricelist = self.partner_id.property_product_pricelist.id
            fpos = self.partner_id.property_account_position and self.partner_id.property_account_position.id or False
            sale_order_vals = {
                    'origin': "Report",
                    'partner_id': self.partner_id.id,
                    'pricelist_id': pricelist,
                    'partner_invoice_id': partner_addr['invoice'],
                    'partner_shipping_id': partner_addr['delivery'],
                    'date_order': fields.datetime.now(),
                    'fiscal_position': fpos,
                    'payment_term':payment_term,
                    }

            sale_order = sale_obj.create(sale_order_vals)


            price_unit = self.apply_pricelist(pricelist, self.product_id.id, 1.00, self.product_id.list_price, sale_order.date_order)
            sale_order_line_vals ={
                'order_id':sale_order.id,
                'product_id':self.product_id.id,
                'name':self.product_id.name,
                'product_uom':self.product_id.uom_id.id,
                'product_uom_qty':1,
                'price_unit':price_unit
            }

            new_line = self.env['sale.order.line'].create(sale_order_line_vals)
            new_line.tax_id = self.product_id.taxes_id


        else:
            sale_order = self.sale_order_id
            price_unit = self.apply_pricelist(sale_order.pricelist_id.id, self.product_id.id, 1.00, self.product_id.list_price, sale_order.date_order)
            sale_order_line_vals ={
                'order_id':sale_order.id,
                'product_id':self.product_id.id,
                'name':self.product_id.name,
                'product_uom':self.product_id.uom_id.id,
                'product_uom_qty':1,
                'price_unit':price_unit
            }
            new_line = self.env['sale.order.line'].create(sale_order_line_vals)
            new_line.tax_id = self.product_id.taxes_id

        #Sale report generation
        companies_string = ''
        for company_id in self._context['active_ids']:
            companies_string+=str(company_id)+','
        sale_order.companies_string = companies_string[:-1]
        sale_order.company_fiscalyear_id1=self.company_fiscalyear_id1.id
        sale_order.company_fiscalyear_id2=self.company_fiscalyear_id2.id
        if self.product_id.is_report and self.product_id.report_id:
            sale_order.sale_order_print_auto(self.product_id.report_id.report_name)
            #self._print_excel(self.product_id.report_id.report_name,'sale.order',sale_order.id)
        #Sale order redirection
        return  {
            'domain': str([('id', 'in', [sale_order.id])]),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'name' : _('Devis'),
            'res_id': sale_order.id
                    }

report_order_wizard()