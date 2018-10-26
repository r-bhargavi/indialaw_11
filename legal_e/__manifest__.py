# -*- coding: utf-8 -*-
{
    'name': 'Legal Information Administration',
    'version': '2.17',
    'category': 'Customized integration',
    'author': 'BroadTech IT Solutions Pvt Ltd.',
    'website': 'http://www.broadtech-innovations.com/',
    'description': """
Legal Information Administration.
===================================================

Used for Creating Legal Information

    """,
    'depends': [
        'base',
        'project',
        'web',
        'hr',
        'account',
        'board',
        # 'hr_evaluation',
        'hr_timesheet',
        'hr_contract',
        'hr_holidays',
        'hr_expense',
        'crm',
        # 'knowledge',
        # 'account_accountant',
        'project',
        # 'project_long_term',
        'sale',
        'sale_stock',
        # 'web_m2x_options',
        # 'web_export_view',
        'purchase',
        # 'project_timesheet',
        'stock',
        'portal',
        'purchase_requisition',
        'account_voucher',
        # 'hr_timesheet_invoice',
    ],
    'js': ['static/src/js/*.js'],
    'qweb': ['static/src/xml/export_inward_register.xml',
             ],
    'data': [
        # 'views/indialaw_accounts.xml',
        'security/hr_security.xml',
        # 'security/project_security.xml',
        # 'security/ir.model.access.csv',
        # 'portal/security/portal_security.xml',
        # 'portal/security/ir.model.access.csv',
        'routine_entries/views/res_users_view.xml',
        'routine_entries/views/case_sheet_sequence.xml',
        'masters/hr_view.xml',
        'routine_entries/views/case_sheet_view.xml',
        'routine_entries/views/case_sheet_data.xml',
        'routine_entries/wizard/case_make_invoice_advance.xml',
        'routine_entries/wizard/case_close_view.xml',
        'masters/res_partner_view.xml',
        # 'masters/res_partner_sequence.xml',
        'masters/court_master_view.xml',
        'masters/arbitrator_master_view.xml',
        'masters/assignee_master_view.xml',
        'masters/task_master_view.xml',
        'masters/task_data.xml',
        'masters/case_master_view.xml',
        # 'masters/casemaster_data.xml',
        'masters/material_master_view.xml',

        'masters/cost_center_view.xml',
        'masters/area_master_view.xml',
        'masters/delivery_master_view.xml',
        'masters/phase_master_view.xml',
        'masters/court_location_master_view.xml',
        'email/client_task.xml',
        'routine_entries/views/inward_register_view.xml',
        'routine_entries/views/tasks_for_invoice_view.xml',
        'routine_entries/views/outward_register_view.xml',
        'routine_entries/wizard/court_diary_view.xml',
        'masters/state_master_view.xml',
        'masters/zone_master_view.xml',
        # 'masters/branch_master_view.xml',
        'masters/ho_branch_master_view.xml',
        'masters/district_master_view.xml',
        'masters/followup_remark_view.xml',
        'routine_entries/wizard/case_sheet_invoice_view.xml',
        'routine_entries/wizard/consolidated_bill_view.xml',
        'routine_entries/wizard/consolidated_bill_sequence.xml',
        # 'routine_entries/wizard/consolidated_bill_report.xml',
        'mail/mail_thread_view.xml',
        'mail/wizard/confirm_done_view.xml',
        'masters/mediator_master_view.xml',
        'views/res_config_view.xml',
        'routine_entries/wizard/case_cancel_view.xml',
        'routine_entries/wizard/case_transfer_view.xml',
        'routine_entries/wizard/project_task_deadline_view.xml',
        'routine_entries/views/bulk_case_sheet_view.xml',
        'wizard/client_case_history_view.xml',
        'wizard/bills_payment_details_view.xml',
        'wizard/cases_bills_info_view.xml',
        'wizard/work_summary_view.xml',
        'views/res_company_view.xml',
        'routine_entries/wizard/hr_emp_update_dept_view.xml',
        # 'portal/views/portal_legale_view.xml',
        'crm/out_of_office_view.xml',
        'views/res_users_view.xml',
        'routine_entries/wizard/associate_payment_reminder_view.xml',
        'routine_entries/wizard/client_change_casesheet_view.xml',
        'routine_entries/wizard/consolidated_bulk_case_sheet_view.xml',
        'wizard/week_timesheet_view.xml',
        'dashboard/casesheet_dashboard_view.xml',
        # 'dashboard/report/casesheet_report_board_view.xml',
        'purchase/purchase_view.xml',
        'routine_entries/wizard/reset_emp_leaves_view.xml',
        # 'purchase/purchase_report.xml',
        'purchase_requisition/wizard/purchase_requisition_partner_view.xml',
        'purchase_requisition/views/purchase_requisition_view.xml',
        'views/product_view.xml',
        'routine_entries/wizard/update_case_dept_view.xml',
        'routine_entries/wizard/add_employee_view.xml',
        'wizard/bulk_case_close_view.xml',
        'wizard/bulk_case_hold_view.xml',
        'wizard/bulk_task_close_view.xml',
        'wizard/bulk_case_fee_update_view.xml',
        # 'views/report.xml',

    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'css': ['static/src/css/case_sheet.css']
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: