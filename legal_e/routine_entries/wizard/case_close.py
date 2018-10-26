# -*- coding: utf-8 -*-
import time
from odoo import fields, models, api
from odoo.tools.translate import _
from odoo.exceptions import UserError


class CaseClose(models.TransientModel):
    _name = "case.close"
    _description = "To Close the Case Sheet"

    name= fields.Text('Remarks')
    close_date=fields.Date('Close Date', default=lambda *a: time.strftime('%Y-%m-%d'))

    # _defaults = {
    #     'close_date':lambda *a: time.strftime('%Y-%m-%d'),
    # }
    
    @api.multi
    def close_case_sheet(self):
        # if self._context is None:
        #     context = {}
        context=self.env.context.copy()
        case_id = self._context.get('active_id', False)
        # self.pool.get('case.sheet').write(cr, uid, [case_id], {'state':'done','close_comments':context['comments'],'close_date':context['close_date']})
        self.env['case.sheet'].browse(case_id).write({'state':'done','close_comments':context['comments'],'close_date':context['close_date']})
        for case_obj in self.env['case.sheet'].browse([case_id]):
            context['case_close'] =  True
#            this set_done not in odoo 11
            # self.env['project.project'].set_done([case_obj.project_id.id])
            type_ids = self.env['project.task.type'].search([('state', '=', 'done')],limit=1)
            if type_ids:
                self.env.cr.execute("update project_task set state='done', stage_id=%s  where project_id=%s;",(type_ids.id, case_obj.project_id.id))
        invoice_ids = self.env['account.invoice'].search([('case_id', '=', case_id)])
        for inv_obj in invoice_ids:
            if inv_obj.state not in ['paid', 'cancel']:
                raise UserError(_('Warning!'),_('Invoices related to this case sheet is not paid yet!'))
        return True

CaseClose()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: