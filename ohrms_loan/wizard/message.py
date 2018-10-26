# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class MessageWizard(models.TransientModel):
    _name='message.wizard'
    
    @api.multi
    def confirm(self):
        payslip_id = self.env['hr.payslip'].browse(self._context.get('active_id'))
        if payslip_id:
            payslip_id.without_loan=True
   