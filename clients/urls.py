from django.urls import path, reverse
from .views import *

urlpatterns = [
    path('', clients_page_view, name='manage_clients'),
    path('delete_client/<int:client_id>/', delete_client, name='delete_client'),
]


# customJS routes
def javascript_settings():
    js_conf = {
        'delete_client': reverse('delete_client'),
    }

    return js_conf
