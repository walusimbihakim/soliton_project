from django.urls import path
from .views.project_views import *
from .views.sites_views import *
from .views.activity_list_views import *

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
]
