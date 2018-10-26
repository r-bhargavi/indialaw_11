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
from odoo import models, fields, api, _

class Output(models.TransientModel):
    _name = 'output'
    
    name = fields.Char('Company Code')
    xls_output = fields.Binary('Excel output',readonly=True)
#    _description = "Excel Output"
#    _columns = {'name':fields.char('Name',size=256),'xls_output': fields.binary('Excel output',readonly=True)}

Output()



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
