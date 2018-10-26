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
from datetime import datetime, timedelta
import time

from odoo import api, fields, models
from odoo.tools.translate import _
from odoo.exceptions import ValidationError

class BulkAccountFollowup(models.TransientModel):
    
    _name = 'bulk.account.followup'
    _description = 'Bulk Account Followup'
    
    
    date=fields.Date('Date')
    name=fields.Text('Description')
    next_date=fields.Date('Next Date')
    state=fields.Selection([('communicate', 'To Communicate'),('communicated', 'Communicated'),('completed', 'Completed')], 'Status')
    communicate_via=fields.Selection([('email', 'Email'),('phone', 'Phone'),('meeting', 'Meeting')], 'Communicated Via')
        
    @api.multi
    def create_bulk_account_followup(self):
        context = self._context or {}
        bill_follow_pool = self.env['consolidated.bill.followup']
        invoice_follow_pool = self.env['account.invoice.followup']
        bill_pool = self.env['consolidated.bill']
        invoice_pool = self.env['account.invoice']
        active_ids = context.get('active_ids', False)
        for data in self:
            current_date = time.strftime('%Y-%m-%d')
            if data.date > current_date:
#                raise osv.except_osv(_('Error'),_('Future date selection restricted.'))
                raise ValidationError(_('Error'),_('Future date selection restricted.'))
            today = datetime.today()
            selected_date = datetime.strptime(data.date, '%Y-%m-%d')
            if selected_date.strftime("%U") != today.strftime("%U"):
#                raise osv.except_osv(_('Error'),_("The 'Date' must be in the current week."))
                raise ValidationError(_('Error'),_("The 'Date' must be in the current week."))
            vals = {
                'date': data.date,
                'name': data.name,
                'next_date': data.next_date,
                'state': data.state,
                'communicate_via': data.communicate_via,
                }
            if context.get('active_model', False) == 'account.invoice':
                for invoice_obj in invoice_pool.browse(active_ids):
                    vals.update({'invoice_id': invoice_obj.id})
                    invoice_follow_pool.create(vals)
            else:
                for bill_obj in bill_pool.browse(active_ids):
                    vals.update({'bill_id': bill_obj.id})
                    bill_follow_pool.create(vals)
                    
        return True
        
BulkAccountFollowup()
