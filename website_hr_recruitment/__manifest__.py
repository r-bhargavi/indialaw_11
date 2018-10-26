# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Online Jobs',
    'category': 'Website',
    'sequence': 142,
    'version': '1.0',
    'summary': 'Job Descriptions And Application Forms',
    'description': "",
    'depends': ['website_partner', 'hr_recruitment', 'website_mail', 'website_form','website'],
    'data': [
        'data/practice_area_master_demo_data.xml',
        'data/year_master_demo_data.xml',
        'data/designation_demo_data.xml',
        'data/degree_demo_data.xml',
        'data/college_demo_data.xml',
        'security/ir.model.access.csv',
        'security/website_hr_recruitment_security.xml',
        'data/config_data.xml',
        'views/website_hr_recuitment_snippets.xml',
        'views/website_hr_recruitment_templates.xml',
        'views/hr_recruitment_views.xml',
        'views/hr_applicant_inherit_view.xml',
        'views/job_application_form_template.xml',
    ],
    'demo': [
        'data/hr_job_demo.xml',
    ],
    'installable': True,
}
