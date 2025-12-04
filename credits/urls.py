from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CreditViewSet, PaymentViewSet

app_name = 'credits'

router = DefaultRouter()
router.register(r'credits', CreditViewSet, basename='credit')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
]
