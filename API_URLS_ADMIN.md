# samacahier/urls.py - Ajouter dans urlpatterns

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/clients/', include('clients.urls')),
    path('api/credits/', include('credits.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    
    # ← ADMIN ENDPOINTS
    path('api/admin/boutiquiers/', include('users.admin_urls')),
]

# ============================================
# users/admin_urls.py - CRÉER CE FICHIER
# ============================================

from django.urls import path
from . import admin_views

urlpatterns = [
    # Lister tous les boutiquiers
    path('', admin_views.list_boutiquiers, name='list_boutiquiers'),
    
    # Détails d'un boutiquier
    path('<int:pk>/', admin_views.boutiquier_detail, name='boutiquier_detail'),
    
    # Désactiver/activer un boutiquier
    path('<int:pk>/toggle-status/', admin_views.toggle_boutiquier_status, name='toggle_boutiquier'),
    
    # Désactiver/activer un crédit
    path('credits/<int:pk>/toggle-status/', admin_views.toggle_credit_status, name='toggle_credit'),
    
    # Désactiver/activer un client
    path('clients/<int:pk>/toggle-status/', admin_views.toggle_client_status, name='toggle_client'),
]
