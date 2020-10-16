from django.urls import path

from .views import scope_views, team_views, wage_sheet_views
from .views.project_views import *
from .views.sites_views import *
from .views.activity_list_views import *
import projects.views.worker_views  as worker_views
from .views.survey_views import *
import projects.views.boq_views as boq_views
from .views import pip_views
import projects.views.field_manager_views as field_manage_views

worker_urls = [
    path('manage_workers/', worker_views.manage_workers_page, name='manage_workers_page'),
    path('delete_worker/<int:id>/', worker_views.delete_worker, name='delete_worker'),
    path('edit_worker/<int:id>/', worker_views.edit_worker_page, name="edit_worker"),
]

survey_urls = [
    path('project/<int:id>/surveys', survey_page_view, name="manage_surveys"),
    path('project/<int:id>/surveys/<int:survey_id>/', edit_survey, name="edit_survey"),
    path('project/<int:survey_id>/', delete_survey, name="delete_survey"),
]

scope_urls = [
    path('manage_scopes', scope_views.manage_scopes, name="manage_scopes_page"),
    path('manage_project_scopes/<int:id>/', scope_views.manage_project_scopes, name='manage_project_scopes'),
    path('manage_survey_scopes/<int:id>/', scope_views.manage_survey_scopes, name='manage_survey_scopes'),
    path('delete_scope/<int:id>/', scope_views.delete_scope, name='delete_scope'),
    path('edit_scope/<int:id>/', scope_views.edit_scope, name='edit_scope'),
]
boq_urls = [
    path('manage_boqs/', boq_views.manage_boqs, name='manage_boqs'),
    path('manage_project_boqs/<int:id>/', boq_views.manage_project_boqs, name='manage_project_boqs'),
    path('create_boq/<int:survey_id>/', boq_views.create_boq, name='create_boq'),
    path('manage_boq_items/<int:id>/', boq_views.manage_boq_items, name='manage_boq_items'),
    path('add_materialboq/<int:id>/', boq_views.add_materialboq, name="add_materialboq"),
    path('add_serviceboq/<int:id>/', boq_views.add_serviceboq, name="add_serviceboq"),
    path('edit_material_boq_item/<int:id>/', boq_views.edit_materialboq, name="edit_material_boq_item"),
    path('delete_material_boq_item/<int:id>/', boq_views.delete_materialboq, name="delete_material_boq_item"),
    path('delete_service_boq_item/<int:id>/', boq_views.delete_serviceboq, name="delete_service_boq_item"),
    path('edit_service_boq_item/<int:id>/', boq_views.edit_serviceboq, name="edit_service_boq_item"),
]

pip_urls = [
    path('scope/<int:scope_id>/pips/', pip_views.pip_page_view, name='manage_pips'),
    path('scope/<int:scope_id>/pip/<int:pip_id>', pip_views.edit_pip_view, name='edit_pip'),
    path('scope/pip/<int:pip_id>', pip_views.delete_pip, name='delete_pip'),
]

field_managers_urls = [
    path('manage_field_managers/', field_manage_views.manage_field_managers, name='manage_field_managers'),
    path('delete_field_manager/<int:id>/', field_manage_views.delete_field_manager, name='delete_field_manager'),
    path('edit_field_manager/<int:id>/', field_manage_views.edit_field_manager, name="edit_field_manager"),
]

teams_urls = [
    path('manage_teams/', team_views.manage_teams_page, name='manage_teams'),
    path('delete_team/<int:id>/', team_views.delete_team, name='delete_team'),
    path('edit_team/<int:id>/', team_views.edit_team_page, name="edit_team"),
]

pip_team_urls = [
    path('manage_pip_teams/', team_views.manage_pip_team_page, name='manage_pip_teams'),
    path('delete_pip_team/<int:id>/', team_views.delete_pip_team, name='delete_pip_team'),
    path('edit_pip_team/<int:id>/', team_views.edit_pip_team_page, name="edit_pip_team"),
]

wage_sheets_urls = [
    path('manage_wage_sheets/', wage_sheet_views.manage_wage_sheets_page, name='manage_wage_sheets'),
    path('delete_wage_sheet/<int:id>/', wage_sheet_views.delete_wage_sheet, name='delete_wage_sheet'),
    path('edit_wage_sheet/<int:id>/', wage_sheet_views.edit_wage_sheet_page, name="edit_wage_sheet"),
    path('manage_wages/<int:wage_sheet_id>', wage_sheet_views.manage_wages_page, name='manage_wages'),
    path('delete_wage/<int:id>/', wage_sheet_views.delete_wage, name='delete_wage'),
    path('edit_wage/<int:id>/', wage_sheet_views.edit_wage_page, name="edit_wage"),
]

urlpatterns = [
    path('', index_page, name='index_page'),
    path('projects/', projects_page_view, name='manage_projects'),
    path('project_details/<int:project_id>/', project_details_view, name='project_details'),
    path('project_settings/', projects_settings_view, name='project_settings'),
    path('project/<int:project_id>/sites/', sites_page_view, name='manage_sites'),
    path('project/<int:project_id>/site/<int:site_id>/', site_details_view, name='site_details'),
    path('activity_list/', activity_page_view, name='manage_activities'),
    path('edit_activity/<int:activity_id>/', edit_activity_view, name='edit_activity'),
    path('delete_activity/<int:activity_id>/', delete_activity_view, name='delete_activity'),
] + worker_urls + survey_urls + boq_urls + scope_urls + \
              pip_urls+field_managers_urls + teams_urls+pip_team_urls+wage_sheets_urls

