# -*- coding: utf-8 -*-
import time
from datetime import datetime
from datetime import timedelta
from odoo import models, fields, api
from odoo.tools.translate import _


class HrHolidaysStatus(models.Model):
    _inherit = "hr.holidays.status"
    _description = "Leave Type"

    unpaid= fields.Boolean('Unpaid')

HrHolidaysStatus()


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    mobile_expense= fields.Float('Mobile Expenses')
    train_pass= fields.Float('Train Pass')
    travel_expense= fields.Float('Travelling Expenses')
    incentives= fields.Float('Incentives')
    arrears= fields.Float('Arrears')
    tax= fields.Float('Prof.Tax')
#         loan= fields.Float('Loan')
#         advance= fields.Float('Salary Advance')

    # function to calculate leaves and overtime on salary slip
    @api.model
    def get_worked_day_lines(self, contract_ids, date_from, date_to):
        """
        @param contract_ids: list of contract id
        @return: returns a list of dict containing the input that should be applied for the given contract between date_from and date_to
        """
        res=super(HrPayslip, self).get_worked_day_lines(contract_ids, date_from, date_to)
        for contract in contract_ids:
            overtime_hours = 0
            overtime_ids = []
            day_from = datetime.strptime(date_from, "%Y-%m-%d")
            day_to = datetime.strptime(date_to, "%Y-%m-%d")
            nb_of_days = (day_to - day_from).days + 1
            for day in range(0, nb_of_days):
                datetime_day = day_from + timedelta(days=day)
                day1 = datetime_day.strftime("%Y-%m-%d")
                overtime_ids += self.env['hr.overtime'].search([('state', '=', 'validate'), (
                'employee_id', '=', contract.employee_id.id), ('date_from', '<=', day1), ('date_to', '>=', day1)])
            if overtime_ids:
                overtime_ids = list(set(overtime_ids))
                for overtime_obj in overtime_ids:
                    overtime_hours += overtime_obj.number_of_hours_temp
            if overtime_hours != 0:
                overtime = {
                    'name': 'Overtime',
                    'sequence': 2,
                    'code': 'OT',
                    'number_of_days': 0.0,
                    'number_of_hours': overtime_hours,
                    'contract_id': contract.id,
                }
                res += [overtime]
        return res

HrPayslip()