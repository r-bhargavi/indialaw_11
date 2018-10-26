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
        'views/india_law_custom_header.xml',
        'views/kotak_page_format.xml',
        'views/cbi_page_format.xml',
        'views/hdfc_page_format.xml',
        'views/bill_of_cost_hdfc.xml',
        'views/bill_of_cost_cbi.xml',
        'views/bill_of_cost_kotak.xml',
        'views/custom_india_law_page.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,

}
