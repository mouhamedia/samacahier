"""
URL configuration for SamaCahier project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls', namespace='users')),
    path('api/clients/', include('clients.urls', namespace='clients')),
    path('api/credits/', include('credits.urls', namespace='credits')),
    path('api/dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('api/admin/', include('users.admin_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
