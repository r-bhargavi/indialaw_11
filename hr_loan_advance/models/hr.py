# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _
import time
import datetime

class HrEmployeeAdvance(models.Model):
    _name = "hr.employee.advance"
    _description = "Employee Advances"
    
    name=fields.Many2one('hr.employee', "Employee",required=True)
    date=fields.Date("Date", default=lambda *a: time.strftime('%Y-%m-%d'))
    amount=fields.Float("Amount")
    description=fields.Char("Description", size=64)
    
HrEmployeeAdvance()


class HrEmployeeLoan(models.Model):
    _name = "hr.employee.loan"
    _description = "Employee Loan"
    _order= 'start_date'
     
    name=fields.Many2one('hr.employee', "Employee",required=True)
    start_date=fields.Date("Start Date",required=True,default=lambda *a: time.strftime('%Y-%m-%d'))
    amount=fields.Float("Amount")
    monthly_payment=fields.Integer('Monthly Payment')
    description=fields.Char("Description", size=64)
    tran_ids=fields.One2many('hr.employee.loan.trn', 'loan_id', 'Payments')
    balance_amount=fields.Float(string='Balance',store=True)
    last_trn_date=fields.Date(string='Last Trns. Date', store=True)
    
HrEmployeeLoan()


class HrEmployeeLoanTrn(models.Model):
    _name = "hr.employee.loan.trn"
    _description = "Loan Payments"
    
    name=fields.Char("Description", size=64)
    loan_id=fields.Many2one('hr.employee.loan', "Loan",required=True)
    date=fields.Date("Date",required=True)
    amount=fields.Float("Amount")
    payslip_id=fields.Many2one('hr.payslip', 'Payslip', readonly=True)
    
    
HrEmployeeLoanTrn()


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'    
    
    #take advance amount take by employee
    @api.depends('employee_id','date_from','date_to')
    def _get_advance(self):
        advance_obj = self.env['hr.employee.advance']
        amount = 0
        for slip in self:
            advance_ids = advance_obj.search([('name', '=', slip.employee_id.id), ('date', '>=', slip.date_from),('date', '<=', slip.date_to)])
            if advance_ids:
                for advance_id in advance_ids:
                    amount += advance_id.amount
                slip.advance = amount
    
    advance=fields.Float(compute='_get_advance',  string='Advance', store=True)
    loan=fields.Float(string='Loan', store=True)
        
HrPayslip()  
#
## vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
