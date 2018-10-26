# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.


from datetime import datetime, date
from lxml import etree
import math
import pytz
import threading
import urllib.parse


from datetime import datetime, timedelta
from odoo import SUPERUSER_ID
from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    birthday_select = fields.Selection([('1', 'Today'), ('2', 'This Week'), ('3', 'This Month')], 'Birthday Selection')
    birthday_string = fields.Char('Birthday')
    birthday_day=fields.Char('Day of Birthday')
    birthday_month=fields.Char('Month of Birthday')
    login_date = fields.Datetime(related='user_id.login_date', string='Latest Connection', readonly=1)

    # to set birthday month and day
    @api.onchange('birthday')
    def onchange_birthday(self):
        if self.birthday:
            dt = datetime.strptime(self.birthday, '%Y-%m-%d')
            self.birthday_day = dt.strftime("%d")
            self.birthday_month= dt.strftime("%m")

    # cron to send birthday wishes mail to employee who are having birthday on a day on which cron runs
    @api.model
    def _cron_hr_birthday_reminder(self):
        su_id =self.env['hr.employee'].browse(SUPERUSER_ID)
        current_date=fields.Date.today()
        convo_current_date=datetime.strptime(current_date,'%Y-%m-%d')
        this_day=convo_current_date.strftime("%d")
        this_month=convo_current_date.strftime("%m")
        employee_ids=self.search([('birthday_day','=',this_day),('birthday_month','=',this_month)])
        for employee in employee_ids:
            bdate =employee.birthday
            # bdate =datetime.strptime(employee.birthday,'%Y-%m-%d').date()
            today =datetime.now().date()
            '''if bdate != today:
                if bdate.month == today.month:
                    if bdate.day == today.day:'''
            if employee:
                template_id = self.env['ir.model.data'].get_object_reference(
                                                      'hr_birthdays_dashboard',
                                                      'email_template_edi_emp_birthday_reminder')[1]
                email_template_obj = self.env['mail.template'].browse(template_id)
                if template_id:
                    email_to=employee.work_email
                    model='hr.employee'
                    email_template_obj.send_mail(employee.id, force_send=True,
                                      email_values={'email_to': email_to,
                                                    'model': model})

        return True


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
