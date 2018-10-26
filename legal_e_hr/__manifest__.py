# -*- coding: utf-8 -*-
{
    'name': 'Legal Hr Customization',
    'version': '1.20',
    'category': 'Customized integration',
    'author': 'BroadTech It Solutions Pvt Ltd.',
    'website': 'http://www.broadtech-innovations.com/',
    'description': """
Hr Customization

    """,
    'depends': ['legal_e', 'hr_payroll', 'hr_overtime', 'hr_attendance','hr_holidays',
    ],
# 'hr_loan_advance'
    'data': [
         # 'edi/hr_holiday_data.xml',
         'views/hr_attendance_view.xml',
         'views/hr_view.xml',
         'security/ir.model.access.csv',
         'security/hr_security.xml',
         'views/hr_payroll_data.xml',
         'views/hr_payroll_view.xml',
         # 'hr_expense_workflow.xml',
         'views/hr_data.xml',
         'views/res_company_view.xml',
         # 'hr_holidays_workflow.xml'
         ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
