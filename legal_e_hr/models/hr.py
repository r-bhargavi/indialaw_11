# -*- coding: utf-8 -*-
from datetime import datetime, date, timedelta
import time
import logging
from odoo import models, fields, api, exceptions
from odoo.tools.translate import _
from odoo import netsvc
from odoo.tools import ustr
from odoo import SUPERUSER_ID


_logger = logging.getLogger(__name__)

class HrHolidaysPublic(models.Model):

    _name = 'hr.holidays.public'
    _description = 'Public Holidays'
    _rec_name = 'year'
    _order = "year"

    year= fields.Char("calendar Year", required=True)
    line_ids= fields.One2many('hr.holidays.public.line', 'holidays_id', 'Holiday Dates')

    _sql_constraints = [
        ('year_unique', 'UNIQUE(year)', _('Duplicate year!')),
    ]

    @api.multi
    def is_public_holiday(self, dt):
        ph_obj = self.env['hr.holidays.public']
        ph_ids = ph_obj.search([('year', '=', dt.year)])
        if len(ph_ids) == 0:
            return False

        for line in (ph_ids[0]).line_ids:
            if date.strftime(dt, "%Y-%m-%d") == line.date:
                return True

        return False

    @api.multi
    def get_holidays_list(self, year):

        res = []
        ph_ids = self.search([('year', '=', year)])
        if len(ph_ids) == 0:
            return res
        [res.append(l.date) for l in (ph_ids[0]).line_ids]
        return res

    # function used in legal_e module
    @api.multi
    def get_next_working_day(self, dt):
        dt = datetime.strptime(dt, '%Y-%m-%d')
        ph_obj = self.env['hr.holidays.public']
        ph_ids = ph_obj.search([('year', '=', dt.year)])
        if len(ph_ids) == 0:
            if dt.weekday() == 6:
                dt = (dt + timedelta(days=1)).strftime('%Y-%m-%d')
                return self.get_next_working_day(dt)
            else:
                return dt

        for line in (ph_ids[0]).line_ids:
        # for line in ph_obj.browse(ph_ids[0]).line_ids:
            if date.strftime(dt, "%Y-%m-%d") == line.date or dt.weekday() == 6:
                dt = (dt + timedelta(days=1)).strftime('%Y-%m-%d')
                return self.get_next_working_day(dt)

        return date.strftime(dt, "%Y-%m-%d")

HrHolidaysPublic()

class HrHolidaysLine(models.Model):

    _name = 'hr.holidays.public.line'
    _description = 'Public Holidays Lines'
    _order = "date, name desc"

    name= fields.Char('Name', size=128, required=True)
    date= fields.Date('Date', required=True)
    holidays_id= fields.Many2one('hr.holidays.public', 'Holiday Calendar Year')
    variable= fields.Boolean('Date may change')

HrHolidaysLine()

# class HrTimesheetSheet(models.Model):
#     _inherit = "hr_timesheet_sheet.sheet"
#
#     def _get_year_from_date(self, cr, uid, ids, field_name, args, context=None):
#         res={}
#         for obj in self.browse(cr, uid, ids):
#             res[obj.id] = obj.date_from[:4]
#         return res
#
#     project_task_work_ids= fields.One2many('project.task.work', 'timesheet_id', 'Project Task Work lines'),
#     start_year = fields.Integer(compute='_get_year_from_date', string='Year', store=True)
#     # store = {
#     #     'hr_timesheet_sheet.sheet': (lambda self, cr, uid, ids, c={}: ids, ['date_from'], 10),
#     # }
#
#     defaults = {
#         'date_to': time.strftime('%Y-%m-%d')
#     }

#     @api.model
#     def create(self, cr, uid, vals, context=None):
#         date_format = '%Y-%m-%d'
#         current_date = time.strftime('%Y-%m-%d')
#         if vals['date_from'] > current_date or vals['date_to'] > current_date:
#             raise osv.except_osv(_('Error'), _('Future date selection restricted.'))
#         date_from_wk_no = datetime.strptime(vals['date_from'], date_format)
#         date_to_wk_no = datetime.strptime(vals['date_to'], date_format)
#         if date_from_wk_no.strftime("%V") == date_to_wk_no.strftime("%V"):
#             if (date_to_wk_no - date_from_wk_no).days != 6:
#                 raise osv.except_osv(_('Error'), _(
#                     "Please select 'Monday' as date from and 'Sunday' as date to in respective weeks"))
#         else:
#             raise osv.except_osv(_('Error'), _('From & To date must be in same week.'))
#
#         return super(hr_timesheet_sheet, self).create(cr, uid, vals, context=context)
#
#     @api.multi
#     def write(self, cr, uid, ids, vals, context=None):
#         res = super(hr_timesheet_sheet, self).write(cr, uid, ids, vals, context=context)
#         if vals.get('date_from', False) or vals.get('date_to', False):
#             date_format = '%Y-%m-%d'
#             current_date = time.strftime('%Y-%m-%d')
#             for time_sheet_obj in self.browse(cr, uid, ids, context=context):
#                 if time_sheet_obj.date_from > current_date or time_sheet_obj.date_to > current_date:
#                     raise osv.except_osv(_('Error'), _('Future date selection restricted.'))
#                 date_from_wk_no = datetime.strptime(time_sheet_obj.date_from, date_format)
#                 date_to_wk_no = datetime.strptime(time_sheet_obj.date_to, date_format)
#                 if date_from_wk_no.strftime("%V") == date_to_wk_no.strftime("%V"):
#                     if (date_to_wk_no - date_from_wk_no).days != 6:
#                         raise osv.except_osv(_('Error'), _(
#                             "Please select 'Monday' as date from and 'Sunday' as date to in respective weeks"))
#                 else:
#                     raise osv.except_osv(_('Error'), _('From & To date must be in same week.'))
#         return res
#
#     def button_reset(self, cr, uid, ids, context=None):
#         wf_service = netsvc.LocalService("workflow")
#         self.write(cr, uid, ids, {'state': 'new'}, context=context)
#         wf_service = netsvc.LocalService("workflow")
#         for id in ids:
#             wf_service.trg_delete(uid, 'hr_timesheet_sheet.sheet', id, cr)
#         return True
#
#     def button_open(self, cr, uid, ids, context=None):
#         wf_service = netsvc.LocalService("workflow")
#         for time_obj in self.browse(cr, uid, ids, context=context):
#             cr.execute('select id from wkf_instance where res_id=%s and res_type=%s and state=%s',
#                        (time_obj.id or None, 'hr_timesheet_sheet.sheet' or None, 'active'))
#             res = cr.fetchall()
#             if not res:
#                 wf_service.trg_create(uid, 'hr_timesheet_sheet.sheet', time_obj.id, cr)
#         return True
#
#
# HrTimesheetSheet()

# class hr_analytic_timesheet(osv.osv):
#     _inherit = "hr.analytic.timesheet"
#
#     def _get_default_timesheet_analytic_account(self, cr, uid, context=None):
#         user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
#         anal_acc_pool = self.pool.get('account.analytic.account')
#         company = False
#         parent_id = False
#         child_id = False
#         if user.company_id:
#             company = user.company_id.name
#             parent_ids = anal_acc_pool.search(cr, uid, [('name', '=', company), ('type', '=', 'view')])
#             if not len(parent_ids):
#                 parent_id = anal_acc_pool.create(cr, uid, {'name': company, 'use_timesheets': True, 'type': 'view'})
#             else:
#                 parent_id = parent_ids[0]
#             if parent_id:
#                 child_ids = anal_acc_pool.search(cr, uid,
#                                                  [('name', '=', 'Miscellaneous Timesheet'), ('type', '=', 'normal'),
#                                                   ('parent_id', '=', parent_id)])
#                 if not len(child_ids):
#                     child_id = anal_acc_pool.create(cr, uid, {'name': 'Miscellaneous Timesheet', 'use_timesheets': True,
#                                                               'type': 'normal', 'parent_id': parent_id})
#                 else:
#                     child_id = child_ids[0]
#
#         return child_id
#
#     _columns = {
#         'from_time': fields.float('From Time'),
#         'to_time': fields.float('To Time'),
#     }
#     _defaults = {
#         'account_id': lambda s, cr, uid, c: s._get_default_timesheet_analytic_account(cr, uid, c),
#     }
#
#     def onchange_time(self, cr, uid, ids, from_time, to_time, context=None):
#         vals = {}
#         if from_time and to_time:
#             if from_time > to_time:
#                 raise osv.except_osv(_('Error'), _('From Time should be Less than To Time.'))
#             else:
#                 vals['unit_amount'] = to_time - from_time
#         return {'value': vals}
#
#
# hr_analytic_timesheet()
#
#
# class project_work(osv.osv):
#     _inherit = "project.task.work"
#
#     def _check_from_to_time(self, cr, uid, ids, context=None):
#         if context is None:
#             context = {}
#         obj = self.browse(cr, uid, ids[0])
#         if obj.from_time and obj.to_time:
#             if obj.from_time > obj.to_time:
#                 return False
#         return True
#
#     _columns = {
#         'timesheet_id': fields.many2one('hr_timesheet_sheet.sheet', 'Timesheet'),
#         'project_id': fields.many2one('project.project', 'Project', ondelete='set null', select="1"),
#         'from_time': fields.float('From Time'),
#         'to_time': fields.float('To Time'),
#         'date': fields.datetime('Date', select="1"),
#     }
#     _constraints = [
#         (_check_from_to_time, 'Error! From Time should be Less than To Time.', ['To Time'])
#     ]
#
    # @api.model
#     def create(self, cr, uid, vals, *args, **kwargs):
#         task_obj = self.pool.get('project.task')
#
#         timesheet_data = self.pool.get('hr_timesheet_sheet.sheet').read(cr, uid, vals['timesheet_id'], ['employee_id'])
#         vals['user_id'] = \
#         self.pool.get('hr.employee').read(cr, uid, timesheet_data['employee_id'][0], ['user_id'])['user_id'][0]
#         retvals = super(project_work, self).create(cr, uid, vals, *args, **kwargs)
#         obj = self.browse(cr, uid, retvals)
#         if obj.hr_analytic_timesheet_id:
#             vals_line = {}
#             task_obj = task_obj.browse(cr, uid, obj.task_id.id)
#             vals_line['name'] = '%s: %s' % (ustr(task_obj.name.name), ustr(obj.name or '/'))
#             vals_line['from_time'] = obj.from_time
#             vals_line['to_time'] = obj.to_time
#             # vals_line['user_id'] = obj.timesheet_id.employee_id.id
#             obj.hr_analytic_timesheet_id.write(vals_line)
#         return retvals
#
#     @api.multi
#     def write(self, cr, uid, ids, vals, context=None):
#         """
#         When a project task work gets updated, handle its hr analytic timesheet.
#         """
#         if context is None:
#             context = {}
#         retvals = super(project_work, self).write(cr, uid, ids, vals, context)
#
#         if isinstance(ids, (long, int)):
#             ids = [ids]
#
#         for task in self.browse(cr, uid, ids, context=context):
#             line_id = task.hr_analytic_timesheet_id
#             if not line_id:
#                 # if a record is deleted from timesheet, the line_id will become
#                 # null because of the foreign key on-delete=set null
#                 continue
#
#             vals_line = {}
#             if 'name' in vals or 'task_id' in vals:
#                 vals_line['name'] = '%s: %s' % (ustr(task.task_id.name.name), ustr(task.name or '/'))
#             if 'from_time' in vals:
#                 vals_line['from_time'] = vals['from_time']
#             if 'to_time' in vals:
#                 vals_line['to_time'] = vals['to_time']
#             self.pool.get('hr.analytic.timesheet').write(cr, uid, [line_id.id], vals_line, context=context)
#
#         return retvals
#
#     def onchange_time(self, cr, uid, ids, from_time, to_time, context=None):
#         vals = {}
#         if from_time and to_time:
#             if from_time > to_time:
#                 raise osv.except_osv(_('Error'), _('From Time should be Less than To Time.'))
#             else:
#                 vals['hours'] = to_time - from_time
#         return {'value': vals}
#
#
# project_work()

class HrHolidays(models.Model):
    _inherit = "hr.holidays"

    flg_reset_leaves=fields.Boolean('To Reset the leaves', default=False)
    state= fields.Selection([('draft', 'To Submit'),
                               ('cancel', 'Cancelled'),
                               ('confirm', 'To Approve'),
                               ('refuse', 'Refused'),
                               ('validate1', 'Second Approval'),
                               ('management_validate', 'Waiting Management Approval'),
                               ('validate', 'Approved')],
                              'Status', readonly=True, track_visibility='onchange',
                              help='The status is set to \'To Submit\', when a holiday request is created.\
                \nThe status is \'To Approve\', when holiday request is confirmed by user.\
                \nThe status is \'Refused\', when holiday request is refused by manager.\
                \nThe status is \'Approved\', when holiday request is approved by manager.')
    # workflow function
    # @api.multi
    # def check_department(self):
    #     """
    #     @return: True or False
    #     """
    #     res = False
    #     for record in self.ids:
    #         user_obj = self.env['res.users'].browse(self.env.user.id)
    #         departments = user_obj.company_id.client_business_dept_ids
    #         if record.employee_id.department_id in departments:
    #             res = True
    #     return res


    # @api.multi
    # def _get_employee_manager(self, holiday_record):
    #     employee_pool = self.env['hr.employee']
    #     user_obj = self.env['res.users'].browse(self.env.user.id)
    #     management_department = user_obj.company_id.management_dept_id
    #     if management_department:
    #         manager_id = employee_pool.search([('department_id','=',management_department.id),
    #                                                     ('ho_branch_id','=',holiday_record.employee_id.ho_branch_id.id)], limit=1)
    #         if manager_id:
    #             manager_obj = manager_id
    #             # manager_obj = employee_pool.browse(manager_id)
    #             return manager_obj
    #     return False

    # @api.multi
    # def get_signup_url(self):
    #     # assert len(ids) == 1
    #     document = self.browse(SUPERUSER_ID)
    #     manager_objs = self._get_employee_manager(SUPERUSER_ID,document)
    #     user = manager_objs and manager_objs[0].user_id
    #     partner = user.partner_id
    #     action = 'hr_holidays.open_ask_holidays'
    #     partner.signup_prepare()
    #     return partner._get_signup_url_for_action(action=action, view_type='form', res_id=document.id)[partner.id]

    # workflow function
    # @api.multi
    # def holidays_management_validate(self, cr, uid, ids, context=None):
    #     mail_mail = self.pool.get('mail.mail')
    #     ir_model_data = self.pool.get('ir.model.data')
    #     if context:
    #         ctx = context.copy()
    #     else:
    #         ctx = {}
    #     for record in self.browse(cr, uid, ids, context=context):
    #         manager_obj = self._get_employee_manager(cr, uid, ids, record, context=context)
    #         if manager_obj:
    #             template_id = ir_model_data.get_object_reference(cr, uid, 'legal_e_hr', 'email_template_hr_holiday')[1]
    #             ctx.update({
    #                 'email_to': manager_obj and manager_obj[0].work_email or '',
    #                 #                     'email_from': record.employee_id.parent_id and record.employee_id.parent_id.work_email
    #             })
    #             self.pool.get('email.template').send_mail(cr, SUPERUSER_ID, template_id, record.id, force_send=True,
    #                                                       context=ctx)
    #         record.write({'state': 'management_validate'})
    #     return True

    # @api.multi
    # def get_signup_url_manager(self, cr, uid, ids, context=None):
    #     assert len(ids) == 1
    #     document = self.browse(cr, SUPERUSER_ID, ids[0], context=context)
    #     user = document.employee_id.parent_id.user_id
    #     partner = user.partner_id
    #     action = 'hr_holidays.open_ask_holidays'
    #     partner.signup_prepare()
    #     return partner._get_signup_url_for_action(action=action, view_type='form', res_id=document.id)[partner.id]

    # @api.multi
    # def action_confirm(self):
    #     res = super(HrHolidays, self).action_confirm()
    #     print("resresresresres", res)
    #     for record in self:
    #         if record.employee_id.parent_id and record.employee_id.parent_id.user_id:
    #             template_id = self.env['ir.model.data'].get_object_reference('legal_e_hr',
    #                                                                               'email_template_hr_holiday_submit')[1]
    #             print("template_idtemplate_idtemplate_id", template_id)
    #             if self._context is None:
    #                 context = {}
    #             self._context.update({
    #                 'email_to': record.employee_id.parent_id.work_email or '',
    #             })
    #             self.env['mail.template'].send_mail(SUPERUSER_ID, template_id, record.id, force_send=True)
    #     return res
HrHolidays()

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    hr_employee_transfer_history_ids= fields.One2many('hr.employee.transfer.history', 'hr_employee_id',
                                                        'Employee Transfer History')
    hr_employee_promotion_history_ids= fields.One2many('hr.employee.promotion.history', 'hr_employee_id',
                                                         'Employee Promotion History')
    hr_employee_recommendation_history_ids=fields.One2many('hr.employee.recommendation.history', 'hr_employee_id',
                                                              'Employee Recommendation History')

    @api.multi
    def attendance_action_change(self):
        """ Check In/Check Out action
            Check In: create a new attendance record
            Check Out: modify check_out field of appropriate attendance record
        """
        if len(self) > 1:
            raise exceptions.UserError(_('Cannot perform check in or check out on multiple employees.'))
        action_date = fields.Datetime.now()

        if self.attendance_state != 'checked_in':
            vals = {
                'employee_id': self.id,
                'check_in': action_date,
            }
            return self.env['hr.attendance'].create(vals)
        else:
            attendance = self.env['hr.attendance'].search([('employee_id', '=', self.id), ('check_out', '=', False)], limit=1)
            if attendance:
                attendance.check_out = action_date
                attendance.action='sign_out'
            else:
                raise exceptions.UserError(
                    _('Cannot perform check out on %(empl_name)s, could not find corresponding check in. '
                      'Your attendances have probably been modified manually by human resources.') % {
                        'empl_name': self.name, })
            return attendance

HrEmployee()

class HrEmployeeTransferHistory(models.Model):

    _name = 'hr.employee.transfer.history'
    _description = 'Employee Transfer History'

    # name=fields.Char('Name', size=128)
    date= fields.Date('Date')
    description=fields.Text('Description')
    hr_employee_id=fields.Many2one('hr.employee', 'Employee')

HrEmployeeTransferHistory()

class HrEmployeePromotionHistory(models.Model):

    _name = 'hr.employee.promotion.history'
    _description = 'Employee Promotion History'


    #name= fields.Char('Name', size=128)
    date= fields.Date('Date')
    description=fields.Text('Description')
    hr_employee_id= fields.Many2one('hr.employee', 'Employee')

HrEmployeePromotionHistory()

class HrEmployeeRecommendationHistory(models.Model):

    _name = 'hr.employee.recommendation.history'
    _description = 'Employee Recommendation History'

    #name= fields.char('Name', size=128)
    date= fields.Date('Date')
    description= fields.Text('Description')
    hr_employee_id= fields.Many2one('hr.employee', 'Employee')


HrEmployeeRecommendationHistory()

#
# class analytical_timesheet_employees(osv.osv_memory):
#     _inherit = "hr.analytical.timesheet.users"
#
#     def default_get(self, cr, uid, fields, context=None):
#         if context is None:
#             context = {}
#         res = super(analytical_timesheet_employees, self).default_get(cr, uid, fields, context=context)
#         emp_ids = self.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)], context=context)
#         if emp_ids:
#             res.update({'employee_ids': [(6, 0, emp_ids)]})
#         return res
#
#
# analytical_timesheet_employees()

