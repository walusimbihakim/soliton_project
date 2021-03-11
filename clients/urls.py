from django.urls import path, reverse
from .views import *

urlpatterns = [
    path('', clients_page_view, name='manage_clients'),
    path('delete_client/<int:client_id>/', delete_client, name='delete_client'),
]


