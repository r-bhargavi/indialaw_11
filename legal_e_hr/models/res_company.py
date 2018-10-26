# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class ResCompany(models.Model):
    _inherit = 'res.company'


    client_business_dept_ids=fields.Many2many('hr.department', 'company_client_business_department', 'company_id',
                                                 'department_id', 'Client Service/Business Development Departments')
    management_dept_id= fields.Many2one('hr.department', 'Management Department')

ResCompany()