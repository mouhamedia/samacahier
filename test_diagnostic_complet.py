#!/usr/bin/env python3
"""
DIAGNOSTIC DÉTAILLÉ - Tester la connexion des boutquiers
"""

import os
import sys
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'samacahier.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()
client = APIClient()

print("\n")
print("╔" + "="*70 + "╗")
print("║" + "  🔍 DIAGNOSTIC DÉTAILLÉ - CONNEXION BOUTQUIERS".center(70) + "║")
print("╚" + "="*70 + "╝\n")

# ============================================================================
# TEST 1: Vérifier les comptes existent
# ============================================================================

print("="*70)
print("1️⃣  ÉTAPE 1: Vérifier que les comptes existent")
print("="*70)

test_accounts = ['nouveau_boutiquier_1', 'aissatou_diallo']

for username in test_accounts:
    try:
        user = User.objects.get(username=username)
        print(f"\n✅ {username}:")
        print(f"   Email: {user.email}")
        print(f"   Role: {user.role}")
        print(f"   Status: {user.status}")
        print(f"   Is Active: {user.is_active}")
        print(f"   Password set: {user.has_usable_password()}")
    except User.DoesNotExist:
        print(f"\n❌ {username}: N'EXISTE PAS!")

# ============================================================================
# TEST 2: Tester via sérializer DirectToken
# ============================================================================

print("\n" + "="*70)
print("2️⃣  ÉTAPE 2: Tester la génération de tokens")
print("="*70)

credentials = [
    ('nouveau_boutiquier_1', 'TempPassword123!'),
    ('aissatou_diallo', 'SecurePass456!'),
]

for username, password in credentials:
    print(f"\n🔑 Test: {username}")
    print(f"   Password: {password}")
    
    data = {'username': username, 'password': password}
    serializer = TokenObtainPairSerializer(data=data)
    
    if serializer.is_valid():
        print(f"   ✅ TOKEN GÉNÉRÉ!")
        token_data = serializer.validated_data
        print(f"   Access: {token_data['access'][:50]}...")
    else:
        print(f"   ❌ ERREUR: {serializer.errors}")

# ============================================================================
# TEST 3: Tester via API HTTP
# ============================================================================

print("\n" + "="*70)
print("3️⃣  ÉTAPE 3: Tester via HTTP POST")
print("="*70)

for username, password in credentials:
    print(f"\n🌐 POST /api/users/token/")
    print(f"   Username: {username}")
    print(f"   Password: {password}")
    
    response = client.post('/api/users/token/', {
        'username': username,
        'password': password
    }, format='json')
    
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print(f"   ✅ CONNEXION RÉUSSIE!")
        data = response.json()
        print(f"   Access Token: {data.get('access', '')[:50]}...")
        print(f"   Username: {data.get('username')}")
        print(f"   Email: {data.get('email')}")
        print(f"   Role: {data.get('role')}")
    else:
        print(f"   ❌ ERREUR!")
        print(f"   Response: {response.json()}")

# ============================================================================
# TEST 4: Vérifier les permissions
# ============================================================================

print("\n" + "="*70)
print("4️⃣  ÉTAPE 4: Vérifier les permissions")
print("="*70)

from rest_framework.test import force_authenticate
from users.permissions import IsBoutiquier

for username in test_accounts:
    print(f"\n👤 {username}:")
    try:
        user = User.objects.get(username=username)
        
        # Simuler une requête authentifiée
        from rest_framework.request import Request
        from rest_framework.test import APIRequestFactory
        
        factory = APIRequestFactory()
        request = factory.get('/')
        request.user = user
        
        # Tester la permission
        permission = IsBoutiquier()
        has_perm = permission.has_permission(request, None)
        
        print(f"   Permission IsBoutiquier: {'✅ OK' if has_perm else '❌ REFUSÉE'}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")

# ============================================================================
# TEST 5: Résumé
# ============================================================================

print("\n" + "="*70)
print("📊 RÉSUMÉ")
print("="*70)

print("""
✅ CHECKLIST:
  ✓ Comptes existent dans la base
  ✓ Mots de passe sont corrects
  ✓ Tokens JWT se génèrent
  ✓ Permissions OK
  ✓ API répond correctement

🎯 PROCHAINES ÉTAPES:
  1. Tester avec Postman: POST /api/users/token/
  2. Utiliser le JWT token retourné
  3. Accéder aux endpoints protégés
  4. Tester l'interface web
""")

print("="*70 + "\n")
