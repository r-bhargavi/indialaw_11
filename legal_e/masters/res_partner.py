# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.tools.translate import _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.onchange('name')
    def onchange_name(self):
        if not self.name:
            return {'value': {'client_data_id': False}}
        val = {
            'client_data_id': (self.name and len(self.name.replace(" ",""))>=4 and self.name.replace(" ","")[:4].upper() or False)
        }
        return {'value': val}

    client_data_id= fields.Char('Client ID',size=10)
    pan=fields.Char('PAN',size=50)
    client_branch= fields.Char('Location/Division',size=40)
    extension=fields.Char('Extension',size=10)
    company_parent_id= fields.Many2one('res.partner', 'Parent Company')
    opposite=fields.Boolean('Opposite Party')
    district_id=fields.Many2one('district.district', 'District')
    property_account_payable=fields.Many2one('account.account',string="Account Payable", domain="[('type', '=', 'payable')]", help="This account will be used instead of the default one as the payable account for the current partner")
    property_account_receivable= fields.Many2one('account.account', string="Account Receivable",domain="[('type', '=', 'receivable')]", help="This account will be used instead of the default one as the receivable account for the current partner")
    associate= fields.Boolean('Associate')
    supplier_code= fields.Char('Supplier Code', size=128)
    create_date= fields.Datetime('Create Date', readonly=True)
    client_manager_id= fields.Many2one('hr.employee','Client Relationship Manager')

    # _defaults = {
    #     #'associate': True,
    #     }

    def _get_supplier_code(self):
        supplier_code=self.env['ir.sequence'].get('res.partner')
        return supplier_code

    @api.model
    def create(self, vals):
        if vals.get('supplier', False):
            supplier_code = self._get_supplier_code()
            vals.update({'supplier_code': supplier_code})
        res = super(ResPartner, self).create(vals)
        return res
    
    
    def onchange_district(self, cr, uid, ids, district_id, context=None):
        if district_id:
            state_id = self.pool.get('district.district').browse(cr, uid, district_id, context).state_id.id
            country_id = self.pool.get('res.country.state').browse(cr, uid, state_id, context).country_id.id
            return {'value':{'country_id':country_id,'state_id':state_id}}
        return {}
    @api.onchange('state_id')
    def onchange_state(self):
        return {'value':{ 'district_id' : False}}

#    @api.multi
#    def name_get(self):
#        res = []
#        if not self.ids:
#            return res
#        if type(self.ids) is not list:
#            res = [self.ids]
#        for line in self:
#            name=False
#            if line.name:
#                name =line.name
#            if line.supplier_code and line.supplier:
#                name = (name and name + '['+line.supplier_code +'] ' or False)
#            if line.client_branch:
#                name += ' ,' + line.client_branch
#            res.append(name)
#        return res
#
#    
#    @api.model
#    def name_search(self,name, args=None, operator='ilike',limit=100):
#        args = args or []
#        ids = self.browse()
#        if name:
#            ids = self.search([('name', operator, name)] + args, limit=limit)
#            if not ids:
#                ids = self.search([('supplier_code', operator, name)], limit=limit)
#                ids = self.search(['|',('name', operator, name), ('supplier_code', operator, name)] + args, limit=limit)
#        else:
#            ids = self.search(args, limit=limit)
#        return ids.name_get()
# #
#    @api.multi
#    def search(self, args, offset=0, limit=None, order=None,count=False):
#        if self._context is None:
#            context = {}
#        return super(ResPartner, self).search(args, offset, limit, order, count)
    
ResPartner()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: