from django.urls import path, reverse
from .views import *

urlpatterns = [
    path('', clients_page_view, name='manage_clients'),
    path('delete_client', delete_client, name='delete_client'),
]


# JS routes
def javascript_settings():
    js_conf = {
        'delete_client': reverse('delete_client'),
    }

    return js_conf
