# -*- coding: utf-8 -*-
{
    'name': 'HRMS Loan Management',
    'version': '11.0.1.0.0',
    'summary': 'Manage Loan Requests',
    'description': """
        Helps you to manage Loan Requests of your company's staff.
        """,
    'category': 'Human Resources',
    'author': "Knacktechs Solutions",
    'company': 'Knacktechs Solutions',
    'maintainer': 'Knacktechs Solutions',
    'website': "https://www.knacktechs.com",
    'depends': [
        'base', 'hr_payroll', 'hr', 'account',
    ],
    'data': [
        'wizard/message_view.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/hr_loan_seq.xml',
        'data/salary_rule_loan.xml',
        'views/hr_loan.xml',
        'views/hr_payroll.xml',
    ],
    'demo': [],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
