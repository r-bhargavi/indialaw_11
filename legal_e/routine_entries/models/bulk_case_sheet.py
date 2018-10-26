# -*- coding: utf-8 -*-
import re
from odoo import fields, models, api
from odoo.tools.translate import _
from odoo import SUPERUSER_ID
from odoo.exceptions import UserError
import base64
import csv
import io
import logging
# import translitcodec
import codecs


class BulkCaseSheet(models.Model):
    _name = 'bulk.case.sheet'
    _description = 'Bulk Case Sheet'
    _inherit = ['mail.thread']

    @api.multi
    def _data_get(self):
        if self._context is None:
            context = {}
        result = {}
        location = self.env['ir.config_parameter'].get_param('ir_attachment.location')
        bin_size = context.get('bin_size')
        for attach in self:
            if location and attach.store_fname:
                result[attach.id] = self._file_read(location, attach.store_fname, bin_size)
            else:
                result[attach.id] = attach.db_datas  
        return result

    @api.multi
    def _data_set(self, name, value):
        # We dont handle setting data to null
        if not value:
            return True
        if self._context is None:
            context = {}
        location = self.env['ir.config_parameter'].get_param('ir_attachment.location')
        file_size = len(value.decode('base64'))
        if location:
            # attach = self.browse(self.ids)
            if self.store_fname:
                self._file_delete(location, self.store_fname)
            fname = self._file_write(location, value)
            # SUPERUSER_ID as probably don't have write access, trigger during create
            super(BulkCaseSheet, self).write(SUPERUSER_ID, [self.ids], {'store_fname': fname, 'file_size': file_size})
        else:
            super(BulkCaseSheet, self).write(SUPERUSER_ID, [self.ids], {'db_datas': value, 'file_size': file_size})
        return True

    @api.multi
    def name_get(self):
        res = []
        if not self.ids:
            return res
        for line in self:
            res.append((line.id,line.name.name))
        return res

    name= fields.Many2one('case.sheet','File Number to Duplicate')
    flg_first_row=fields.Boolean('The first row of the file contains the label of the column')
    field_delimiter=fields.Selection([(',',','),(';',';'),(':',':')],'Field Delimiter', default=',')
    text_delimiter=fields.Selection([('"','"'),("'","'")],'Text Delimiter',  default='"')
    datas=fields.Binary(string='File Content')
    # datas=fields.Binary(compute='_data_get', fnct_inv=_data_set, string='File Content', nodrop=True)
    datas_fname=fields.Char('File Content',size=256, required=True)
    store_fname=fields.Char('Stored Filename', size=256)
    db_datas=fields.Binary('Database Data')
    file_size= fields.Integer('File Size')
    attach_id= fields.Many2one('ir.attachment','Attachment ID')
    lot_name=fields.Char('Lot Number', size=64, required=True)
    arbitration_amount=fields.Float('Arbitration Fee')

    # _defaults = {
    #             'field_delimiter':',',
    #             'text_delimiter':'"',
    # }

    @api.multi
    def generate_bulk_casesheet(self):
        if self._context is None:
            context = {}
        for line in self:
            _reader = codecs.getreader('latin-1')
            data=csv.reader(_reader(io.BytesIO(base64.b64decode(line.datas))), quotechar='"', delimiter=',')
            for cells in data:
                if len(cells)>1:
                    refsearchids = self.env['case.sheet'].search([('client_id','=',line.name.client_id.id),('company_ref_no','=',cells[0])])
                    if len(refsearchids):
                        raise UserError(_('Warning'),_('For this Client "%s" Client Reference already Exists.'%cells[0]))
                    opp_data = {}
                    for opp in line.name.opp_parties:
                        opp_data['type'] = opp.type
                        opp_data['name'] = cells[1]
                    if opp_data == {}:
                        opp_data = {'name':cells[1]}
                    case_sheet_data={'lot_name': line.lot_name, 'arbitration_amount': line.arbitration_amount,'company_ref_no':cells[0],'opp_parties':[(0, 0, opp_data)]}
                    newid = line.name.with_context(bulk_case=True).copy(case_sheet_data)
                    self.env['case.sheet'].confirm_casesheet([newid])
            # self.env['case.sheet'].write([line.name.id], {'lot_name': line.lot_name, 'arbitration_amount': line.arbitration_amount})
                line.name.write({'lot_name': line.lot_name, 'arbitration_amount': line.arbitration_amount})
        return retval

    @api.model
    def create(self, vals):
        if self._context is None:
            context = {}
        retvals = super(BulkCaseSheet, self).create(vals)
        return retvals
        
BulkCaseSheet()
