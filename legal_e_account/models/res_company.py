# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Business Applications
#    Copyright (C) 2004-2012 OpenERP S.A. (<http://openerp.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import api, fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'
        
    bad_debts_journal_id=fields.Many2one('account.journal', 'Journal')
    ledger_account_ids=fields.Many2many('account.account','ledger_accounts', 'company_id', 'account_id', 'Billing Ledger Accounts')
    bank_account_ids=fields.Many2many('account.account','bank_accounts', 'company_id', 'account_id', 'Billing Bank Accounts')
        
    
ResCompany()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: