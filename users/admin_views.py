# users/views.py - Ajouter ces endpoints

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from credits.models import Credit
from decimal import Decimal
import secrets
import string

User = get_user_model()


def generate_temp_password():
    """Génère un mot de passe temporaire sécurisé"""
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(12))

class IsSuperUser:
    """Permission pour vérifier si c'est un admin"""
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


# ============ ADMIN - CRÉER UN BOUTIQUIER ============

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_boutiquier(request):
    """
    POST /api/admin/boutiquiers/create/
    Créer un nouveau boutiquier avec mot de passe temporaire
    
    Body:
    {
        "username": "boutiquier_nom",
        "email": "boutiquier@example.com",
        "first_name": "Nom",
        "last_name": "Prénom",
        "phone": "+221770000000"
    }
    """
    if not request.user.is_superuser:
        return Response(
            {'error': 'Permission refusée - Admin seulement'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    username = request.data.get('username', '').strip()
    email = request.data.get('email', '').strip()
    first_name = request.data.get('first_name', '').strip()
    last_name = request.data.get('last_name', '').strip()
    phone = request.data.get('phone', '').strip()
    
    # Validation
    if not username or not email:
        return Response(
            {'error': 'Username et email requis'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': f'Username "{username}" déjà utilisé'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(email=email).exists():
        return Response(
            {'error': f'Email "{email}" déjà utilisé'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Générer mot de passe temporaire
    temp_password = generate_temp_password()
    
    # Créer le boutiquier
    try:
        boutiquier = User.objects.create_user(
            username=username,
            email=email,
            password=temp_password,  # ← Hashé automatiquement par create_user
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role='boutiquier',
            status='active',
            is_active=True  # ← IMPORTANT: Actif immédiatement
        )
        
        return Response({
            'success': True,
            'message': f'Boutiquier créé avec succès',
            'boutiquier': {
                'id': boutiquier.id,
                'username': boutiquier.username,
                'email': boutiquier.email,
                'first_name': boutiquier.first_name,
                'last_name': boutiquier.last_name,
                'phone': boutiquier.phone,
                'role': boutiquier.role,
                'status': boutiquier.status,
                'is_active': boutiquier.is_active,
                'temp_password': temp_password,  # ← À communiquer au boutiquier
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': f'Erreur création: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )


class IsSuperUser:
    """Permission pour vérifier si c'est un admin"""
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

# ============ ADMIN - LISTER TOUS LES BOUTIQUIERS ============

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_boutiquiers(request):
    """
    GET /api/admin/boutiquiers/
    Lister tous les boutiquiers avec leurs montants
    Seulement pour les superadmins
    """
    if not request.user.is_superuser:
        return Response(
            {'error': 'Permission refusée'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    boutiquiers = User.objects.filter(role='boutiquier')
    
    data = []
    for b in boutiquiers:
        # Calculer les totaux
        b.calculate_totals()
        
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
            'clients_count': b.clients.filter(is_active=True).count(),
            'credits_count': Credit.objects.filter(
                client__boutiquier=b, 
                is_active=True
            ).count(),
        })
    
    return Response(data)


# ============ ADMIN - DÉTAILS D'UN BOUTIQUIER ============

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def boutiquier_detail(request, pk):
    """
    GET /api/admin/boutiquiers/{id}/
    Voir détails complets d'un boutiquier
    """
    if not request.user.is_superuser:
        return Response(
            {'error': 'Permission refusée'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        boutiquier = User.objects.get(id=pk, role='boutiquier')
    except User.DoesNotExist:
        return Response(
            {'error': 'Boutiquier non trouvé'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Calculer les totaux
    boutiquier.calculate_totals()
    
    # Récupérer ses clients
    from clients.models import Client
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
        'active_credits': Credit.objects.filter(
            client__boutiquier=boutiquier,
            is_active=True
        ).count(),
        'clients': [
            {
                'id': c.id,
                'name': c.name,
                'phone': c.phone,
                'status': c.status,
                'total_owed': sum(Decimal(cr.amount) for cr in c.credits.all()) or 0,
                'total_paid': sum(Decimal(cr.paid_amount) for cr in c.credits.all()) or 0,
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
            for c in credits[:10]  # Dernier 10 crédits
        ]
    })


# ============ ADMIN - DÉSACTIVER/ACTIVER UN BOUTIQUIER ============

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def toggle_boutiquier_status(request, pk):
    """
    PATCH /api/admin/boutiquiers/{id}/toggle-status/
    {
        "status": "inactive",  # ou "active" ou "archived"
        "reason": "N'a pas payé" (optionnel)
    }
    """
    if not request.user.is_superuser:
        return Response(
            {'error': 'Permission refusée'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        boutiquier = User.objects.get(id=pk, role='boutiquier')
    except User.DoesNotExist:
        return Response(
            {'error': 'Boutiquier non trouvé'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    new_status = request.data.get('status')
    if new_status not in ['active', 'inactive', 'archived']:
        return Response(
            {'error': 'Statut invalide. Utilisez: active, inactive ou archived'},
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


# ============ ADMIN - DÉSACTIVER/ACTIVER UN CRÉDIT ============

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def toggle_credit_status(request, pk):
    """
    PATCH /api/admin/credits/{id}/toggle-status/
    {
        "is_active": false  # ou true
    }
    """
    if not request.user.is_superuser:
        return Response(
            {'error': 'Permission refusée'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        credit = Credit.objects.get(id=pk)
    except Credit.DoesNotExist:
        return Response(
            {'error': 'Crédit non trouvé'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    is_active = request.data.get('is_active', True)
    credit.is_active = is_active
    
    if not is_active:
        credit.status = 'archived'
    
    credit.save()
    
    return Response({
        'success': True,
        'credit': {
            'id': credit.id,
            'is_active': credit.is_active,
            'status': credit.status
        }
    })


# ============ ADMIN - DÉSACTIVER/ACTIVER UN CLIENT ============

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def toggle_client_status(request, pk):
    """
    PATCH /api/admin/clients/{id}/toggle-status/
    {
        "status": "inactive"  # ou "active" ou "archived"
    }
    """
    if not request.user.is_superuser:
        return Response(
            {'error': 'Permission refusée'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    from clients.models import Client
    
    try:
        client = Client.objects.get(id=pk)
    except Client.DoesNotExist:
        return Response(
            {'error': 'Client non trouvé'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    new_status = request.data.get('status')
    if new_status not in ['active', 'inactive', 'archived']:
        return Response(
            {'error': 'Statut invalide'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    client.status = new_status
    if new_status in ['inactive', 'archived']:
        client.is_active = False
    else:
        client.is_active = True
    
    client.save()
    
    return Response({
        'success': True,
        'client': {
            'id': client.id,
            'name': client.name,
            'status': client.status,
            'is_active': client.is_active
        }
    })
