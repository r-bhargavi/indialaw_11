from odoo import models, fields, api, _
from datetime import datetime


class AccountInvoice(models.Model):


    _inherit  = 'account.invoice'
    _description = "Account Invoice"


    custom_bill_date=fields.Date(string="Bill Date:", default=datetime.today())
    custom_client_reference=fields.Char(string="Client Reference")

    @api.multi
    def get_extra_rows(self, lines):
        print("-------------", lines)
        if lines < 10:
            counter = lines
            rows = ""
            while counter != 8:
                rows += "<tr>"
                for each in range(0, 6):
                    rows += "<td style='border:1px solid;height:35px;border-top:none;border-bottom:none; border-color: black;'></td>"
                rows += "</tr>"
                counter += 1
            return rows



    @api.depends('particular_invoice_line_ids.price_unit')
    def compute_text(self):
        return self.currency_id.amount_to_text(self.particular_invoice_line_ids.price_unit)




class ResPartner(models.Model):

    _inherit="res.partner"



class ResCompany(models.Model):

    _inherit="res.company"