# -*- coding: utf-8 -*-
import datetime
from odoo import netsvc
from odoo import models, fields, api, _
from odoo.tools.translate import _
from odoo.exceptions import UserError, ValidationError


class HrOvertimeType(models.Model):
    _name = "hr.overtime.type"
    _description = "Overtime Type"

    name= fields.Char('Description', required=True, size=64)
    double_validation=fields.Boolean('Apply Double Validation',help="If its True then its overtime type have to be validated by second validator")
    active=fields.Boolean('Active',help="If the active field is set to false, it will allow you to hide the overtime type without removing it.")

HrOvertimeType()

class HrOvertime(models.Model):
    _name = "hr.overtime"
    _description = "Overtime"
    _order = "date_from asc"

    @api.multi
    def _employee_get(self):
        ids = self.env['hr.employee'].search( [('user_id', '=', self.env.user.id)])
        print("idsssssssssssssssss", ids, ids.name)
        if ids:
            return ids[0]
        return False

    @api.multi
    @api.depends('number_of_hours')
    def _compute_number_of_hours(self, name):
        result = {}
        for hol in self.browse():
            result[hol.id] = hol.number_of_hours_temp
        return result

    name= fields.Char('Description', required=True, size=64)
    state= fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Waiting Approval'),
        ('refuse', 'Refused'),
        ('validate1', 'Waiting Second Approval'), ('validate', 'Approved'),
        ('cancel', 'Cancelled')],
        'State', readonly=True,default='draft', help='When the overtime request is created the state is \'Draft\'.\n It is confirmed by the user and request is sent to admin, the state is \'Waiting Approval\'.\
        If the admin accepts it, the state is \'Approved\'. If it is refused, the state is \'Refused\'.')
    user_id = fields.Many2one('res.users', related='employee_id.user_id', string='User', store=True,
                              default=lambda self: self.env.user.id)
    date_from= fields.Datetime('Start Date', readonly=True, states={'draft': [('readonly', False)]})
    date_to= fields.Datetime('End Date', readonly=True, states={'draft': [('readonly', False)]})
    employee_id= fields.Many2one('hr.employee', "Employee",  invisible=False, readonly=True, default=_employee_get,
                                   states={'draft': [('readonly', False)]})
    manager_id= fields.Many2one('hr.employee', 'First Approval', invisible=False, readonly=True)
    notes= fields.Text('Reasons', readonly=True, states={'draft': [('readonly', False)]})
    number_of_hours_temp= fields.Float('Number of Hours', readonly=True, states={'draft': [('readonly', False)]})
    number_of_hours = fields.Char(string='Number od Hours', store=True, compute=_compute_number_of_hours)
    department_id = fields.Many2one('hr.department', string='Department', related='employee_id.department_id',
                                    readonly=True, store=True)
    manager_id2 = fields.Many2one('hr.employee', 'Second Approval', readonly=True,
                                  help='This area is automaticly filled by the user who validate the leave with second level (If Leave type need second validation)')
    overtime_type_id=fields.Many2one("hr.overtime.type", "Overtime Type", required=True, readonly=True,
                                        states={'draft': [('readonly', False)]})
    double_validate=fields.Boolean(string='Double Validation', related='overtime_type_id.double_validation')

    _sql_constraints = [
        ('date_check', "CHECK ( number_of_hours_temp > 0 )", "The number of hours must be greater than 0 !"),
        ('date_check2', "CHECK (date_from < date_to)", "The start date must be before the end date !")
    ]

    @api.multi
    def _get_number_of_hours(self, date_from, date_to):
        """Returns a float equals to the timedelta between two dates given as string."""

        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        from_dt = datetime.datetime.strptime(date_from, DATETIME_FORMAT)
        to_dt = datetime.datetime.strptime(date_to, DATETIME_FORMAT)
        timedelta = to_dt - from_dt
        diff_day = timedelta.days + float(timedelta.seconds) / 86400
        return diff_day

    @api.multi
    def unlink(self):
        for rec in self.browse():
            if rec.state == 'draft':
                raise UserError(_('Warning!'), _('You cannot delete a overtime which is not in draft state !'))
        #                 raise Exception(_('You cannot delete a overtime which is not in draft state !'))
        return super(HrOvertime, self).unlink()

    @api.onchange('date_to','date_from')
    def onchange_date_from(self):
        result = {}
        result['value'] = {
            'number_of_hours_temp': 0,
        }
        return result

    @api.multi
    def set_to_draft(self):
        self.write( {
            'state': 'draft',
            'manager_id': False,
        })
        # wf_service = netsvc.log(self,'1','OT','set')
        # print("wffffffffffffffffffff", wf_service)
        # for id in self:
        #     wf_service.trg_create('hr.overtime', id)
        return True

    # direct approval of overtime request
    @api.multi
    def overtime_validate(self):
        obj_emp = self.env['hr.employee']
        print("obj_empobj_empobj_empobj_emp", obj_emp)
        ids2 = obj_emp.search([('user_id', '=', self.user_id.id)])
        manager = ids2 and ids2[0] or False
        print("managermanagermanagermanager", manager)
        if self.overtime_type_id.double_validation == True:
            return self.write({'state': 'validate1', 'manager_id': manager.id})
        else:
            return self.write({'state': 'validate', 'manager_id': manager.id})

    # second approval of overtime request
    @api.multi
    def overtime_validate2(self):
        obj_emp = self.env['hr.employee']
        ids2 = obj_emp.search([('user_id', '=', self.user_id.id)])
        manager = ids2 and ids2[0] or False
        self.write({'state': 'validate', 'manager_id2': manager.id})
        return True

    @api.multi
    def overtime_cancel(self):
        for record in self.browse():
            wf_service = netsvc.LocalService("workflow")
            for id in []:
                wf_service.trg_validate('hr.overtime', id, 'cancel')

        return True

    @api.multi
    def overtime_confirm(self):
        return self.write({'state': 'confirm'})

    @api.multi
    def overtime_refuse(self):
        obj_emp = self.env['hr.employee']
        ids2 = obj_emp.search([('user_id', '=', self.user_id.id)])
        manager = ids2 and ids2[0] or False
        self.write({'state': 'refuse', 'manager_id2': manager.id})
        self.overtime_cancel()
        return True

HrOvertime()

