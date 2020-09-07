from django.urls import path
from .views.project_views import *
from .views.sites_views import *
import projects.views.worker_views  as worker_views

worker_urls = [
    path('manage_workers/', worker_views.manage_workers_page, name='manage_workers_page'),
    path('delete_worker/<int:id>/', worker_views.delete_worker, name='delete_worker'),
    path('edit_worker/<int:id>/', worker_views.edit_worker_page, name="edit_worker"),
]
urlpatterns = [
                  path('', index_page, name='index_page'),
                  path('projects/', projects_page_view, name='manage_projects'),
                  path('project_details/<int:project_id>/', project_details_view, name='project_details'),
                  path('project_settings/', projects_settings_view, name='project_settings'),
                  path('project/<int:project_id>/sites/', sites_page_view, name='manage_sites'),
                  path('project/<int:project_id>/site/<int:site_id>/', site_details_view, name='site_details')
              ] + worker_urls
