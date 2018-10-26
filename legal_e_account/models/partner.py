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
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner' 
    
    @api.multi
    def search(self,args, offset=0, limit=None, order=None, context=None, count=False):
        context = self._context or {}
        emp_pool = self.env['hr.employee']
        if context.get('employee_pay', False):
            employee_ids = emp_pool.search([])
            partner_ids = []
            for emp_obj in emp_pool.browse(employee_ids):
                if emp_obj.user_id:
                    partner_ids.append(emp_obj.user_id.partner_id.id)
            args += [('id', 'in', partner_ids)]
        return super(ResPartner, self).search(args,offset=offset, limit=limit, order=order, count=count)
    
    
    
ResPartner()  

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: