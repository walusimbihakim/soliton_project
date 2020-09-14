from django.urls import path
from .views.project_views import *
from .views.sites_views import *
from .views.activity_list_views import *
import projects.views.worker_views  as worker_views
import projects.views.boq_views as boq_views

worker_urls = [
    path('manage_workers/', worker_views.manage_workers_page, name='manage_workers_page'),
    path('delete_worker/<int:id>/', worker_views.delete_worker, name='delete_worker'),
    path('edit_worker/<int:id>/', worker_views.edit_worker_page, name="edit_worker"),
]

boq_urls = [
    path('manage_boqs/', boq_views.manage_boqs, name='manage_boqs'),
    path('manage_project_boqs/<int:id>/', boq_views.manage_project_boqs, name='manage_project_boqs'),
    path('create_boq/<int:survey_id>/', boq_views.create_boq, name='create_boq'),
    path('manage_boq_items/<int:id>/', boq_views.manage_boq_items, name='manage_boq_items'),
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

