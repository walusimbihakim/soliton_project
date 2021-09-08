from django.urls import path, include
import xlsxwriter
from projects.views import scope_views, team_views, wage_sheet_views, boq_views
from projects.views.auth_views import super_admin_required_page, project_manager_required_page, \
    supervisor_required_page, finance_officer_required_page
from projects.views.notification_views import unread_notifications_page, notifications_page
from projects.views.sites_views import *
import projects.views.worker_views as worker_views
from projects.views.survey_views import *
from projects.views.project_views import *
from projects.views.activity_list_views import *
from projects.views import project_settings_view, budget_views
from projects.views import pip_views
import projects.views.field_manager_views as field_manage_views
import projects.views.segment_views as segment_views
import projects.views.complaint_views as complaint_views
import projects.views.deduction_views as deduction_views
import projects.views.wage_bill_views as wage_bill_views
import projects.views.user_views as user_views

worker_urls = [
    path('manage_workers/', worker_views.manage_workers_page,
         name='manage_workers_page'),
    path('manage_group_workers/', worker_views.manage_group_workers_page,
         name='manage_group_workers_page'),
    path('view_all_workers/', worker_views.view_all_workers_page,
         name='view_all_workers_page'),
    path('all_workers_csv/', worker_views.all_workers_csv,
         name='all_workers_csv'),
    path('all_workers_pdf/', worker_views.all_workers_pdf,
         name='all_workers_pdf'),
    path('delete_worker/<int:id>/',
         worker_views.delete_worker, name='delete_worker'),
    path('edit_worker/<int:id>/', worker_views.edit_worker_page, name="edit_worker"),
    path('transfer_worker/<int:worker_id>/', worker_views.transfer_worker_view, name="transfer_worker"),
    path('transfer_worker_from_phone_number/', worker_views.transfer_worker_from_phone_number_view,
         name="transfer_worker_from_phone_number"),
    path('edit_group_worker/<int:id>/', worker_views.edit_group_worker_page,
         name="edit_group_worker"),
    path('delete_group_worker/<int:id>/',
         worker_views.delete_group_worker, name='delete_group_worker'),

]

survey_urls = [
    path('project/<int:id>/surveys', survey_page_view, name="manage_surveys"),
    path('project/<int:id>/surveys/<int:survey_id>/',
         edit_survey, name="edit_survey"),
    path('project/<int:survey_id>/', delete_survey, name="delete_survey"),
]

scope_urls = [
    path('manage_scopes', scope_views.manage_scopes, name="manage_scopes_page"),
    path('manage_project_scopes/<int:id>/',
         scope_views.manage_project_scopes, name='manage_project_scopes'),
    path('manage_survey_scopes/<int:id>/',
         scope_views.manage_survey_scopes, name='manage_survey_scopes'),
    path('delete_scope/<int:id>/', scope_views.delete_scope, name='delete_scope'),
    path('edit_scope/<int:id>/', scope_views.edit_scope, name='edit_scope'),
]
boq_urls = [
    path('manage_boqs/', boq_views.manage_boqs, name='manage_boqs'),
    path('manage_project_boqs/<int:id>/',
         boq_views.manage_project_boqs, name='manage_project_boqs'),
    path('create_boq/<int:survey_id>/', boq_views.create_boq, name='create_boq'),
    path('manage_boq_items/<int:id>/',
         boq_views.manage_boq_items, name='manage_boq_items'),
    path('add_materialboq/<int:id>/',
         boq_views.add_materialboq, name="add_materialboq"),
    path('add_serviceboq/<int:id>/',
         boq_views.add_serviceboq, name="add_serviceboq"),
    path('edit_material_boq_item/<int:id>/',
         boq_views.edit_materialboq, name="edit_material_boq_item"),
    path('delete_material_boq_item/<int:id>/',
         boq_views.delete_materialboq, name="delete_material_boq_item"),
    path('delete_service_boq_item/<int:id>/',
         boq_views.delete_serviceboq, name="delete_service_boq_item"),
    path('edit_service_boq_item/<int:id>/',
         boq_views.edit_serviceboq, name="edit_service_boq_item"),
]

pip_urls = [
    path('scope/<int:scope_id>/pips/',
         pip_views.pip_page_view, name='manage_pips'),
    path('scope/<int:scope_id>/pip/<int:pip_id>',
         pip_views.edit_pip_view, name='edit_pip'),
    path('scope/pip/<int:pip_id>', pip_views.delete_pip, name='delete_pip'),
]

settings_urls = [
    path('uom/', project_settings_view.unit_of_measure_view, name='manage_uom'),
    path('edit_uom/<int:uom_id>/',
         project_settings_view.edit_uom_view, name='edit_uom'),
    path('delete_uom/<int:uom_id>/',
         project_settings_view.delete_uom, name='delete_uom'),

    path('expenses/', project_settings_view.manage_expense_view,
         name='manage_expenses'),
    path('edit_expense/<int:expense_id>/',
         project_settings_view.edit_expense_view, name='edit_expense'),
    path('delete_expense/<int:expense_id>/',
         project_settings_view.delete_expense, name='delete_expense'),
]

budget_urls = [
    path('create_budget/<int:pip_id>/',
         budget_views.create_budget, name='create_budget'),
    path('manage_budgets/<int:budget_id>/',
         budget_views.manage_budgets_view, name='manage_budgets'),

    path('add_material_budget/<budget_id>/',
         budget_views.add_material_budget_view, name='add_material_budget'),
    path('edit_material_budget/<budget_id>/',
         budget_views.edit_material_budget_view, name='edit_material_budget'),
    path('delete_material_budget/<budget_id>/',
         budget_views.delete_material_budget_view, name='delete_material_budget'),

    path('add_execution_budget/<budget_id>/',
         budget_views.add_execution_budget_view, name='add_execution_budget'),
    path('edit_execution_budget/<budget_id>/',
         budget_views.edit_execution_budget_view, name='edit_execution_budget'),
    path('delete_execution_budget/<budget_id>/',
         budget_views.delete_execution_budget_view, name='delete_execution_budget'),

    path('add_expense_budget/<budget_id>/',
         budget_views.add_expense_budget_view, name='add_expense_budget'),
    path('edit_expense_budget/<budget_id>/',
         budget_views.edit_expense_budget_view, name='edit_expense_budget'),
    path('delete_expense_budget/<budget_id>/',
         budget_views.delete_expense_budget_view, name='delete_expense_budget'),

    path('get_material_unitcost/', budget_views.get_material_unitcost_view,
         name='get_material_unitcost'),
    path('get_expense_rate/', budget_views.get_expense_rate_view,
         name='get_expense_rate'),
]

field_managers_urls = [
    path('manage_field_managers/', field_manage_views.manage_field_managers,
         name='manage_field_managers'),
    path('delete_field_manager/<int:id>/',
         field_manage_views.delete_field_manager, name='delete_field_manager'),
    path('edit_field_manager/<int:id>/',
         field_manage_views.edit_field_manager, name="edit_field_manager"),
]

teams_urls = [
    path('manage_teams/', team_views.manage_teams_page, name='manage_teams'),
    path('delete_team/<int:id>/', team_views.delete_team, name='delete_team'),
    path('edit_team/<int:id>/', team_views.edit_team_page, name="edit_team"),
]

pip_team_urls = [
    path('manage_pip_teams/', team_views.manage_pip_team_page,
         name='manage_pip_teams'),
    path('delete_pip_team/<int:id>/',
         team_views.delete_pip_team, name='delete_pip_team'),
    path('edit_pip_team/<int:id>/',
         team_views.edit_pip_team_page, name="edit_pip_team"),
]

wage_sheets_urls = [
    path('manage_wage_sheets/', wage_sheet_views.manage_wage_sheets_page,
         name='manage_wage_sheets'),
    path('delete_wage_sheet/<int:id>/',
         wage_sheet_views.delete_wage_sheet, name='delete_wage_sheet'),
    path('edit_wage_sheet/<int:id>/',
         wage_sheet_views.edit_wage_sheet_page, name="edit_wage_sheet"),
    path('manage_wages/<int:wage_sheet_id>',
         wage_sheet_views.manage_wages_page, name='manage_wages'),
    path('add_wage_from_phone_number_page/<int:wage_sheet_id>/',
         wage_sheet_views.add_wage_from_phone_number_page, name='add_wage_from_phone_number_page'),

    path('delete_wage/<int:id>/', wage_sheet_views.delete_wage, name='delete_wage'),
    path('edit_wage/<int:id>/', wage_sheet_views.edit_wage_page, name="edit_wage"),
    path('manage_group_wages/<int:wage_sheet_id>',
         wage_sheet_views.manage_group_wages_page, name='manage_group_wages'),
    path('edit_wage_group/<int:id>/', wage_sheet_views.edit_group_wage_page, name="edit_wage_group"),
    path('delete_wage_group/<int:id>/', wage_sheet_views.delete_wage_group, name='delete_wage_group'),
    path('submit_wage_sheet/<int:wage_sheet_id>/',
         wage_sheet_views.submit_wage_sheet, name="submit_wage_sheet"),
    path('approve_or_reject_wage_sheets/', wage_sheet_views.approve_or_reject_wagesheets_page,
         name="approve_or_reject_wagesheets"),
    path('manage_submitted_sheet/<int:wage_sheet_id>/',
         wage_sheet_views.manage_submitted_sheet, name="manage_submitted_sheet"),
    path('approve_reject_wagesheet/<int:wagesheet_id>/',
         wage_sheet_views.approve_or_reject_wage_sheets_process, name="approve_reject_wagesheet"),
    path('reject_wage/', wage_sheet_views.reject_wage, name="reject_wage"),
    path('user_submitted_wage_sheets_page/', wage_sheet_views.user_submitted_wage_sheets_page,
         name="user_submitted_wage_sheets_page"),
    path('submitted_wage_sheets/<int:id>', wage_sheet_views.submitted_wage_sheet_page,
         name="submitted_wage_sheet_page"),
    path('retract_wage_sheet/<int:wage_sheet_id>/',
         wage_sheet_views.retract_wage_sheet, name="retract_wage_sheet"),
    path('current_wage_bill_sheets', wage_sheet_views.current_wage_bill_sheets_page, name="current_wage_bill_sheets"),
    path("wage_bill_sheets/<int:wage_bill_id>/", wage_sheet_views.wage_bill_sheets_page, name="wage_bill_sheets"),
    path("wage_sheet_pdf/<int:wage_sheet_id>/", wage_sheet_views.wage_sheet_pdf, name="wage_sheet_pdf"),
    path("approved_wage_sheets/", wage_sheet_views.approved_wage_sheets_page, name="approved_wage_sheets"),
    path("expired_wage_sheets/", wage_sheet_views.expired_wage_sheets_page, name="expired_wage_sheets_page")

]

segments_urls = [
    path('manage_segments/', segment_views.manage_segments_page,
         name='manage_segments'),
    path('delete_segment/<int:id>/',
         segment_views.delete_segment, name='delete_segment'),
    path('edit_segment/<int:id>/',
         segment_views.edit_segment_page, name="edit_segment"),
]

complaint_urls = [
    path('manage_complaints/<int:wage_sheet_id>',
         complaint_views.manage_complaints_page, name='manage_complaints'),
    path('delete_complaint/<int:id>/',
         complaint_views.delete_complaint, name='delete_complaint'),
    path('edit_complaint/<int:id>/',
         complaint_views.edit_complaint_page, name="edit_complaint"),
    path('reject_complaint/',
         wage_sheet_views.reject_complaint, name="reject_complaint"),
]

deduction_urls = [
    path('manage_deductions/<int:wage_sheet_id>',
         deduction_views.manage_deductions_page, name='manage_deductions'),
    path('delete_deduction/<int:id>/',
         deduction_views.delete_deduction, name='delete_deduction'),
    path('edit_deduction/<int:id>/',
         deduction_views.edit_deduction_page, name="edit_deduction"),
    path('reject_deduction/<int:deduction_id>/<int:role>/',
         wage_sheet_views.reject_deduction, name="reject_deduction"),
]

activity_urls = [
    path('activity_list/', activity_page_view, name='manage_activities'),
    path('edit_activity/<int:activity_id>/',
         edit_activity_view, name='edit_activity'),
    path('delete_activity/<int:activity_id>/',
         delete_activity_view, name='delete_activity'),
    path('get_activity_rate/', get_activity_rate, name='get_activity_rate'),
]

wage_bill_urls = [
    path('view_all_wage_bills/', wage_bill_views.view_all_wage_bills,
         name='view_all_wage_bills'),
    path('edit_wage_bill/<int:wage_bill_id>/',
         wage_bill_views.edit_wage_bill, name='edit_wage_bill'),
    path('delete_wage_bill/<int:wage_bill_id>/',
         wage_bill_views.delete_wage_bill, name='delete_wage_bill'),
    path('get_end_date/', wage_bill_views.get_end_date, name='get_end_date'),
    path('current_consolidated_wage_bill/', wage_bill_views.current_consolidated_wage_bill,
         name='current_consolidated_wage_bill'),
    path('consolidated_wage_bill_csv/<int:wage_bill_id>/', wage_bill_views.consolidated_wage_bill_payments_csv,
         name="consolidated_wage_bill_csv"),
    path('reset_wage_bill_payments/<int:wage_bill_id>/', wage_bill_views.reset_consolidated_wage_bill_payments,
         name="reset_wage_bill_payments"),
    path('consolidated_wage_bill/<int:wage_bill_id>/', wage_bill_views.consolidated_wage_bill,
         name="consolidated_wage_bill"),
    path('worker_wage_bill_breakdown/<int:wage_bill_id>/<int:worker_id>/', wage_bill_views.worker_wage_bill_breakdown,
         name="worker_wage_bill_breakdown"),
    path('wage_bill_breakdown/<int:wage_bill_id>/', wage_bill_views.wage_bill_payment_breakdown,
         name="wage_bill_breakdown"),
    path('consolidated_wage_bill_pdf/<int:wage_bill_id>/', wage_bill_views.consolidated_wage_bill_pdf,
         name="consolidated_wage_bill_pdf"),
    path('generate_consolidated_bill/<int:wage_bill_id>/', wage_bill_views.generate_consolidated_wage_bill_payments,
         name="generate_consolidated_wage_bill"),
    path('view_all_wage_bill_payments/<int:wage_bill_id>/', wage_bill_views.view_consolidated_wage_bill_payments,
         name="view_consolidated_wage_bill_payments"),
    path('wage_bill_managers/<int:wage_bill_id>/', wage_bill_views.wage_bill_manager_total,
         name="wage_bill_managers"),
    path('manager_supervisors/<int:wage_bill_id>/<int:manager>/', wage_bill_views.wage_bill_supervisor_total,
         name="manager_supervisors"),
    path('manager_payment_breakdown/<int:wage_bill_id>/<int:manager>/',
         wage_bill_views.wage_bill_manager_payment_breakdown,
         name="manager_payment_breakdown"),
    path('payments_dashboard/<int:wage_bill_id>/', wage_bill_views.payments_dashboard, name="payments_dashboard"),
    path('payment_stats_excel/<int:wage_bill_id>/', wage_bill_views.payment_stats_excel, name="payment_stats_excel"),

]

project_urls = [
    path('', dashboard_page, name='dashboard_page'),
    path('projects/', projects_page_view, name='manage_projects'),
    path('project_details/<int:project_id>/',
         project_details_view, name='project_details'),
    path('project_settings/', projects_settings_view, name='project_settings'),
    path('project/<int:project_id>/sites/',
         sites_page_view, name='manage_sites'),
    path('project/<int:project_id>/site/<int:site_id>/',
         site_details_view, name='site_details'),
]

user_urls = [
    path('manage_users/', user_views.manage_user_view,
         name='manage_users'),
    path("edit_user/<int:id>/", user_views.edit_user_view, name="edit_user"),
    path("delete_user/<int:id>/", user_views.delete_user_view, name="delete_user")
]

auth_urls = [
    path("super_admin_required_page/", super_admin_required_page,
         name="super_admin_required_page"),
    path("project_manager_required_page/", project_manager_required_page,
         name="project_manager_required_page"),
    path("supervisor_required_page/", supervisor_required_page,
         name="supervisor_required_page"),
    path("finance_officer_required_page/", finance_officer_required_page,
         name="finance_officer_required_page"),
]

notification_urls = [
    path("unread_notifications/", unread_notifications_page,
         name="unread_notifications_page"),
    path("notifications/", notifications_page,
         name="notifications_page"),
]

urlpatterns = activity_urls + project_urls + worker_urls + survey_urls + boq_urls + scope_urls + budget_urls + settings_urls + \
              pip_urls + field_managers_urls + teams_urls + pip_team_urls + wage_sheets_urls \
              + wage_bill_urls + segments_urls + complaint_urls + \
              deduction_urls + user_urls + auth_urls + notification_urls


# customJS routes
def javascript_settings():
    js_conf = {
        'get_material_unitcost': reverse('get_material_unitcost'),
        'get_expense_rate': reverse('get_expense_rate'),
        'get_activity_rate': reverse('get_activity_rate'),
        'get_end_date': reverse('get_end_date'),
        'reject_wage': reverse('reject_wage'),
    }
    return js_conf
