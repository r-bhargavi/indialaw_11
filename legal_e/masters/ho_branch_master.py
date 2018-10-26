# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo import SUPERUSER_ID

        
class HoBranch(models.Model):
    _description="Head Office"
    _name = 'ho.branch'

    state_id= fields.Many2one('res.country.state', 'State', required=True)
    name= fields.Char('Office Name', size=64, required=True)
    code= fields.Char('Office Code', size=10, required=True)
    sequence_id= fields.Many2one('ir.sequence', 'Entry Sequence', help="This field contains the information related to the numbering of the Case Entries.")
    district_id=fields.Many2one('district.district', 'District')
    country_id=fields.Many2one('res.country', 'Country')
    active=fields.Boolean('Active')

    #district set as null when no state present
    @api.onchange('state_id')
    def onchange_state(self):
        return {'value':{ 'district_id' : False}}
    
    #state set as null when no country preset
    @api.onchange('country_id')
    def onchange_country(self):
        return {'value':{ 'state_id' : False}}

    @api.model
    def create_sequence(self,vals):
        """ Create new no_gap entry sequence for every new Branch
        """
        seq = {
            'name': vals['name'],
            'implementation':'no_gap',
            'padding': 3,
            'number_increment': 1
        }
        if 'company_id' in vals:
            seq['company_id'] = vals['company_id']
        return self.env['ir.sequence'].create(seq)

    @api.model
    def create(self,vals):
        if vals is None:
           vals = {}
        vals.update({'sequence_id': False})
        return super(HoBranch, self).create(vals)
        
HoBranch()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
