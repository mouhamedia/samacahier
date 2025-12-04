from rest_framework import serializers
from .models import Credit, Payment


class PaymentSerializer(serializers.ModelSerializer):
    """Sérializeur pour les paiements."""
    
    class Meta:
        model = Payment
        fields = ('id', 'credit', 'amount', 'payment_date', 'payment_method', 'note', 'created_at')
        read_only_fields = ('id', 'payment_date', 'created_at')


class CreditSerializer(serializers.ModelSerializer):
    """Sérializeur pour les crédits."""
    
    payments = PaymentSerializer(many=True, read_only=True)
    remaining_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    client_name = serializers.CharField(source='client.name', read_only=True)
    
    class Meta:
        model = Credit
        fields = ('id', 'client', 'client_name', 'boutiquier', 'amount', 'paid_amount', 'remaining_amount', 'status', 'description', 'due_date', 'payments', 'created_at', 'updated_at')
        read_only_fields = ('id', 'boutiquier', 'paid_amount', 'created_at', 'updated_at')
