# -*- coding: utf-8 -*-
import time
import babel
from odoo import models, fields, api, tools, _
from datetime import datetime
from odoo.exceptions import ValidationError


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    
    @api.one
    @api.depends('loan_ids')
    def compute_total_paid(self):
        """This compute the total paid amount of Loan.
            """
        total = 0.0
        for line in self.loan_ids:
            if line.pay:
                total += line.amount
        self.total_paid = total
        
    loan_ids = fields.One2many('hr.loan.line', 'payslip_id', string="Loans")
    total_paid = fields.Float(string="Total Loan Amount", compute='compute_total_paid')
    without_loan = fields.Boolean(string="Not loan", default=False)
    loan_reason=fields.Text('Reason for skipping loan installment?')
    
#    if employee take loan unpaid installment add in payslip loan line
    @api.onchange('employee_id', 'date_from', 'date_to')
    def onchange_employee(self):
        res=super(HrPayslip, self).onchange_employee()
        loan_list = []
        if self.employee_id:
            loan_ids = self.env['hr.loan.line'].search([('employee_id', '=', self.employee_id.id), ('paid', '=', False)])
            for loan in loan_ids:
                if loan.loan_id.state == 'approve':
                    loan_list.append(loan.id)
            self.loan_ids = loan_list
        return res
    
#    loan line avilabe in payslip  hr manager not select take second conformation of manager
    @api.multi
    def compute_sheet(self):
        for payslip in self:
            if payslip.without_loan==False:
                if payslip.loan_ids:
                    loan_ids=payslip.loan_ids.filtered(lambda r: r.pay == True)
                    if not loan_ids:
                        view_ref = self.env['ir.model.data'].get_object_reference('ohrms_loan', 'message_view')
                        view_id = view_ref[1] if view_ref else False
                        return {
                            'name': _('Message'),
                            'view_type': 'form',
                            'view_mode': 'form',
                            'view_id': view_id,
                            'res_model': 'message.wizard',
                            'type': 'ir.actions.act_window',
                            'target': 'new',
                        }
        return super(HrPayslip, self).compute_sheet()
    
#    in loan line pay selected on click of this button loan installment are paid if pay check box selected in payslip
    @api.multi
    def action_payslip_done(self):
        loan_list = []
        res=super(HrPayslip, self).action_payslip_done()
        if self.loan_ids:
            for line in self.loan_ids:
                if line.pay:
                    line.paid=True
                    loan_list.append(line.id)
                else:
                    line.payslip_id = False
        self.loan_ids = loan_list
        return res

    
