# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.tools.translate import _
from odoo import SUPERUSER_ID
from odoo.exceptions import UserError


class ConsolidatedBulkCaseSheet(models.TransientModel):
    _name = 'consolidated.bulk.case.sheet'
    _description = 'Consolidated Bulk Case Sheet'
    _inherit = ['mail.thread']

    @api.multi
    def _data_get(self, name, arg):
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
    def _data_set(self,name, value, arg):
        # We dont handle setting data to null
        if not value:
            return True
        if self._context is None:
            context = {}
        location = self.env['ir.config_parameter'].get_param('ir_attachment.location')
        file_size = len(value.decode('base64'))
        if location:
            attach = self.browse(id)
            if attach.store_fname:
                self._file_delete(location, attach.store_fname)
            fname = self._file_write(location, value)
            # SUPERUSER_ID as probably don't have write access, trigger during create
            super(ConsolidatedBulkCaseSheet, self).write(SUPERUSER_ID, [id], {'store_fname': fname, 'file_size': file_size})
        else:
            super(ConsolidatedBulkCaseSheet, self).write(SUPERUSER_ID, [id], {'db_datas': value, 'file_size': file_size})
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
    text_delimiter=fields.Selection([('"','"'),("'","'")],'Text Delimiter', default='"')
    datas= fields.Binary(compute='_data_get', fnct_inv=_data_set, string='File Content')
    datas_fname= fields.Char('File Content',size=256, required=True)
    store_fname= fields.Char('Stored Filename', size=256)
    db_datas= fields.Binary('Database Data')
    file_size= fields.Integer('File Size')
    attach_id= fields.Many2one('ir.attachment','Attachment ID')

    # _defaults = {
    #             'field_delimiter':',',
    #             'text_delimiter':'"',
    # }
    @api.multi
    def update_consolidated_bill_casesheet(self):
        for line in self:
            case_ids = []
            csvfile = line.datas.decode('base64')
            rowcount = 0
            if line.flg_first_row:
                rowcount = 1
            csvsplit = csvfile.split('\n')    
            for row in range(rowcount,len(csvsplit)):
                cells = csvsplit[row].split(line.field_delimiter)
                if len(cells) and cells[0].replace(line.text_delimiter,"").strip()!='':
                    cells[0] = cells[0].replace(line.text_delimiter,"")
                    refsearchids = self.env['case.sheet'].search([('name','=',cells[0].strip()),('client_id','=',self._context['client_id']),('work_type','=',self._context['work_type']),('casetype_id','=',self._context['casetype_id'])])
                    
                    if not len(refsearchids):
                        raise UserError(_('Error'),_('File Number "%s" is NOT present in the selected Client Case Details.'%cells[0]))
                    else:
                        case_ids.append(refsearchids[0])
            if len(case_ids):                
                for case_id in case_ids:
                    for act in self._context['active_ids']:
                        self.env['consolidated.bill'].write([act],{'case_sheet_ids':[(4,case_id)]})
        return True

    @api.model
    def create(self, vals):
        if self._context is None:
            context = {}
        retvals = super(ConsolidatedBulkCaseSheet, self).create(vals)
        return retvals
        
ConsolidatedBulkCaseSheet()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: