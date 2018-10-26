# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    company_pan_no=fields.Char('PAN Number', size=40)
    expense_account_ids= fields.Many2many('account.account', 'company_accounts', 'company_id', 'account_id','Expense Accounts')
    proceed_stage_id= fields.Many2one('court.proceedings.stage', 'Closing Stage')



ResCompany()