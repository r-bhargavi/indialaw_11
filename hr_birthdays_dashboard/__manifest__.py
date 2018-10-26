# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
    'name' : "Send Employee Birthday Wishes",
    'version' : "11.0.0.1",
    'author' : "Knacktechs Solutions",
    'summary': 'Send Birthday Greetings Email to Employee',
    'description' : '''
             Module to send an Email to customer on Birthday.
			send birthday wishes to customer, birthday wishes email to customer, Birthday Reminder email, Birthday Greetings email to customer. send birthday wishes to Partner, birthday wishes email to Partner, Birthday Reminder email, Birthday Greetings email to Partner. 
    ''',
    'license':'OPL-1',
    'category' : "Extra Tools",
    'data': [
             'views/res_partner_view.xml',
             'views/birthday_reminder_cron.xml',
             'views/hr_employee_view.xml',
             'edi/birthday_reminder_action_data.xml'
             ],
    'website': 'http://www.knacktechs.com',
    'depends' : ['base', 'hr'],
    'installable': True,
    'auto_install': False,
	"images":['static/description/Banner.png'],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
