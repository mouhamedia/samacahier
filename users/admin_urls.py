from django.urls import path
from . import admin_views

urlpatterns = [
    # Boutiquiers
    path('boutiquiers/', admin_views.list_boutiquiers, name='list_boutiquiers'),
    path('boutiquiers/create/', admin_views.create_boutiquier, name='create_boutiquier'),
    path('boutiquiers/<int:pk>/', admin_views.boutiquier_detail, name='boutiquier_detail'),
    path('boutiquiers/<int:pk>/toggle-status/', admin_views.toggle_boutiquier_status, name='toggle_boutiquier_status'),
    
    # Clients
    path('clients/<int:client_id>/toggle-status/', admin_views.toggle_client_status, name='toggle_client_status'),
    
    # Crédits
    path('credits/<int:credit_id>/toggle-status/', admin_views.toggle_credit_status, name='toggle_credit_status'),
]
