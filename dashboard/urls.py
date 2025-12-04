from django.urls import path

from .views import DashboardView, ClientDashboardView

app_name = 'dashboard'

urlpatterns = [
    path('boutiquier/', DashboardView.as_view(), name='boutiquier-dashboard'),
    path('client/', ClientDashboardView.as_view(), name='client-dashboard'),
]
