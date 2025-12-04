# 🔧 API ET MODÈLES - DÉSACTIVATION BOUTIQUIERS

## 📊 MODÈLE CLIENT MODIFIÉ

```python
# clients/models.py

from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Client(models.Model):
    STATUS_CHOICES = [
        ('active', 'Actif'),
        ('inactive', 'Inactif'),
        ('archived', 'Archivé'),
    ]
    
    boutiquier = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    
    # CODE UNIQUE & PERMANENT
    access_code = models.CharField(max_length=20, unique=True, editable=False)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.access_code:
            self.access_code = self.generate_unique_code()
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_unique_code():
        """Générer un code unique: ABC-DE-001"""
        code = str(uuid.uuid4())[:8].upper()
        return f"{code}"
    
    def __str__(self):
        return f"{self.name} ({self.access_code})"
```

---

## 💰 MODÈLE CRÉDIT MODIFIÉ

```python
# credits/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Credit(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('partial', 'Partiellement payé'),
        ('paid', 'Payé'),
        ('overdue', 'En retard'),
        ('archived', 'Archivé'),
    ]
    
    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE, related_name='credits')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    product = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    is_active = models.BooleanField(default=True)  # ← Peut être désactivé
    
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Crédit {self.client.name} - {self.amount} XOF"
```

---

## 👤 MODÈLE UTILISATEUR (CustomUser)

```python
# users/models.py

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('boutiquier', 'Boutiquier'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    phone = models.CharField(max_length=20, blank=True)
    
    # ← DÉSACTIVATION (pas suppression)
    is_active = models.BooleanField(default=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Actif'),
            ('inactive', 'Inactif - Non payé'),
            ('archived', 'Archivé'),
        ],
        default='active'
    )
    
    total_owed = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0,
        help_text="Montant total dû par ce boutiquier"
    )
    
    paid_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0,
        help_text="Montant payé par ce boutiquier"
    )
    
    def calculate_totals(self):
        """Calculer le montant total dû et payé"""
        credits = Credit.objects.filter(
            client__boutiquier=self,
            is_active=True
        )
        
        self.total_owed = sum(c.amount for c in credits)
        self.paid_amount = sum(c.paid_amount for c in credits)
        self.save()
    
    def __str__(self):
        return f"{self.username} ({self.role})"
```

---

## 📡 API ENDPOINTS

### 1️⃣ **Lister tous les Boutiquiers (Admin)**

```python
# users/views.py

from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsSuperUser])
def list_boutiquiers(request):
    """
    GET /api/admin/boutiquiers/
    Lister tous les boutiquiers avec leurs montants
    """
    boutiquiers = CustomUser.objects.filter(role='boutiquier')
    
    data = []
    for b in boutiquiers:
        b.calculate_totals()  # Mettre à jour les totaux
        
        data.append({
            'id': b.id,
            'username': b.username,
            'email': b.email,
            'first_name': b.first_name,
            'last_name': b.last_name,
            'phone': b.phone,
            'status': b.status,  # active, inactive, archived
            'is_active': b.is_active,
            'total_owed': float(b.total_owed),
            'paid_amount': float(b.paid_amount),
            'remaining': float(b.total_owed - b.paid_amount),
            'clients_count': b.clients.count(),
            'credits_count': Credit.objects.filter(client__boutiquier=b).count(),
        })
    
    return Response(data)
```

### 2️⃣ **Désactiver/Activer un Boutiquier**

```python
@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsSuperUser])
def toggle_boutiquier_status(request, pk):
    """
    PATCH /api/admin/boutiquiers/{id}/toggle-status/
    {
        "status": "inactive",  # ou "active"
        "reason": "N'a pas payé"
    }
    """
    try:
        boutiquier = CustomUser.objects.get(id=pk, role='boutiquier')
    except CustomUser.DoesNotExist:
        return Response(
            {'error': 'Boutiquier non trouvé'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    new_status = request.data.get('status')
    if new_status not in ['active', 'inactive', 'archived']:
        return Response(
            {'error': 'Statut invalide'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # ← Désactiver mais NE PAS supprimer
    boutiquier.status = new_status
    if new_status in ['inactive', 'archived']:
        boutiquier.is_active = False
    else:
        boutiquier.is_active = True
    
    boutiquier.save()
    
    return Response({
        'success': True,
        'message': f'Boutiquier {new_status}',
        'boutiquier': {
            'id': boutiquier.id,
            'username': boutiquier.username,
            'status': boutiquier.status,
            'is_active': boutiquier.is_active
        }
    })
```

### 3️⃣ **Désactiver/Activer un Crédit**

```python
@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsSuperUser])
def toggle_credit_status(request, pk):
    """
    PATCH /api/admin/credits/{id}/toggle-status/
    {
        "is_active": false
    }
    """
    try:
        credit = Credit.objects.get(id=pk)
    except Credit.DoesNotExist:
        return Response(
            {'error': 'Crédit non trouvé'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    credit.is_active = request.data.get('is_active', True)
    credit.status = 'archived' if not credit.is_active else credit.status
    credit.save()
    
    return Response({
        'success': True,
        'credit': {
            'id': credit.id,
            'is_active': credit.is_active,
            'status': credit.status
        }
    })
```

### 4️⃣ **Obtenir détails d'un Boutiquier**

```python
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsSuperUser])
def boutiquier_detail(request, pk):
    """
    GET /api/admin/boutiquiers/{id}/
    Voir détails d'un boutiquier
    """
    try:
        boutiquier = CustomUser.objects.get(id=pk, role='boutiquier')
    except CustomUser.DoesNotExist:
        return Response(
            {'error': 'Boutiquier non trouvé'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Calculer les totaux
    boutiquier.calculate_totals()
    
    # Récupérer ses clients
    clients = Client.objects.filter(boutiquier=boutiquier)
    
    # Récupérer ses crédits
    credits = Credit.objects.filter(client__boutiquier=boutiquier)
    
    return Response({
        'id': boutiquier.id,
        'username': boutiquier.username,
        'email': boutiquier.email,
        'first_name': boutiquier.first_name,
        'last_name': boutiquier.last_name,
        'phone': boutiquier.phone,
        'status': boutiquier.status,
        'is_active': boutiquier.is_active,
        'total_owed': float(boutiquier.total_owed),
        'paid_amount': float(boutiquier.paid_amount),
        'remaining': float(boutiquier.total_owed - boutiquier.paid_amount),
        'clients_count': clients.count(),
        'credits_count': credits.count(),
        'clients': [
            {
                'id': c.id,
                'name': c.name,
                'status': c.status,
                'total_owed': sum(cr.amount for cr in c.credits.all()),
                'total_paid': sum(cr.paid_amount for cr in c.credits.all()),
            }
            for c in clients
        ],
        'credits': [
            {
                'id': c.id,
                'client_name': c.client.name,
                'amount': float(c.amount),
                'paid_amount': float(c.paid_amount),
                'product': c.product,
                'status': c.status,
                'is_active': c.is_active,
            }
            for c in credits
        ]
    })
```

---

## 📐 ROUTES URL

```python
# users/urls.py ou samacahier/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Admin endpoints
    path('api/admin/boutiquiers/', views.list_boutiquiers, name='list_boutiquiers'),
    path('api/admin/boutiquiers/<int:pk>/', views.boutiquier_detail, name='boutiquier_detail'),
    path('api/admin/boutiquiers/<int:pk>/toggle-status/', views.toggle_boutiquier_status, name='toggle_boutiquier_status'),
    path('api/admin/credits/<int:pk>/toggle-status/', views.toggle_credit_status, name='toggle_credit_status'),
]
```

---

## 🗄️ MIGRATION

```bash
# Générer la migration
python manage.py makemigrations

# Appliquer la migration
python manage.py migrate
```

---

## 📊 FLUX COMPLET

```
1. Admin accède au dashboard
2. Voit liste de tous les boutiquiers avec:
   - Montant total dû
   - Montant payé
   - Restant
   - Nombre de clients
   - Nombre de crédits
   - Statut (actif/inactif)

3. Admin clique sur un boutiquier
4. Voit:
   - Tous ses clients
   - Tous ses crédits
   - Détails financiers

5. Admin voit qu'il n'a pas payé
6. Clique "Désactiver"
7. Boutiquier reste en BDD
8. Mais statut = "inactive"
9. Boutiquier ne peut plus se connecter
10. Ses données restent visibles

11. Quand il paie:
12. Admin clique "Activer"
13. Boutiquier peut se reconnecter ✅
```

---

## ✨ DONNÉES CONSERVÉES

```
Admin désactive Boutiquier
    ↓
Boutiquier NON SUPPRIMÉ ✅
    ↓
Tous ses clients conservés ✅
    ↓
Tous ses crédits conservés ✅
    ↓
Paiements historique conservé ✅
    ↓
Juste marqué comme "inactif" ⚠️
    ↓
Quand il paie → Réactiver ✅
```

---

## 🔐 PERMISSIONS

```python
# Seulement superadmin peut:
✅ Voir tous les boutiquiers
✅ Voir montants
✅ Désactiver
✅ Activer
✅ Voir les crédits

# Boutiquier peut:
✅ Voir ses clients
✅ Créer crédits
✅ Ajouter paiements

# Client peut:
✅ Voir ses crédits
✅ Rien d'autre
```

---

## 💾 BASE DE DONNÉES

```sql
-- USERS table (modifié)
id | username | role | status | total_owed | paid_amount | is_active

-- CLIENTS table (modifié)
id | name | boutiquier_id | access_code | status | is_active

-- CREDITS table (modifié)
id | client_id | amount | paid_amount | product | status | is_active
```

---

## 🎯 RÉSUMÉ

| Action | Avant | Après |
|--------|-------|-------|
| **Désactiver Boutiquier** | ❌ Impossible | ✅ Status = "inactive" |
| **Données conservées** | N/A | ✅ 100% conservé |
| **Peut se reconnecter** | N/A | ❌ Non (is_active=False) |
| **Admin voit toujours** | N/A | ✅ Oui |
| **Réactivation** | N/A | ✅ Un clic |

