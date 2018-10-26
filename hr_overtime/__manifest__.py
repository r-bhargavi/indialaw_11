# -*- coding: utf-8 -*-
{
    "name": "Human Resources Overtime Management",
    "version": "1.0",
    "author": "Zesty Beanz Technologies",
    "category": "Human Resources",
    "website": "www.zbeanztech.com",
    "description": """Human Resources: Overtime tracking and workflow""",
    'depends': ['base','hr','resource'],
    'init_xml': [],
    'data': [
#              'report.xml',
            'security/ir_rule.xml',
            'security/ir.model.access.csv',
            'views/hr_overtime_view.xml',
             # 'hr_overtime_workflow.xml',

             ],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'certificate': '',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: