from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

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
        
        # Retourner les infos du client et ses crédits
        credits = Credit.objects.filter(client=client)
        
        total_amount = sum(credit.amount for credit in credits)
        total_paid = sum(credit.paid_amount for credit in credits)
        remaining = total_amount - total_paid
        
        return Response({
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
                'credits': [
                    {
                        'id': credit.id,
                        'amount': float(credit.amount),
                        'paid_amount': float(credit.paid_amount),
                        'remaining': float(credit.amount - credit.paid_amount),
                        'status': credit.status,
                        'description': credit.description,
                        'due_date': credit.due_date,
                    }
                    for credit in credits.order_by('-created_at')
                ]
            }
        })

