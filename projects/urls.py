from django.urls import path
from .views.project_views import *
from .views.sites_views import *
from .views.activity_list_views import *
import projects.views.worker_views  as worker_views
from .views.survey_views import *
import projects.views.boq_views as boq_views

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
] + worker_urls + survey_urls
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
              ] + worker_urls + boq_urls

