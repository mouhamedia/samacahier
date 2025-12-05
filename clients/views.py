from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Client
from .serializers import ClientSerializer, ClientAccessCodeSerializer
from users.permissions import IsBoutiquier
from credits.models import Credit


class ClientViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des clients."""
    
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated, IsBoutiquier]
    
    def get_queryset(self):
        """Retourne les clients du boutiquier connecté."""
        return Client.objects.filter(boutiquier=self.request.user)
    
    def perform_create(self, serializer):
        """Associe le client au boutiquier connecté."""
        serializer.save(boutiquier=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_clients(self, request):
        """Retourne tous les clients du boutiquier."""
        clients = self.get_queryset()
        serializer = self.get_serializer(clients, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def my_credits(self, request):
        """GET /api/clients/my-credits/ - Retourne les crédits du client connecté"""
        # Récupérer le code d'accès depuis les paramètres
        access_code = request.query_params.get('code')
        
        if not access_code:
            return Response(
                {'error': 'Code d\'accès requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            client = Client.objects.get(access_code=access_code.upper(), is_active=True)
        except Client.DoesNotExist:
            return Response(
                {'error': 'Client non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        credits = Credit.objects.filter(client=client).order_by('-created_at')
        
        credit_list = [
            {
                'id': credit.id,
                'product': credit.product or 'Crédit',
                'amount': float(credit.amount),
                'paid_amount': float(credit.paid_amount),
                'remaining': float(credit.amount - credit.paid_amount),
                'status': credit.status,
                'description': credit.description or '',
                'created_at': credit.created_at.isoformat(),
                'due_date': credit.due_date.isoformat() if credit.due_date else None,
            }
            for credit in credits
        ]
        
        return Response(credit_list)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def transactions(self, request):
        """GET /api/clients/transactions/ - Historique des transactions du client"""
        access_code = request.query_params.get('code')
        
        if not access_code:
            return Response(
                {'error': 'Code d\'accès requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            client = Client.objects.get(access_code=access_code.upper(), is_active=True)
        except Client.DoesNotExist:
            return Response(
                {'error': 'Client non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        credits = Credit.objects.filter(client=client).order_by('-created_at')
        
        transactions = []
        balance = 0
        
        for credit in credits:
            # Crédit créé
            transactions.append({
                'id': f'credit_{credit.id}',
                'date': credit.created_at.isoformat(),
                'type': 'credit',
                'description': f'Crédit: {credit.product or "Produit"}',
                'amount': float(credit.amount),
                'balance': float(balance + credit.amount),
            })
            balance += credit.amount
            
            # Paiement
            if credit.paid_amount > 0:
                transactions.append({
                    'id': f'payment_{credit.id}',
                    'date': credit.updated_at.isoformat(),
                    'type': 'payment',
                    'description': f'Paiement: {credit.product or "Produit"}',
                    'amount': float(credit.paid_amount),
                    'balance': float(balance - credit.paid_amount),
                })
                balance -= credit.paid_amount
        
        # Trier par date décroissante
        transactions = sorted(transactions, key=lambda x: x['date'], reverse=True)
        
        return Response(transactions)


class ClientAccessView(APIView):
    """Vue pour se connecter avec un code d'accès simple."""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        """
        Connexion simplifiée pour les clients.
        
        Body:
        {
            "access_code": "ABC123"
        }
        """
        access_code = request.data.get('access_code', '').strip().upper()
        
        if not access_code:
            return Response(
                {'error': 'Le code d\'accès est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            client = Client.objects.get(access_code=access_code, is_active=True)
        except Client.DoesNotExist:
            return Response(
                {'error': 'Code d\'accès invalide ou client inactif'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Générer un token JWT pour le client
        from rest_framework_simplejwt.tokens import RefreshToken
        
        refresh = RefreshToken()
        refresh['access_code'] = client.access_code
        refresh['client_id'] = client.id
        refresh['client_name'] = client.name
        
        access_token = str(refresh.access_token)
        
        # Retourner les infos du client et ses crédits
        credits = Credit.objects.filter(client=client)
        
        total_amount = sum(float(credit.amount) for credit in credits)
        total_paid = sum(float(credit.paid_amount) for credit in credits)
        remaining = total_amount - total_paid
        
        return Response({
            'access': access_token,  # ← JWT Token
            'client_id': client.id,
            'client_name': client.name,
            'access_code': client.access_code,
            'phone': client.phone,
            'email': client.email,
            'boutiquier_name': client.boutiquier.get_full_name() or client.boutiquier.username,
            'credits_info': {
                'total_credits': credits.count(),
                'total_amount': float(total_amount),
                'total_paid': float(total_paid),
                'remaining': float(remaining),
            }
        })

