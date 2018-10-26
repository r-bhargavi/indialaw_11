# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.tools.translate import _
from odoo import netsvc
from odoo.exceptions import UserError


class CaseSheetInvoice(models.Model):
    _name = "case.sheet.invoice"
    _description = "To Create an Invoice for Case Sheet"

    @api.multi
    @api.depends('invoice_lines_court_proceedings_assignment','invoice_lines_court_proceedings_fixed','invoice_lines_other_expenses','invoice_lines_fixed','invoice_lines_assignment_hourly','invoice_lines_assignment_fixed')
    def _get_total_amount(self):
        for inv in self:
            amount = 0.00
            for line in inv.invoice_lines_fixed:            
                amount = amount + line.amount + line.out_of_pocket_amount
            for line in inv.invoice_lines_assignment_hourly:            
                if line.amount:
                    amount = amount + line.amount
            for line in inv.invoice_lines_assignment_fixed:            
                if line.amount:
                    amount = amount + line.amount + line.out_of_pocket_amount
            for line in inv.invoice_lines_other_expenses:            
                if line.amount:
                    amount = amount + line.amount
            for line in inv.invoice_lines_court_proceedings_fixed:            
                if line.amount:
                    amount = amount + line.amount
            for line in inv.invoice_lines_court_proceedings_assignment:            
                if line.amount:
                    amount = amount + line.amount
            inv.amount_total_1 = amount

    name=fields.Char('Case Invoice Number',size=100)
    case_id= fields.Many2one('case.sheet','File Number')
    bill_type=fields.Selection([('fixed_price','Fixed Price'),('assignment_wise','Assignment Wise')],'Billing Type', required=False)
    amount_total_1=fields.Float(compute='_get_total_amount',string='Total Amount')
    invoice_lines_fixed=fields.One2many('case.sheet.invoice.line','inv_id_fixed','Fixed Price Stages Details')
    invoice_lines_assignment_hourly=fields.One2many('case.sheet.invoice.line','inv_id_assignment_hourly','Hourly Stages Details')
    invoice_lines_assignment_fixed=fields.One2many('case.sheet.invoice.line','inv_id_assignment_fixed','Fixed Price Stages Details')
    invoice_lines_other_expenses=fields.One2many('case.sheet.invoice.line','inv_id_other_expense','Other Expenses Details')
    invoice_lines_out_of_pocket=fields.One2many('case.sheet.invoice.line','inv_id_out_of_pocket','Out of Pocket Expenses Details')
    invoice_lines_court_proceedings_fixed=fields.One2many('case.sheet.invoice.line','inv_id_court_proceed_fixed','Fixed Price Court Proceedings Details')
    invoice_lines_court_proceedings_assignment=fields.One2many('case.sheet.invoice.line','inv_id_court_proceed_assignment','Assignment Wise Court Proceedings Details')
    invoice_lines=fields.One2many('case.sheet.invoice.line','inv_id_bill','Invoice Details')
    invoice_id=fields.Many2one('account.invoice','Invoice')
    subject=fields.Text('Subject')
    consolidated_id=fields.Many2one('consolidated.bill','Consolidated Bill Number')
    receivable_account_id=fields.Many2one('account.account', 'Receivable Account', domain=[('type','=','receivable')], help="The partner account used for these invoices.")
    sale_account_id=fields.Many2one('account.account', 'Sales Account', domain=[('type','=','view'), ('type', '=', 'closed')], help="The income or expense account related to the selected product.")
    invoice_date=fields.Date('Invoiced Date')
    expense_account_id= fields.Many2one('account.account', 'Expense Account', domain=[('type','=','view'), ('type', '=', 'closed')], states={'confirm':[('required',True)]})

    @api.multi
    def get_total_amount(self):
        res = 0.00
        for obj in self:
            amount = 0.00
            for line in obj.invoice_lines_fixed:            
                ob = self.env['fixed.price.stages'].browse(line.ref_id)
                amount += ob.amount + ob.out_of_pocket_amount
            for line in obj.invoice_lines_assignment_hourly:
                ob = self.env['assignment.wise'].browse(line.ref_id)
                amount += line.amount
            for line in obj.invoice_lines_assignment_fixed:            
                ob = self.env['assignment.wise'].browse(line.ref_id)
                amount += ob.amount + ob.out_of_pocket_amount
            for line in obj.invoice_lines_other_expenses:    
                if self.env['other.expenses'].search([('id','=',line.ref_id)]):
                    ob= self.env['other.expenses'].browse(line.ref_id)
                    amount += ob.amount
            for line in obj.invoice_lines_court_proceedings_fixed:
                amount += line.amount
            for line in obj.invoice_lines_court_proceedings_assignment:
                amount += line.amount
            return amount    
        return res

    @api.multi
    def dummy(self):
        return True

    @api.multi
    def invoice_case_sheet(self):
        context = self.env.context.copy() or {}
        line_total = 0.00
        obj_id=self
        if obj_id.type=='out_invoice':
            for line in obj_id.invoice_lines:
                line_total= line_total + line.amount
            if round(line_total,2) != round(obj_id.amount_total_1,2):
                raise UserError(_('Total Amount in Billing Particulars is NOT EQUAL to Total Amount!'))
        up_invoice_lines = []
        for line in obj_id.invoice_lines_fixed:
            invoice_line = {
                             'name':line.name,
                             'price_unit':line.amount + line.out_of_pocket_amount,
                             'quantity':1.0,
#                             'account_id':accoynt_id.id,
                             'account_analytic_id':obj_id.case_id.project_id.analytic_account_id.id,
                             'office_id': line.office_id.id 
                             }
            up_invoice_lines.append((0,0,invoice_line))
            
        for line in obj_id.invoice_lines_assignment_fixed:
            invoice_line = {
                             'name':line.name,
                             'price_unit':line.amount + line.out_of_pocket_amount,
                             'quantity':1.0,
                             'account_id':False,
                             'account_analytic_id':obj_id.case_id.project_id.analytic_account_id.id,
                             'office_id': line.office_id.id 
                             }
            up_invoice_lines.append((0,0,invoice_line))
            
            
        for line in obj_id.invoice_lines_assignment_hourly:
            invoice_line = {
                             'name':line.name,
                             'price_unit':line.amount + line.out_of_pocket_amount,
                             'quantity':1.0,
                             'account_id':False,
                             'account_analytic_id':obj_id.case_id.project_id.analytic_account_id.id,
                             'office_id': line.office_id.id 
                             }
            up_invoice_lines.append((0,0,invoice_line))
            
        for line in obj_id.invoice_lines_court_proceedings_assignment:
            invoice_line = {
                             'name':line.name,
                             'price_unit':line.amount + line.out_of_pocket_amount,
                             'quantity':1.0,
                             'account_id':False,
                             'account_analytic_id':obj_id.case_id.project_id.analytic_account_id.id,
                             'office_id': line.office_id.id 
                             }
            up_invoice_lines.append((0,0,invoice_line))
            
            
        for line in obj_id.invoice_lines_other_expenses:
            invoice_line = {
                             'name':line.name,
                             'price_unit':line.amount,
                             'quantity':1.0,
                             'account_id':False,
                             'account_analytic_id':obj_id.case_id.project_id.analytic_account_id.id,
                             'office_id': line.office_id.id 
                             }
            up_invoice_lines.append((0,0,invoice_line))
        
        particular_invoice_lines = []
        for line in obj_id.invoice_lines:
            particular_invoice_line = {
                             'name':line.name,
                             'price_unit':line.amount,
                             }
            particular_invoice_lines.append((0,0,particular_invoice_line))

        context.update({'type':'out_invoice'})
        journal_id = self.env['account.invoice']._default_journal()
        invoice = {
                   'partner_id':obj_id.case_id.client_id.id,
                   'type':'out_invoice',
                   'legale_number':(obj_id.consolidated_id and obj_id.consolidated_id.name or obj_id.case_id.name),
                   'subject_line':obj_id.subject,
                   'name':obj_id.case_id.name,
                   'journal_id':journal_id.id,
                   'invoice_line_ids':up_invoice_lines,
                   'particular_invoice_line_ids': particular_invoice_lines,
                   'account_id':obj_id.case_id.client_id.property_account_receivable_id.id,
                   'case_id':obj_id.case_id.id,
                   'consolidated_id':(obj_id.consolidated_id and obj_id.consolidated_id.id or False),
                   'date_invoice':obj_id.invoice_date,
                   }
        invoice_id = self.env['account.invoice'].create(invoice)
        #Update the Lines as Invoiced
        if invoice_id:
            self.write({'invoice_id':invoice_id.id})
            for line in obj_id.invoice_lines_fixed:
                ref_id=self.env['fixed.price.stages'].browse(line.ref_id)
                ref_id.write({'invoiced':True})
#                line.ref_id.write({'invoiced':True})
            for line in obj_id.invoice_lines_assignment_hourly:
                ref_id=self.env['assignment.wise'].browse(line.ref_id)
                ref_id.write({'invoiced':True, 'billed_hours':(assign.billed_hours + assign.remaining_hours), 'remaining_hours':0.00})
                # line.ref_id.write({'invoiced':True, 'billed_hours':(assign.billed_hours + assign.remaining_hours), 'remaining_hours':0.00})
            for line in obj_id.invoice_lines_assignment_fixed:
#                self.env['assignment.wise'].write([line.ref_id],{'invoiced':True})
                ref_id=self.env['assignment.wise'].browse(line.ref_id)
                ref_id.write({'invoiced':True})
            for line in obj_id.invoice_lines_other_expenses:
                ref_id=self.env['other.expenses'].browse(line.ref_id)
#                self.env['other.expenses'].write([line.ref_id],{'invoiced':True})
                ref_id.write({'invoiced':True})
            for line in obj_id.invoice_lines_court_proceedings_fixed:
                ref_id=self.env['court.proceedings'].browse(line.ref_id)
#                self.env['court.proceedings'].write([line.ref_id],{'invoiced':True})
                ref_id.write({'invoiced':True})
            for line in obj_id.invoice_lines_court_proceedings_assignment:
                ref_id=self.env['court.proceedings'].browse(line.ref_id)
#                self.env['court.proceedings'].write([line.ref_id],{'invoiced':True})
                ref_id.write({'invoiced':True})
            # wf_service = netsvc.LocalService("workflow")
            # if obj.consolidated_id:
                # wf_service.trg_validate(uid, 'account.invoice', invoice_id, 'invoice_open', cr)
            
            return True    
        return False

    @api.multi
    def cancel_invoice_case_sheet(self):
        context = self._context or {}

        for obj in self:
                for line in obj.invoice_lines_fixed:
                    self.env['fixed.price.stages'].write([line.ref_id],{'invoiced':False})
                    # line.ref_id.write({'invoiced':False})
                for line in obj.invoice_lines_assignment_hourly:
                    assign = self.env['assignment.wise'].browse(line.ref_id)
                    remain = line.bill_hours
                    if not remain or remain<=0:
                        remain = line.amount/assign.amount
                    remain = remain or 0.00
                    self.env['assignment.wise'].write([line.ref_id],{'invoiced':False, 'billed_hours':(assign.billed_hours - remain), 'remaining_hours':assign.remaining_hours + remain})
                    # line.ref_id.write({'invoiced':False, 'billed_hours':(assign.billed_hours - remain), 'remaining_hours':assign.remaining_hours + remain})
                for line in obj.invoice_lines_assignment_fixed:            
                    self.env['assignment.wise'].write([line.ref_id],{'invoiced':False})
                    # line.ref_id.write({'invoiced':False})
                
                for line in obj.invoice_lines_other_expenses:  
                    if line.ref_id:
                        expenses_ids = self.env['other.expenses'].search([('id', '=', line.ref_id)])
                        if expenses_ids:
                            self.env['other.expenses'].write([line.ref_id],{'invoiced':False})
                            # line.ref_id.write({'invoiced':False})
                for line in obj.invoice_lines_court_proceedings_fixed:
                    self.env['court.proceedings'].write([line.ref_id],{'invoiced':False})
                    # line.ref_id.write({'invoiced':False})
                for line in obj.invoice_lines_court_proceedings_assignment:
                    self.env['court.proceedings'].write([line.ref_id],{'invoiced':False})
                    # line.ref_id.write({'invoiced':False})
                return True    
        return False

    @api.multi
    def draft_invoice_case_sheet(self):
        for obj in self:
            for line in obj.invoice_lines_fixed:  
                ref_id=self.env['fixed.price.stages'].browse(line.ref_id)
                ref_id.write({'invoiced':True})
            for line in obj.invoice_lines_assignment_hourly:
                assign = self.env['assignment.wise'].browse(line.ref_id)
                remain = line.bill_hours
                if not remain or remain<=0:
                    remain = line.amount/assign.amount
                remain = remain or 0.00
                assign.write({'invoiced':True, 'billed_hours':(assign.billed_hours + assign.remaining_hours), 'remaining_hours':0.00})
            for line in obj.invoice_lines_assignment_fixed: 
                assign = self.env['assignment.wise'].browse(line.ref_id)
                assign.write({'invoiced':True})
            for line in obj.invoice_lines_other_expenses: 
                other_expenses = self.env['assignment.wise'].browse(line.ref_id)
                other_expenses.write({'invoiced':True})
            for line in obj.invoice_lines_court_proceedings_fixed:
                court_proceedings = self.env['court.proceedings'].browse(line.ref_id)
                court_proceedings.write({'invoiced':True})
            for line in obj.invoice_lines_court_proceedings_assignment:
                court_proceedings = self.env['court.proceedings'].browse(line.ref_id)
                court_proceedings.write({'invoiced':True})
        return True    

    @api.multi
    def unlink(self):
        for obj in self:
                for line in obj.invoice_lines_assignment_hourly:
                    assign = self.env['assignment.wise'].browse(line.ref_id)
                    remain = line.bill_hours
                    if not remain or remain<=0:
                        remain = line.amount/assign.amount
                    remain = remain or 0.00
                    self.env['assignment.wise'].write([line.ref_id],{'invoiced':False, 'billed_hours':(assign.billed_hours - remain), 'remaining_hours':assign.remaining_hours + remain})
        retvals = super(CaseSheetInvoice, self).unlink()
        return retvals


CaseSheetInvoice()

class CaseSheetInvoiceLine(models.Model):
    _name = "case.sheet.invoice.line"
    _description = "To Create an Invoice for Case Sheet"


    inv_id_bill=fields.Many2one('case.sheet.invoice','Case Invoice ID')
    inv_id_court_proceed_assignment=fields.Many2one('case.sheet.invoice','Case Invoice ID')
    inv_id_court_proceed_fixed=fields.Many2one('case.sheet.invoice','Case Invoice ID')
    inv_id_out_of_pocket=fields.Many2one('case.sheet.invoice','Case Invoice ID')
    inv_id_other_expense=fields.Many2one('case.sheet.invoice','Case Invoice ID')
    inv_id_assignment_fixed=fields.Many2one('case.sheet.invoice','Case Invoice ID')
    inv_id_assignment_hourly=fields.Many2one('case.sheet.invoice','Case Invoice ID')
    inv_id_fixed=fields.Many2one('case.sheet.invoice','Case Invoice ID')
    name= fields.Char('Description')
    amount=fields.Float('Amount')
    out_of_pocket_amount=fields.Float('Out of Pocket Expense')
    ref_id=fields.Integer('Reference ID')
    date=fields.Date('Date')
    effective=fields.Selection([('effective','Effective'),('noeffective','Not Effective')],'Effective?')
    bill_hours=fields.Float('Billing Hours')
    office_id=fields.Many2one('ho.branch','Office') #add office field # Sanal Davis # 27/5/15

    @api.onchange('invid')
    def onchange_line_amount(self):
        context = self._context or {}
        val = {}
        obj = self.browse(self.invid)
        line_total = 0.00
        if obj=='out_invoice':
            for line in obj.invoice_lines:            
                line_total= line_total + line.amount
            if round(line_total,2) != round(obj.amount_total_1,2):
                val['amount'] = 0.00
                raise UserError(_('Total Amount in Billing Particulars is NOT EQUAL to Total Amount!'))
        
        return {'value':val}

CaseSheetInvoiceLine()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: