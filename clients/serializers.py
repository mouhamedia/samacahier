from rest_framework import serializers
from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    """Sérializeur pour les clients."""
    
    boutiquier_name = serializers.CharField(source='boutiquier.username', read_only=True)
    
    class Meta:
        model = Client
        fields = ('id', 'boutiquier', 'boutiquier_name', 'name', 'phone', 'email', 'address', 'access_code', 'is_active', 'created_at', 'updated_at')
        read_only_fields = ('id', 'boutiquier', 'access_code', 'created_at', 'updated_at')


class ClientAccessCodeSerializer(serializers.Serializer):
    """Sérializeur pour la connexion par code d'accès."""
    access_code = serializers.CharField(max_length=10, required=True)
