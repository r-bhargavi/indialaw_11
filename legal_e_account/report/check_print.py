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

import time
from datetime import datetime
from legal_e_account.report.Number2Words import Number2Words
from openerp.report import report_sxw

class print_check(report_sxw.rml_parse):
    _name = 'report.check.print'
    def __init__(self, cr, uid, name, context=None):
        super(print_check, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time, 
            'get_amt_inwords': self.get_amt_inwords,
            'get_date': self.get_date,
        })
    
    
    
    def get_amt_inwords(self, total):
        wGenerator = Number2Words()
        amt_in_words =  wGenerator.convertNumberToWords(total) + ' Only.'
        return amt_in_words
    
        
    def get_date(self, dt, position):
        date = datetime.strptime(str(dt), '%Y-%m-%d').strftime('%d-%m-%Y')
        date = date.replace('-', '')
        return date[position]
    

report_sxw.report_sxw('report.check.print', 'account.voucher', 'addons/legal_e_account/report/check_print.rml', parser=print_check, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: