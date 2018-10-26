# -*- encoding: utf-8 -*-

{
    'name': 'HR Loan and Advance Management',
    'version': '1.0',
    'category': 'Human Resources',
    'description': """Manages loan and advance feature and its effects in payslip """,
    'author': "Knacktechs Solutions",
    'website' : "http://www.knacktechs.com",
    'images': [],
    'depends': ['hr','hr_payroll','ohrms_loan'],
    # 'init_xml': [],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_view.xml',
       ],
    'demo_xml': [],
    'test': [],
    'active': False,
    'application': True,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
