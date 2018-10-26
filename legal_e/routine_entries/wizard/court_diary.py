# -*- coding: utf-8 -*-
import time
from odoo import fields, models, api


class CourtDiary(models.TransientModel):
    parent_id = False
    _name = "court.diary"
    _description = "Court Diary Details"


    name= fields.Many2one('case.sheet', 'File Number')
#         'client_id':fields.Many2one('res.partner','Client Name'),
    from_date=fields.Date('From date', default=lambda *a: time.strftime('%Y-%m-%d'))
    to_date=fields.Date('To Date', default=lambda *a: time.strftime('%Y-%m-%d'))
    date_filter=fields.Selection([('=','is equal to'),('!=','is not equal to'),('>','greater than'),('<','less than'),('>=','greater than or equal to'),('<=','less than or equal to'),('between','between')],'Proceed Date')
    next_from_date=fields.Date('From date', default=lambda *a: time.strftime('%Y-%m-%d'))
    next_to_date=fields.Date('To Date', default=lambda *a: time.strftime('%Y-%m-%d'))
    next_date_filter=fields.Selection([('=','is equal to'),('!=','is not equal to'),('>','greater than'),('<','less than'),('>=','greater than or equal to'),('<=','less than or equal to'),('between','between'),('missing','IS MISSING')],'Next Proceed Date')
    court_proceed_lines= fields.Many2many('court.proceedings', 'court_diary_line_ids', 'diary_id', 'proceeding_id', 'Court History')
    missing_date=fields.Boolean('Missing Dates')
    office_id= fields.Many2one('ho.branch', 'Office')
    state_id= fields.Many2one('res.country.state', 'State')
    client_service_manager_id= fields.Many2one('hr.employee','Client Relationship Manager')
    last_smt= fields.Boolean('Last Proceeding Only')

    assignee_id= fields.Many2one('hr.employee','Assignee')
    division_id=fields.Many2one('hr.department', 'Department/Division')
    client_ids=  fields.Many2many('res.partner', 'client_missing_diary_rel', 'client_id', 'court_diary_id', 'Clients')

    # _defaults = {
    #     'from_date':lambda *a: time.strftime('%Y-%m-%d'),
    #     'to_date':lambda *a: time.strftime('%Y-%m-%d'),
    #     'next_from_date':lambda *a: time.strftime('%Y-%m-%d'),
    #     'next_to_date':lambda *a: time.strftime('%Y-%m-%d'),
    # }
    @api.model
    def default_get(self, fields_list):
        if not self._context:
            context = {}
        self.parent_id = False    
        res = super(CourtDiary, self).default_get(fields_list)
        return res

    @api.multi
    def name_get(self):
        res = []
        if not self.ids:
            return ['COURT_HISTORY']
        for task_line in self:
            res.append((task_line.id,'COURT HISTORY'))
        return res

    @api.multi
    def filter_proceedings(self):
        context=self._context
        procee_pool = self.env['court.proceedings']
        filters = []
        self.parent_id = self.ids[0]
        if ('case_id') in context and context['case_id']!=False:
            filters.append(('case_id','=',context['case_id']))
        if context.get('client_ids', False) and context['client_ids'][0][2]:
            filters.append(('client_id','in', context['client_ids'][0][2])) 
        if ('date_filter') in context and context['date_filter']!=False:
            if context['date_filter']!='between':
                filters.append(('proceed_date',context['date_filter'],context['proceed_from_date'])) 
            else:
                filters.append(('proceed_date','>',context['proceed_from_date']))     
                filters.append(('proceed_date','<',context['proceed_to_date']))     
        if ('next_date_filter') in context and context['next_date_filter']!=False:
            filters.append(('flg_next_date','=',True))
            if context['next_date_filter']=='missing':
                filters.append(('next_proceed_date','=',False))                  
            elif context['next_date_filter']!='between':
                filters.append(('next_proceed_date',context['next_date_filter'],context['next_proceed_from_date'])) 
            else:
                filters.append(('next_proceed_date','>',context['next_proceed_from_date']))     
                filters.append(('next_proceed_date','<',context['next_proceed_to_date']))
        if context.get('missing_date', False):
            filters.append(('date_missing','=', True))
        if context.get('office_id', False):
            filters.append(('case_id.ho_branch_id','=', context['office_id']))
        if context.get('state_id', False):
            filters.append(('case_id.state_id','=', context['state_id']))
            
        if context.get('assignee_id', False):
            filters.append(('case_id.assignee_id','=', context['assignee_id']))
        
        if context.get('division_id', False):
            filters.append(('case_id.division_id','=', context['division_id']))
        
        if context.get('client_service_manager_id', False):
            filters.append(('case_id.client_service_manager_id','=', context['client_service_manager_id']))

        data_ids = procee_pool.search(filters, order='proceed_date desc')
        if context.get('last_smt', False):
            case_ids = [proce_obj.case_id.id for proce_obj in data_ids]
            # case_ids = [proce_obj.case_id.id for proce_obj in procee_pool.browse( data_ids)]
            case_ids = list(set(case_ids))
            proceed_ids = []
            for case_id in case_ids:
                proc_ids =  procee_pool.search([('case_id', '=', case_id)], order='proceed_date desc')
                proceed_ids.append(proc_ids[0])
            return self.write({'court_proceed_lines':[(6, 0, proceed_ids)]})
        return self.write({'court_proceed_lines':[(6, 0, data_ids)]})

    @api.multi
    def clear_filters(self):
        res={}
        res['name'] = False
        res['client_id'] = False
        res['date_filter'] = False
        res['from_date'] = time.strftime('%Y-%m-%d')
        res['to_date'] = time.strftime('%Y-%m-%d')
        res['next_date_filter'] = False
        res['next_from_date'] = time.strftime('%Y-%m-%d')
        res['next_to_date'] = time.strftime('%Y-%m-%d')
        res['client_service_manager_id'] = False
        res['state_id'] = False
        res['office_id'] = False
        res['date_missing'] = False
        res['last_smt'] = False
        return self.write(res)

    @api.multi
    def clear_filters_all(self):
        res={}
        res['name'] = False
        res['client_id'] = False
        res['date_filter'] = False
        res['from_date'] = time.strftime('%Y-%m-%d')
        res['to_date'] = time.strftime('%Y-%m-%d')
        res['next_date_filter'] = False
        res['next_from_date'] = time.strftime('%Y-%m-%d')
        res['next_to_date'] = time.strftime('%Y-%m-%d')
        res['client_service_manager_id'] = False
        res['state_id'] = False
        res['office_id'] = False
        res['date_missing'] = False
        res['last_smt'] = False
        self.env.cr.execute('delete from court_diary_line_ids')
        return self.write(res)
        
    @api.multi
    def get_ids(self):
        ret = []
        if self.parent_id:
            for line in self.browse(self.parent_id).court_proceed_lines:
                ret.append(str(line.id))
        return {"ids":ret}

CourtDiary()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: