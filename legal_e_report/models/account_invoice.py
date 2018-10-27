# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from datetime import datetime
from num2words import num2words

class AccountInvoice(models.Model):


    _inherit  = 'account.invoice'
    _description = "Account Invoice"


    custom_bill_date=fields.Date(string="Bill Date:", default=datetime.today())
    custom_client_reference=fields.Char(string="Client Reference")

    @api.multi
    def get_extra_rows(self, lines):
        if lines < 10:
            counter = lines
            rows = ""
            while counter != 8:
                rows += "<tr>"
                for each in range(0, 3):
                    rows += "<td style='border:1px solid;height:35px;border-top:none;border-bottom:none; border-color: black;'></td>"
                rows += "</tr>"
                counter += 1
            return rows

    def get_num2words_amount(self, amount):
        amt_word = num2words(amount, lang='en_IN').replace('point', 'rupees and')
        print('-------------',amt_word)
        amt_word = str(amt_word).title()
        return amt_word + ' Only'



#class ResPartner(models.Model):
#
#    _inherit="res.partner"
#
#
#
#class ResCompany(models.Model):
#
#    _inherit="res.company"