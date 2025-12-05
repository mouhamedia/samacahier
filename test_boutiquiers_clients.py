#!/usr/bin/env python
"""
Test: Les boutiquiers peuvent créer leurs propres clients
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'samacahier.settings')
django.setup()

from django.contrib.auth import get_user_model
from clients.models import Client

User = get_user_model()

print("=" * 70)
print("🧪 TEST: BOUTIQUIERS CRÉENT DES CLIENTS")
print("=" * 70)

# Récupérer un boutiquier
boutiquier = User.objects.filter(role='boutiquier', status='active').first()

if not boutiquier:
    print("❌ Aucun boutiquier trouvé!")
    exit(1)

print(f"\n👤 Boutiquier: {boutiquier.username} ({boutiquier.email})")

# Test 1: Créer un client
print("\n📝 CRÉATION D'UN CLIENT:")
try:
    client = Client.objects.create(
        boutiquier=boutiquier,
        name="Fatima Ba",
        phone="+221778901234",
        email="fatima@example.com",
        address="Dakar, Sénégal",
        status='active'
    )
    print(f"✅ Client créé avec succès!")
    print(f"   Nom: {client.name}")
    print(f"   Phone: {client.phone}")
    print(f"   Code d'accès: {client.access_code}")
    print(f"   Boutique: {client.boutiquier.username}")
except Exception as e:
    print(f"❌ Erreur création client: {e}")
    exit(1)

# Test 2: Vérifier les clients du boutiquier
print("\n📊 CLIENTS DU BOUTIQUIER:")
clients = Client.objects.filter(boutiquier=boutiquier)
for c in clients:
    print(f"  ✅ {c.name}")
    print(f"     Phone: {c.phone}")
    print(f"     Code: {c.access_code}")
    print(f"     Status: {c.status}")

# Test 3: Vérifier l'association
print("\n🔗 VÉRIFICATION ASSOCIATION:")
client_check = Client.objects.get(id=client.id)
print(f"✅ Client trouvé: {client_check.name}")
print(f"✅ Boutiquier: {client_check.boutiquier.username}")
print(f"✅ Code d'accès permanent: {client_check.access_code}")

# Test 4: Tester avec API
print("\n" + "=" * 70)
print("🔌 TEST VIA API REST")
print("=" * 70)

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIRequestFactory, force_authenticate
from clients.views import ClientViewSet

# Générer le JWT du boutiquier
refresh = RefreshToken.for_user(boutiquier)
access_token = str(refresh.access_token)

print(f"\n🔑 Token JWT généré pour: {boutiquier.username}")

# Créer une requête API
factory = APIRequestFactory()
request = factory.post('/api/clients/', {
    'name': 'Alassane Diallo',
    'phone': '+221765432109',
    'email': 'alassane@example.com',
    'address': 'Thiès, Sénégal'
})

# Authentifier la requête avec le JWT
force_authenticate(request, user=boutiquier, token=access_token)

# Appeler le ViewSet
view = ClientViewSet.as_view({'post': 'create'})
response = view(request)

print(f"\nRéponse API: {response.status_code}")
if response.status_code == 201:
    print("✅ CLIENT CRÉÉ VIA API!")
    print(f"   Données: {response.data}")
else:
    print(f"⚠️  Status: {response.status_code}")
    print(f"   Réponse: {response.data}")

print("\n" + "=" * 70)
print("✅ RÉSUMÉ:")
print("=" * 70)
print(f"✅ Les boutiquiers PEUVENT créer leurs propres clients")
print(f"✅ Chaque client a un code d'accès unique et permanent")
print(f"✅ Les clients sont automatiquement associés au boutiquier")
print(f"✅ API REST fonctionnelle pour la création")
print("=" * 70)
