# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from odoo.tools.translate import _
import time
import datetime


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    action=fields.Selection([('sign_in', 'Sign In'), ('sign_out', 'Sign Out'), ('action','Action')], 'Action', required=True, default='sign_in')

    @api.onchange('check_in','check_out')
    def onchange_check_in_out(self):
        if self.check_out:
            self.action='sign_out'
        else:
            self.action='sign_in'

    # @api.multi
    # def close_signout(self):
    #     attendance_pool = self.env['hr.attendance']
    #     emp_ids = self.env['hr.employee'].search([('user_id', '!=', False)])
    #     for emp_id in emp_ids:
    #         ids_signin = attendance_pool.search([('action', '=', 'sign_in'), ('employee_id', '=', emp_id)])
    #         ids_signout = attendance_pool.search([('action', '=', 'sign_out'), ('employee_id', '=', emp_id)])
    #         if len(ids_signin) != len(ids_signout):
    #             attendance_obj = attendance_pool.browse(ids_signin[0])
    #             date = attendance_obj.name.split(' ')
    #             name = date[0] + ' 23:00:00'
    #             if not ids_signout or ids_signin[0] > ids_signout[0]:
    #                 if not attendance_obj.sheet_id:
    #                     vals = {
    #                         'employee_id': emp_id,
    #                         'name': name,
    #                         'action': 'sign_out',
    #                     }
    #                     attendance_pool.create(vals)
    #                 else:
    #                     self.cr.execute(
    #                         'insert into hr_attendance (employee_id, name, action, sheet_id) values (%s, %s, %s, %s);',
    #                         (emp_id, name, 'sign_out', attendance_obj.sheet_id.id))
    #     return True

    # Cron function to automatically signout attendance of employees
    @api.multi
    def automatic_signout_scheduler(self):
        attendance_pool = self.env['hr.attendance']
        emp_ids = self.env['hr.employee'].search([('user_id', '!=', False)])
        for emp_id in emp_ids:
            ids_signin = self.env['hr.attendance'].search([('check_in', '>=', time.strftime('%Y-%m-%d') + ' 00:00:01'),('check_in', '<=', time.strftime('%Y-%m-%d') + ' 23:59:59'),('check_out','=',False),('action', '=', 'sign_in'),('employee_id','=',emp_id.id)])
            # ids_signout = attendance_pool.search([('check_out', '>=', time.strftime('%Y-%m-%d') + ' 00:00:01'),
            #                                                ('check_out', '<=', time.strftime('%Y-%m-%d') + ' 23:59:59'),
            #                                                ('action', '=', 'sign_out'), ('employee_id', '=', emp_id.id)])
            # if ids_signin or ids_signout:
            #     if len(ids_signin) != len(ids_signout):
            #         if not ids_signout or len(ids_signin) > len(ids_signout):
            if ids_signin:
                for signin in ids_signin:
                    signin.check_out=datetime.datetime.now()
                    signin.action='sign_out'

        return True


HrAttendance()


class LegalHrAttendance(models.Model):
    _name = 'legal.hr.attendance'
    _rec_name = 'employee_id'

    employee_id= fields.Many2one('hr.employee', 'Employee')
    office_id= fields.Many2one('ho.branch', 'Branch')
    dom =fields.Float('DOM')
    day_present= fields.Float('Days Present')
    absent=fields.Float('Absent')
    comp_off= fields.Float('Comp Off')
    comp_off_balance= fields.Float('Comp Off Balance')
    late_mark= fields.Float('Late Mark')
    leave_balance=fields.Float('Leave Balance')
    leave_availed= fields.Float('Leave Availed')
    leave_remain= fields.Float('Leave Remaining')
    ot_hour=fields.Float('OT Hours')
    date_from= fields.Date('Date From')
    date_to= fields.Date('Date To')
