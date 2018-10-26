# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from openerp.osv import fields, osv

class bank_recon(osv.osv_memory):
    _name = "legale.bank.recon"
    _description = "Bank Reconciliation"
    
    from_date=fields.date('From'),
    to_date=fields.date('To'),
    journal_id=fields.many2one('account.journal', 'Journal'),       
    
    
    @api.multi
    def print_check(self):
        for data in self:
            datas = {
                 'ids': data.id,
                 'model': 'account.voucher',
                 'form': {
                    'partner_id': data.partner_id.name,
                    'amount': data.amount,
                    'date': data.date,
                    'acc_payee': data.acc_payee,
                    }
                  }
            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'check.print',
                'datas': datas,
                'nodestroy': True,
                }
        return True

bank_recon()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
