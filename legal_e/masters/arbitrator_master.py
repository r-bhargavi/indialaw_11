# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ArbitratorMaster(models.Model):
    _name = 'arbitrator.master'

    name= fields.Char('Arbitrator Name',size=128, required=True)
    number=fields.Char('Arbitrator No',size=64, required=True)
    street= fields.Char('Street', size=128)
    street2= fields.Char('Street2', size=128)
    zip=fields.Char('Zip', change_default=True, size=24)
    city= fields.Char('City', size=128)
    district_id=fields.Many2one("district.district",'District')
    state_id=fields.Many2one("res.country.state", 'State')
    country_id=fields.Many2one('res.country', 'Country')
    email=fields.Char('Email', size=240)
    phone= fields.Char('Phone', size=64)
    fax= fields.Char('Fax', size=64)
    mobile=fields.Char('Mobile', size=64)
    bank_ids=fields.One2many('res.partner.bank', 'arbitrator_id', 'Banks')
    
    @api.onchange('state_id')
    def onchange_state(self):
        return {'value': {'district_id' : False}}
    
    
ArbitratorMaster()

class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    arbitrator_id=fields.Many2one('arbitrator.master', 'Arbitrator')
    partner_id=fields.Many2one('res.partner', 'Account Owner',
            ondelete='cascade')
    
ResPartnerBank()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: