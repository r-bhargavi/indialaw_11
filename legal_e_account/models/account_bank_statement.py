# -*- coding: utf-8 -*-
import time

from odoo import api, fields, models
from odoo.tools.translate import _
import odoo.addons.decimal_precision as dp

class AccountBankStatement(models.Model):
    
    @api.model
    def create(self,vals):
        if 'line_ids' in vals:
            for idx, line in enumerate(vals['line_ids']):
                line[2]['sequence'] = idx + 1
        return super(AccountBankStatement, self).create(vals)
    
    @api.multi
    def write(self):
        res = super(AccountBankStatement, self).write()
        for statement in self:
            for idx, line in enumerate(statement.line_ids):
                line.write({'sequence': idx + 1})
        return res
#
    def _default_journal_id(self):
        context = self._context or {}
        journal_pool = self.env['account.journal']
        journal_type = context.get('journal_type', False)
        company_id = self.env['res.company']._company_default_get('legale.account.bank.statement')
        if journal_type:
            ids = journal_pool.search([('type', '=', journal_type),('company_id','=',company_id.id)])
            if ids:
                return ids[0]
        return False

   

    def _get_period(self):
        ctx = dict(context or {}, account_period_prefer_normal=True)
        periods = self.env['account.period'].find(context=ctx)
        if periods:
           return periods[0]
        return False

    def _currency(self, cursor, user, ids, name, args, context=None):
        res = {}
        res_currency_obj = self.env['res.currency']
        res_users_obj = self.env['res.users']
        default_currency = res_users_obj.browse(cursor, user,
                user, context=context).company_id.currency_id
        for statement in self.browse(cursor, user, ids, context=context):
            currency = statement.journal_id.currency
            if not currency:
                currency = default_currency
            res[statement.id] = currency.id
        currency_names = {}
        for currency_id, currency_name in res_currency_obj.name_get(cursor,
                user, [x for x in res.values()], context=context):
            currency_names[currency_id] = currency_name
        for statement_id in res.keys():
            currency_id = res[statement_id]
            res[statement_id] = (currency_id, currency_names[currency_id])
        return res
#
#
    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.env['res.currency']
        line_obj = self.env['account.move.line']
        res = {}
#        amount_total,amount_diff_total=0.0,0.0
        for order in self:
            val = val1 = cr_amount = dr_amount = total = 0.0
#            cur = order.currency
            for line in order.line_ids:
                val += line.amount
                if line.bank_date >= order.from_date and line.bank_date <= order.to_date and line.reconciled:
                    total -= line.cr_amount
                    total += line.dr_amount
                    
                if line.bank_date and line.bank_date > order.to_date:
                    cr_amount += line.cr_amount
                    dr_amount += line.dr_amount
                elif not line.reconciled:
                    cr_amount += line.cr_amount
                    dr_amount += line.dr_amount
                    
                val1 += line.differ_amount
            order.amount_total = cur_obj.round(val)
            order.amount_diff_total = cur_obj.round(val1)
            domain = [
                ('state', '=', 'valid'),
                ('bank_reco', '=', True),
                ('account_id', '=', order.journal_id.default_debit_account_id.id),
                ]
            if order.from_date:
                domain.append(('date', '<=', order.to_date))
                
            line_ids = line_obj.search(domain)
            for move_line_obj in line_obj.browse(line_ids):
                if move_line_obj.debit > 0:
                    total += move_line_obj.debit
                elif move_line_obj.credit > 0:
                    total -= move_line_obj.credit
            total += order.balance_per_book
            order.balance_bank = cur_obj.round(total)
            order.debit_total = cur_obj.round(dr_amount)
            order.credit_total = cur_obj.round(cr_amount)
            
        return res
# old function
#    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
#        cur_obj = self.env['res.currency']
#        line_obj = self.env['account.move.line']
#        res = {}
#        for order in self.browse(cr, uid, ids, context=context):
#            res[order.id] = {
#                'amount_total': 0.0,
#                'amount_diff_total': 0.0,
#                }
#            
#            val = val1 = cr_amount = dr_amount = total = 0.0
#            cur = order.currency
#            for line in order.line_ids:
#                val += line.amount
#                if line.bank_date >= order.from_date and line.bank_date <= order.to_date and line.reconciled:
#                    total -= line.cr_amount
#                    total += line.dr_amount
#                    
#                if line.bank_date and line.bank_date > order.to_date:
#                    cr_amount += line.cr_amount
#                    dr_amount += line.dr_amount
#                elif not line.reconciled:
#                    cr_amount += line.cr_amount
#                    dr_amount += line.dr_amount
#                    
#                val1 += line.differ_amount
#            res[order.id]['amount_total'] = cur_obj.round(cr, uid, cur, val)
#            res[order.id]['amount_diff_total'] = cur_obj.round(cr, uid, cur, val1)
#            domain = [
#                ('state', '=', 'valid'),
#                ('bank_reco', '=', True),
#                ('account_id', '=', order.journal_id.default_debit_account_id.id),
#                ]
#            if order.from_date:
#                domain.append(('date', '<=', order.to_date))
#                
#            line_ids = line_obj.search(cr, uid, domain, context=context)
#            for move_line_obj in line_obj.browse(cr, uid, line_ids, context=context):
#                if move_line_obj.debit > 0:
#                    total += move_line_obj.debit
#                elif move_line_obj.credit > 0:
#                    total -= move_line_obj.credit
##             total += order.balance_per_book
#            res[order.id]['balance_bank'] = cur_obj.round(cr, uid, cur, total)
#            res[order.id]['debit_total'] = cur_obj.round(cr, uid, cur, dr_amount)
#            res[order.id]['credit_total'] = cur_obj.round(cr, uid, cur, cr_amount)
#            
#        return res
#    
#    def _get_statement(self, cr, uid, ids, context=None):
#        result = {}
#        for line in self.env['legale.account.bank.statement.line'].browse(cr, uid, ids, context=context):
#            result[line.statement_id.id] = True
#        return result.keys()

    _order = "date desc, id desc"
    _name = "legale.account.bank.statement"
    _description = "Bank Statement"
    _inherit = ['mail.thread']
    
    name=fields.Char('Reference', size=64, required=True,default="/", states={'draft': [('readonly', False)]}, readonly=True, help='if you give the Name other then /, its created Accounting Entries Move will be with same name as statement name. This allows the statement entries to have the same references than the statement itself') # readonly for account_cash_statement
    date=fields.Date('Date', states={'confirm': [('readonly', True)]},default=fields.Date.context_today, select=True)
    journal_id=fields.Many2one('account.journal', 'Journal', required=True,
        readonly=True, states={'draft':[('readonly',False)]},default=_default_journal_id)
    company_id=fields.Many2one('res.company',related='journal_id.company_id',default=lambda self: self.env['res.company']._company_default_get('legale.account.bank.statement'), string='Company', store=True, readonly=True)
    line_ids=fields.One2many('legale.account.bank.statement.line','statement_id', 'Statement lines', states={'confirm':[('readonly', True)]})
        
    state=fields.Selection([('draft', 'New'),
                                   ('open','Open'), # used by cash statements
                                   ('confirm', 'Closed')],
                                   'Status',default='draft', required=True, readonly="1", track_visibility='always',
                                   help='When new statement is created the status will be \'Draft\'.\n'
                                        'And after getting confirmation from the bank it will be in \'Confirmed\' status.')
    currency=fields.Many2one(compute='_currency', string='Currency')
    account_id=fields.Many2one(related='journal_id.default_debit_account_id', string='Account used in this journal', readonly=True, help='used in statement reconciliation domain, but shouldn\'t be used elswhere.')
        
    amount_total=fields.Float( compute='_amount_all', digits_compute=dp.get_precision('Account'), string='Amount Total',
            store=True)
#    amount_total=fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Amount Total',
#            store={
#                'legale.account.bank.statement': (lambda self, cr, uid, ids, c={}: ids, ['line_ids'], 10),
#                'legale.account.bank.statement.line': (_get_statement, ['amount','differ_amount','reconciled','dr_amount','cr_amount','bank_date'], 10),
#            },
#            multi='sums'),
    amount_diff_total=fields.Float( compute='_amount_all', digits_compute=dp.get_precision('Account'), string='Diff.Amount Total.',
            store=True,
            multi='sums')
#    amount_diff_total=fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Diff.Amount Total.',
#            store={
#                'legale.account.bank.statement': (lambda self, cr, uid, ids, c={}: ids, ['line_ids'], 10),
#                'legale.account.bank.statement.line': (_get_statement, ['amount','differ_amount','reconciled','dr_amount','cr_amount','bank_date'], 10),
#            },
#            multi='sums'),
        
    balance_per_book=fields.Float('Balance as per company book', digits_compute=dp.get_precision('Account'),track_visibility='always')
        
    balance_bank=fields.Float( compute='_amount_all', digits_compute=dp.get_precision('Account'), string='Balance as per bank',
            store=True,
            multi='sums', track_visibility='always')
#    balance_bank=fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Balance as per bank',
#            store={
#                'legale.account.bank.statement': (lambda self, cr, uid, ids, c={}: ids, ['journal_id', 'line_ids','balance_per_book', 'from_date', 'to_date'], 10),
#                'legale.account.bank.statement.line': (_get_statement, ['amount','differ_amount','reconciled','dr_amount','cr_amount','bank_date'], 10),
#            },
#            multi='sums', track_visibility='always'),
        
    debit_total=fields.Float(compute='_amount_all', digits_compute=dp.get_precision('Account'), string='Debit Total',
            store=True,
            multi='sums', track_visibility='always')
#    debit_total=fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Debit Total',
#            store={
#                'legale.account.bank.statement': (lambda self, cr, uid, ids, c={}: ids, ['journal_id', 'line_ids','balance_per_book', 'from_date', 'to_date'], 10),
#                'legale.account.bank.statement.line': (_get_statement, ['amount','differ_amount','reconciled','dr_amount','cr_amount','bank_date'], 10),
#            },
#            multi='sums', track_visibility='always'),
#           
    credit_total=fields.Float(compute='_amount_all', digits_compute=dp.get_precision('Account'), string='Credit Total',
            store=True,
            multi='sums', track_visibility='always')
#    credit_total=fields.function(compute=_amount_all, digits_compute=dp.get_precision('Account'), string='Credit Total',
#            store={
#                'legale.account.bank.statement': (lambda self, cr, uid, ids, c={}: ids, ['journal_id', 'line_ids','balance_per_book', 'from_date', 'to_date'], 10),
#                'legale.account.bank.statement.line': (_get_statement, ['amount','differ_amount','reconciled','dr_amount','cr_amount','bank_date'], 10),
#            },
#            multi='sums', track_visibility='always'),
                
        
    
    from_date=fields.Date('From', states={'draft': [('readonly', False)]}, readonly=True)
    to_date=fields.Date('To', states={'draft': [('readonly', False)]}, readonly=True)
        

#    @api.onchange('journal_id') 
##    def onchange_journal_id(self, cr, uid, statement_id, journal_id, context=None):
#    def onchange_journal_id(self):
#        if not self.journal_id:
#            return {}
#
#        journal_data = self.env['account.journal'].read(cr, uid, journal_id, ['company_id', 'currency'], context=context)
#        company_id = journal_data['company_id']
#        currency_id = journal_data['currency'] or self.env['res.company'].browse(cr, uid, company_id[0], context=context).currency_id.id
#        return {'value': {'company_id': company_id, 'currency': currency_id}}
    
#    @api.onchange('date', 'company_id')
#    def onchange_date(self):
#        """
#            Find the correct period to use for the given date and company_id, return it and set it in the context
        #"""
#        res = {}
#        period_pool = self.env['account.period']
#
#        if context is None:
#            context = {}
#        ctx = context.copy()
#        ctx.update({'company_id': company_id, 'account_period_prefer_normal': True})
#        pids = period_pool.find(cr, uid, dt=date, context=ctx)
#        if pids:
#            res.update({'period_id': pids[0]})
#            context.update({'period_id': pids[0]})
#
#        return {
#            'value':res,
#            'context':context,
#        }
#
#    
    def button_dummy(self):
        return True
#    
    @api.multi
    def button_confirm_bank(self):
        move_line_obj = self.env['account.move.line']
        for reco_obj in self:
            for line_obj in reco_obj.line_ids:
                if line_obj.reconciled:
                    line_obj.move_id.write({'bank_date': line_obj.bank_date, 'bank_reco': line_obj.reconciled}, context=context)
        return self.write({'state': 'confirm'})
#    
    def button_cancel(self):
        return self.write({'state': 'draft'})
#    
#    
    def import_journal_entires(self):
        if context is None:
            context = {}

        line_obj = self.env['account.move.line']
        statement_obj = self.env['legale.account.bank.statement']
        statement_line_obj = self.env['legale.account.bank.statement.line']
        currency_obj = self.env['res.currency']
        line_date = time.strftime('%Y-%m-%d')
        
        now = time.strftime('%Y-%m-%d')

        company_id = self.env['res.users'].browse(cr, uid, uid, context=context).company_id.id
        domain = [('company_id', '=', company_id), ('date_start', '<', now), ('date_stop', '>', now)]
        fiscalyears = self.env['account.fiscalyear'].search(cr, uid, domain, limit=1)
        if fiscalyears:
            fiscal_obj = self.env['account.fiscalyear'].browse(cr, uid, fiscalyears[0], context=context)
            context.update({
                'date_from': fiscal_obj.date_start,
                })
        for rec_obj in self.browse(cr, uid, ids, context=context):
            statement_line_obj.unlink(cr, uid, [rec_line.id for rec_line in rec_obj.line_ids], context=context)
            context.update({
                'date_to': rec_obj.to_date,
                'journal_ids': [rec_obj.journal_id.id]
                })
            res = self.env['account.account'].read(cr, uid, [rec_obj.journal_id.default_debit_account_id.id], ['debit','credit','balance'],context=context)
            if res:
                self.write(cr, uid, [rec_obj.id], {'balance_per_book': res[0]['balance']}, context=context)
            domain = [
                ('date','<=',rec_obj.to_date),
                ('journal_id','=',rec_obj.journal_id.id), 
                ('reconcile_id','=',False), 
                ('state', '=', 'valid'),
                ('bank_reco', '=', False),
                ('account_id', '=', rec_obj.journal_id.default_debit_account_id.id),
                ]
            if rec_obj.from_date:
                 domain.append(('date','>=',rec_obj.from_date))
                
            line_ids = line_obj.search(cr, uid, domain, context=context)
            # for each selected move lines
            for line in line_obj.browse(cr, uid, line_ids, context=context):
                voucher_res = {}
                ctx = context.copy()
                #  take the date for computation of currency => use payment date
                ctx['date'] = line_date
                amount = dr_amount = cr_amount = 0.0
    
                if line.debit > 0:
                    dr_amount = amount = line.debit
                elif line.credit > 0:
                    cr_amount = amount = line.credit
    
                type = 'general'
                if line.journal_id.type in ('sale', 'sale_refund'):
                    type = 'customer'
                elif line.journal_id.type in ('purchase', 'purchase_refund'):
                    type = 'supplier'
                
                statement_line_obj.create(cr, uid, {
                    'name': line.name or '?',
                    'move_id': line.id,
                    'amount': amount,
                    'dr_amount': dr_amount,
                    'cr_amount': cr_amount,
                    'differ_amount': amount,
                    'type': type,
                    'partner_id': line.partner_id.id,
                    'account_id': line.account_id.id,
                    'statement_id': rec_obj.id,
                    'ref': line.ref,
                    'date': line.date,
                }, context=context)
        
        return True
    

AccountBankStatement()

class AccountBankStatementLine(models.Model):
    
    @api.onchange('partner_id') 
    def onchange_partner_id(self):
#        obj_partner = self.env['res.partner']
#        context = self._context or {}
        if not self.partner_id:
            return {}
        if not self.supplier and not self.customer:
            type = 'general'
        elif self.supplier and self.customer:
            type = 'general'
        else:
            if self.supplier == True:
                type = 'supplier'
            if self.customer == True:
                type = 'customer'
        res_type = self.onchange_type(partner_id=partner_id, type=type)
        if res_type['value'] and res_type['value'].get('account_id', False):
            return {'value': {'type': type, 'account_id': res_type['value']['account_id']}}
        return {'value': {'type': type}}
#
    def onchange_type(self, partner_id, type):
        res = {'value': {}}
#        obj_partner = self.env['res.partner']
#        context = self._context or {}
        if not partner_id:
            return res
        account_id = False
#        line = self.browse(cr, uid, line_id, context=context)
        line = self
        if not line or (line and not line[0].account_id):
#            part = obj_partner.browse(cr, uid, partner_id, context=context)
            if type == 'supplier':
                account_id = partner_id.property_account_payable.id
            else:
                account_id = partner_id.property_account_receivable.id
            res['value']['account_id'] = account_id
        return res
    
    @api.onchange('bank_date','date')
    def onchange_bank_date(self):
        res = {'value': {'reconciled': False}}
        if bank_date:
            if bank_date < date:
                res['value'].update({})
                warning = {
                   'title': _('Error!'),
                   'message' : 'Bank date must be greater than transaction date'
                    }
                return {'value': {'bank_date': False, 'reconciled': False}, 'warning': warning}
            else:
                res['value']['reconciled'] = True
        
        return res
    
    
    _order = "date asc"
    _name = "legale.account.bank.statement.line"
    _description = "Bank Statement Line"

    name=fields.Char('OBI',default=lambda self: self.env['ir.sequence'].get('legale.account.bank.statement.line'), required=True, help="Originator to Beneficiary Information")
    move_id=fields.Many2one('account.move.line', 'Move Line')
    date=fields.Date('Date', required=True,default=lambda self : self._context.get('date', fields.Date.context_today(self)))
    amount=fields.Float('Amount', digits_compute=dp.get_precision('Account'))
    cr_amount=fields.Float('Credit', digits_compute=dp.get_precision('Account'))
    dr_amount=fields.Float('Debit', digits_compute=dp.get_precision('Account'))
    type=fields.Selection([
            ('supplier','Supplier'),
            ('customer','Customer'),
            ('general','General')
            ], 'Type', required=True,default='general')
    partner_id=fields.Many2one('res.partner', 'Partner')
    account_id=fields.Many2one('account.account','Account',
            required=True)
    statement_id=fields.Many2one('legale.account.bank.statement', 'Statement',
            select=True, required=True, ondelete='cascade')
    journal_id=fields.Many2one(related='statement_id.journal_id', string='Journal', store=True, readonly=True)
    analytic_account_id=fields.Many2one('account.analytic.account', 'Analytic Account')
    move_ids=fields.Many2many('account.move',
            'account_bank_statement_line_move_rel', 'statement_line_id','move_id',
            'Moves')
    ref=fields.Char('Reference', size=32)
    note=fields.Text('Notes')
    sequence=fields.Integer('Sequence', select=True, help="Gives the sequence order when displaying a list of bank statement lines.")
    company_id=fields.Many2one('statement_id.company_id',string='Company', store=True, readonly=True)
    differ_amount=fields.Float('Diff. Amount', digits_compute=dp.get_precision('Account'))
    bank_date=fields.Date('Bank Date')
    reconciled=fields.Boolean('Reconciled')

    
    
    
    def _check_bank_reco_date(self):
        for line in self:
             if line.bank_date and line.bank_date < line.statement_id.from_date:
                return False
        return True

    _constraints = [
        (_check_bank_reco_date, 'The Reco. Date earlier than transaction date is not allowed .', ['bank_date']),
    ]
    

AccountBankStatementLine()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
