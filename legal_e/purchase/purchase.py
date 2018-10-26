# -*- coding: utf-8 -*-
import time
from odoo.tools.translate import _
from odoo import fields, models, api
from odoo import netsvc
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order' 

    date_order=fields.Date('Order Date', help="Date on which this document has been created.", default=lambda *a: time.strftime('%Y-%m-%d'))
    create_date=fields.Datetime('Create Date')
    order_line= fields.One2many('purchase.order.line', 'order_id', 'Order Lines', states={'approved':[('readonly',True)],'done':[('readonly',True)]})
    office_id=fields.Many2one('hr.office', 'Office')
    ho_branch_id=fields.Many2one('ho.branch','HO Branch')

#     _defaults = {
#                'date_order': lambda *a: time.strftime('%Y-%m-%d'),
# #                'create_date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
#     		}

    #load office automatically when po create
    @api.model
    def create(self, vals):
        hr_employee_pool = self.env['hr.employee']
        employee_ids = hr_employee_pool.search([('user_id', '=', self.create_uid)])
        if employee_ids:
            employee = employee_ids
            if vals:
                vals['office_id'] = employee[0].office_id.id
                vals['ho_branch_id'] = employee[0].ho_branch_id.id
        order = super(PurchaseOrder, self).create(vals)
        return order

    @api.multi
    def copy(self,default=None):
        default = default or {}
        default.update({
            'date_approve': False,
        })        
        res = super(PurchaseOrder, self).copy(default)
        return res

    @api.multi
    def _choose_account_from_po_line(self, po_line):
        fiscal_obj = self.env['account.fiscal.position']
        
        if po_line.product_id:
            acc_id = po_line.product_id.property_account_expense.id
            if not acc_id:
                acc_id = po_line.product_id.categ_id.property_account_expense_categ.id
            if not acc_id:
                raise UserError(_('Error!'), _('Define expense account for this company: "%s" (id:%d).') % (po_line.product_id.name, po_line.product_id.id,))
        else:
            acc_id = False#property_obj.get(cr, uid, 'property_account_expense_categ', 'product.category', context=context).id
        fpos = po_line.order_id.fiscal_position or False
        return fiscal_obj.map_account(fpos, acc_id)
    
    def print_quotation(self, cr, uid, ids, context=None):
        '''
        This function prints the request for quotation and mark it as sent, so that we can see more easily the next step of the workflow
        '''
        res = super(PurchaseOrder, self).print_quotation()
        if res.get('report_name'):
            res.update({'report_name': 'purchase.order'})
        return res
        
PurchaseOrder()


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line' 
    #
    # STATE_SELECTION = [
    #     ('draft', 'Draft PO'),
    #     ('sent', 'RFQ Sent'),
    #     ('confirmed', 'Waiting Approval'),
    #     ('approved', 'Purchase Order'),
    #     ('except_picking', 'Shipping Exception'),
    #     ('except_invoice', 'Invoice Exception'),
    #     ('done', 'Done'),
    #     ('cancel', 'Cancelled')
    # ]

    @api.multi
    def _get_state(self):
        result = {}
        for order in self.env['purchase.order'].browse(self.ids):
            for line in order.order_line:
                result[line.id] = True
        return result.keys() 

       # 'order_state':fields.related('order_id','state',type='selection',selection=STATE_SELECTION,string='Order State',
       #  store={
       #      'purchase.order.line': (lambda self, cr, uid, ids, c={}: ids, ['order_id'], 10),
       #      'purchase.order': (_get_state, ['state'], 10),
       #  }),
    order_state = fields.Selection([
        ('draft', 'Draft PO'),
        ('sent', 'RFQ Sent'),
        ('confirmed', 'Waiting Approval'),
        ('approved', 'Purchase Order'),
        ('except_picking', 'Shipping Exception'),
        ('except_invoice', 'Invoice Exception'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], string='Order State', store=True, related='order_id.state', default='draft')
    date_order = fields.Date(related='order_id.date_order', string='Order Date', readonly=True)
    #
    # _defaults = {
    #            'order_state': 'draft',
    # 		}
            

#     def view_init(self, cr, uid, fields, context=None):
#         if not context:
#             context = {}
#         po_obj = self.pool.get('purchase.order')
#         data = context and context.get('active_id', False)
#         if data:
#             po = po_obj.browse(cr, uid, data, context=context)
#             if po.state in ('done','approved'):
#                 raise osv.except_osv(_('Warning!'), _("Purchase Order is already Approved. So, now you cannot add new Line Now!"))
#       
    def unlink(self):
        if self._context is None:
            context = {}
        for line in self.browse(self.ids):
            if line.order_id.state in ('approved','done'):
                raise UserError(_('Warning!'), _("'You cannot delete an Order line which is already Approved.'!"))
        return super(PurchaseOrderLine, self).unlink()
            
PurchaseOrderLine()


class StockPicking(models.Model):
    _inherit = "stock.picking"

    user_id_done=fields.Many2one('res.users', 'Received By')
    office_id=fields.Many2one('hr.office', 'Office')

    #
    # TODO: change and create a move if not parents
    #
    @api.multi
    def action_done(self):
        """Changes picking state to done.
        
        This method is called at the end of the workflow by the activity "done".
        @return: True
        """
        self.write({'state': 'done', 'date_done': time.strftime('%Y-%m-%d %H:%M:%S'), 'user_id_done':self.env.user.id})
        return True
    
StockPicking()


# class stock_picking_in(osv.osv):
#     _inherit = "stock.picking.in"
#
#     _columns = {
#                'user_id_done':fields.many2one('res.users', 'Received By'),
#                'office_id': fields.many2one('hr.office', 'Office'),
#                 }
#
# stock_picking_in()


class StockMove(models.Model):
    _inherit = "stock.move"
    

    user_id_done=fields.Many2one('res.users', 'Received By')
    date_done= fields.Datetime('Date done')

   
    def _action_done(self):
        res = super(StockMove,self)._action_done()
        self.write({'date_done': time.strftime('%Y-%m-%d %H:%M:%S'), 'user_id_done':self.env.user.id})
        return True
    
StockMove()


# class stock_partial_move(osv.osv_memory):
#     _inherit = "stock.partial.move"
#
#     def do_partial(self, cr, uid, ids, context=None):
#         # no call to super!
#         assert len(ids) == 1, 'Partial move processing may only be done one form at a time.'
#         partial = self.browse(cr, uid, ids[0], context=context)
#         partial_data = {
#             'delivery_date' : partial.date
#         }
#         moves_ids = []
#         for move in partial.move_ids:
#             if not move.move_id:
#                 raise osv.except_osv(_('Warning !'), _("You have manually created product lines, please delete them to proceed"))
#             if move.move_id.product_qty < move.quantity or move.quantity == 0:
#                 raise osv.except_osv(_('Warning !'), _("please check quantity"))
#             move_id = move.move_id.id
#             partial_data['move%s' % (move_id)] = {
#                 'product_id': move.product_id.id,
#                 'product_qty': move.quantity,
#                 'product_uom': move.product_uom.id,
#                 'prodlot_id': move.prodlot_id.id,
#             }
#             moves_ids.append(move_id)
#             if (move.move_id.picking_id.type == 'in') and (move.product_id.cost_method == 'average'):
#                 partial_data['move%s' % (move_id)].update(product_price=move.cost,
#                                                           product_currency=move.currency.id)
#         self.pool.get('stock.move').do_partial(cr, uid, moves_ids, partial_data, context=context)
#         return {'type': 'ir.actions.act_window_close'}
#
# stock_partial_move()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: