# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' :'Reports',
    'version' : '11.0',
    'summary': 'Reports for customer',
    'sequence': 30,
    'description': """

    """,
    'category': 'Management',
    'author': 'knacktechs solutions',
    'website': 'https://www.knacktechs.com',
    'depends' : ['base','account'],
    'demo': [

    ],
    'data': [
        'wizard/daily_csm_report.xml',
        'wizard/daily_collection_report_view.xml',
        'wizard/daily_crm_report_view.xml',
        'wizard/detailed_billing_report_view.xml',
        'wizard/pending_bill_report_view.xml',
        'views/india_law_custom_header.xml',
        'views/report.xml',
        'views/bill_of_cost_hdfc.xml',
        'views/hdfc_report_template.xml',
        'views/bill_of_cost_cbi.xml',
        'views/bill_of_cost_kotak.xml',
        'views/custom_india_law_page.xml',
        'views/vodafone_template.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,

}
