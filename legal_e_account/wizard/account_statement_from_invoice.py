# -*- coding: utf-8 -*-
import time

from odoo import api, fields, models
from odoo.tools.translate import _

class AccountStatementFromInvoiceLines(models.TransientModel):
    """
    Generate Entries by Statement from Invoices
    """
    _name = "legale.account.statement.from.invoice.lines"
    _description = "Entries by Statement from Invoices"
        
    journal_id=fields.Many2one('account.journal', 'Journal')
    period_id=fields.Many2one('account.period', 'Period')
    line_ids=fields.Many2many('account.move.line', 'legale_account_move_line_relation', 'move_id', 'line_id', 'Invoices')
    
    @api.multi
    def populate_statement(self):
        context = self._context or {}
        statement_id = context.get('statement_id')
        if not statement_id:
            return {'type': 'ir.actions.act_window_close'}
#        data =  self.read(cr, uid, ids, context=context)[0]
#        line_ids = data['line_ids']
        if not self.line_ids:
            return {'type': 'ir.actions.act_window_close'}

        line_obj = self.env['account.move.line']
        statement_obj = self.env['legale.account.bank.statement']
        statement_line_obj = self.env['legale.account.bank.statement.line']
        currency_obj = self.ev['res.currency']
        line_date = time.strftime('%Y-%m-%d')
        statement = statement_obj.browse(statement_id)

        # for each selected move lines
#        for line in line_obj.browse(cr, uid, line_ids, context=context):
        for line in self.line_ids:
            voucher_res = {}
            ctx = context.copy()
            #  take the date for computation of currency => use payment date
            ctx['date'] = line_date
            
                
            amount = dr_amount = cr_amount = 0.0
    
            if line.debit > 0:
                dr_amount = amount = line.debit
            elif line.credit > 0:
                cr_amount = amount = line.credit

            if line.amount_currency:
                amount = currency_obj.compute(line.currency_id.id,
                    statement.currency.id, line.amount_currency)
            elif (line.invoice and line.invoice.currency_id.id != statement.currency.id):
                amount = currency_obj.compute(cr, uid, line.invoice.currency_id.id,
                    statement.currency.id, amount, context=ctx)

            type = 'general'
            if line.journal_id.type in ('sale', 'sale_refund'):
                type = 'customer'
            elif line.journal_id.type in ('purchase', 'purchase_refund'):
                type = 'supplier'
            
            statement_line_obj.create({
                'name': line.name or '?',
                'amount': amount,
                'dr_amount': dr_amount,
                'cr_amount': cr_amount,
                'differ_amount': amount,
                'type': type,
                'partner_id': line.partner_id.id,
                'account_id': line.account_id.id,
                'statement_id': statement_id,
                'ref': line.ref,
                'date': line.date,
            })
        return {'type': 'ir.actions.act_window_close'}

AccountStatementFromInvoiceLines()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
