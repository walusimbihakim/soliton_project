from django.urls import path
from .views.project_views import *
from .views.sites_views import *

urlpatterns = [
    path('', index_page, name='index_page'),
    path('projects/', projects_page_view, name='manage_projects'),
    path('project_details/<int:project_id>/', project_details_view, name='project_details'),
    path('project_settings/', projects_settings_view, name='project_settings'),
    path('project/<int:project_id>/sites/', sites_page_view, name='manage_sites'),
    path('project/<int:project_id>/site/<int:site_id>/', site_details_view, name='site_details'),
]
