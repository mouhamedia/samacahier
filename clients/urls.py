from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ClientViewSet, ClientAccessView

app_name = 'clients'

router = DefaultRouter()
router.register(r'', ClientViewSet, basename='client')

urlpatterns = [
    path('', include(router.urls)),
    path('access/', ClientAccessView.as_view(), name='client-access'),
]
