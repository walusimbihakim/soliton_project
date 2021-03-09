from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('projects.urls')),
    path('clients/', include('clients.urls')),
    path('auth/', include('authentication.urls')),
]

handler404 = 'custom_errors.views.error_404'
handler500 = 'custom_errors.views.error_500'
handler403 = 'custom_errors.views.error_403'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
