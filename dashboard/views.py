from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Q
from datetime import datetime, timedelta

from credits.models import Credit, Payment
from clients.models import Client
from users.permissions import IsBoutiquier


class DashboardView(views.APIView):
    """Vue pour le tableau de bord des boutiquiers."""
    
    permission_classes = [IsAuthenticated, IsBoutiquier]
    
    def get(self, request):
        """Retourne les statistiques du tableau de bord."""
        user = request.user
        
        # Récupérer tous les clients et crédits du boutiquier
        clients = Client.objects.filter(boutiquier=user)
        credits = Credit.objects.filter(boutiquier=user)
        
        # Statistiques générales
        total_clients = clients.count()
        total_credits = credits.count()
        
        # Statistiques sur les montants
        total_amount = credits.aggregate(Sum('amount'))['amount__sum'] or 0
        total_paid = credits.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
        total_remaining = total_amount - total_paid
        
        # Statistiques par statut
        credits_by_status = {
            'pending': credits.filter(status='pending').count(),
            'partial': credits.filter(status='partial').count(),
            'paid': credits.filter(status='paid').count(),
            'overdue': credits.filter(status='overdue').count(),
        }
        
        # Crédits en retard
        today = datetime.now().date()
        overdue_credits = credits.filter(due_date__lt=today, status__in=['pending', 'partial']).count()
        
        # Top 5 clients avec plus de crédits
        top_clients = clients.annotate(
            credit_count=Count('credits'),
            total_credit=Sum('credits__amount')
        ).order_by('-total_credit')[:5]
        
        top_clients_data = [{
            'id': client.id,
            'name': client.name,
            'credit_count': client.credit_count,
            'total_credit': client.total_credit,
        } for client in top_clients]
        
        # Paiements du mois
        current_month = datetime.now().month
        current_year = datetime.now().year
        payments_this_month = Payment.objects.filter(
            credit__boutiquier=user,
            payment_date__month=current_month,
            payment_date__year=current_year
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Panier moyen par client
        average_credit = total_amount / total_clients if total_clients > 0 else 0
        
        dashboard_data = {
            'general_stats': {
                'total_clients': total_clients,
                'total_credits': total_credits,
                'total_amount': total_amount,
                'total_paid': total_paid,
                'total_remaining': total_remaining,
                'average_credit_per_client': average_credit,
            },
            'credits_by_status': credits_by_status,
            'overdue_credits': overdue_credits,
            'top_clients': top_clients_data,
            'payments_this_month': payments_this_month,
        }
        
        return Response(dashboard_data)


class ClientDashboardView(views.APIView):
    """Vue pour le tableau de bord des clients."""
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Retourne les crédits du client connecté."""
        user = request.user
        
        # Récupérer les crédits du client
        credits = Credit.objects.filter(client__user=user) if hasattr(user, 'client') else []
        
        if not credits.exists():
            return Response({
                'total_credits': 0,
                'total_amount': 0,
                'total_paid': 0,
                'total_remaining': 0,
                'credits': []
            })
        
        total_amount = credits.aggregate(Sum('amount'))['amount__sum'] or 0
        total_paid = credits.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
        
        return Response({
            'total_credits': credits.count(),
            'total_amount': total_amount,
            'total_paid': total_paid,
            'total_remaining': total_amount - total_paid,
            'credits': [
                {
                    'id': credit.id,
                    'boutiquier': credit.boutiquier.username,
                    'amount': credit.amount,
                    'paid_amount': credit.paid_amount,
                    'status': credit.status,
                    'due_date': credit.due_date,
                } for credit in credits
            ]
        })
