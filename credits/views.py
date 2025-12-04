from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Q
from datetime import datetime

from .models import Credit, Payment
from .serializers import CreditSerializer, PaymentSerializer
from users.permissions import IsBoutiquier


class CreditViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des crédits."""
    
    serializer_class = CreditSerializer
    permission_classes = [permissions.IsAuthenticated, IsBoutiquier]
    
    def get_queryset(self):
        """Retourne les crédits du boutiquier connecté."""
        return Credit.objects.filter(boutiquier=self.request.user)
    
    def perform_create(self, serializer):
        """Associe le crédit au boutiquier connecté."""
        serializer.save(boutiquier=self.request.user)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Retourne les statistiques des crédits."""
        credits = self.get_queryset()
        
        total_amount = credits.aggregate(Sum('amount'))['amount__sum'] or 0
        total_paid = credits.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
        
        stats = {
            'total_credits': credits.count(),
            'total_amount': total_amount,
            'total_paid': total_paid,
            'remaining': total_amount - total_paid,
            'by_status': {
                'pending': credits.filter(status='pending').count(),
                'partial': credits.filter(status='partial').count(),
                'paid': credits.filter(status='paid').count(),
                'overdue': credits.filter(status='overdue').count(),
            }
        }
        return Response(stats)
    
    @action(detail=True, methods=['post'])
    def add_payment(self, request, pk=None):
        """Ajoute un paiement à un crédit."""
        credit = self.get_object()
        serializer = PaymentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(credit=credit)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des paiements."""
    
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsBoutiquier]
    
    def get_queryset(self):
        """Retourne les paiements des crédits du boutiquier."""
        return Payment.objects.filter(credit__boutiquier=self.request.user)
    
    def perform_create(self, serializer):
        """Crée un paiement."""
        serializer.save()
