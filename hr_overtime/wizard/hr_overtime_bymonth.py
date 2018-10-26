# -*- coding: utf-8 -*-
from datetime import time
from odoo import models, fields, api, _


class HrOvertimeByMonth(models.TransientModel):
    _name = 'hr.overtime.wizard_odt.month'
    _description = 'Print Monthly Overtime Report'

    month=fields.Selection(
        [(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'),
         (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], 'Month', required=True, default=lambda *a: time.gmtime()[1])
    year=fields.Integer('Year', required=True, default=lambda *a: time.gmtime()[0])


    @api.multi
    def print_report(self):
        datas = {
            'ids': self._context.get('active_ids', []) and self._context.get('active_ids', []) or [],
            'model': 'hr.employee',
            'form': self.read()[0]
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'overtime_odt',
            'context':None,
            'datas': datas,
        }
