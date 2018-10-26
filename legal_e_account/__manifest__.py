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


{
    'name': 'Legal Account Customization',
    'version': '1.1',
    'category': 'Customized integration',
    'author': 'BroadTech It Solutions Pvt Ltd.',
    'website': 'http://www.broadtech-innovations.com/',
    'description': """
Account Customization

    """,
    'depends': [
        'legal_e',
        'account_cancel'
    ],
    'data': [
#         'security/security.xml',
#         'security/ir.model.access.csv',
         'views/res_company_view.xml',
         'views/account_view.xml',
#         'wizard/success_msg_view.xml',
        'wizard/check_print_view.xml',
#         'views/account_report.xml',
#         'views/invoice_sequence.xml',
         'views/purchase_view.xml',
         'wizard/account_statement_from_invoice_view.xml',
         'views/account_bank_statement_view.xml',
         'wizard/bulk_account_followup_view.xml',
         
         
         ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
