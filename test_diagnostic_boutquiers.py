#!/usr/bin/env python3
"""
DIAGNOSTIC DÉTAILLÉ - Problème de connexion des boutquiers
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'samacahier.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

print("\n" + "="*70)
print("🔍 DIAGNOSTIC DÉTAILLÉ - PROBLÈME DE CONNEXION")
print("="*70)

# ============================================================================
# TEST 1: Vérifier que les comptes existent
# ============================================================================

print("\n1️⃣ ÉTAPE 1: COMPTES EXISTENT DANS LA BASE?")
print("-" * 70)

test_users = [
    ('nouveau_boutiquier_1', 'TempPassword123!'),
    ('aissatou_diallo', 'SecurePass456!'),
]

for username, password in test_users:
    try:
        user = User.objects.get(username=username)
        print(f"\n✅ {username} EXISTS")
        print(f"   Email: {user.email}")
        print(f"   Role: {user.role}")
        print(f"   Status: {user.status}")
        print(f"   Is Active: {user.is_active}")
        print(f"   Has password: {user.has_usable_password()}")
    except User.DoesNotExist:
        print(f"\n❌ {username} NOT FOUND")

# ============================================================================
# TEST 2: Authenticate avec Django
# ============================================================================

print("\n2️⃣ ÉTAPE 2: TESTER authenticate() DE DJANGO")
print("-" * 70)

for username, password in test_users:
    print(f"\nTest: {username} / {password}")
    user = authenticate(username=username, password=password)
    if user:
        print(f"   ✅ AUTHENTIFICATION OK")
        print(f"   User ID: {user.id}")
        print(f"   User Role: {user.role}")
    else:
        print(f"   ❌ AUTHENTIFICATION ÉCHOUÉE")

# ============================================================================
# TEST 3: Test du sérializer TokenObtainPairSerializer
# ============================================================================

print("\n3️⃣ ÉTAPE 3: TESTER TokenObtainPairSerializer")
print("-" * 70)

for username, password in test_users:
    print(f"\nTest: {username} / {password}")
    data = {'username': username, 'password': password}
    serializer = TokenObtainPairSerializer(data=data)
    
    if serializer.is_valid():
        print(f"   ✅ SÉRIALIZER VALID")
        tokens = serializer.validated_data
        access_token = tokens.get('access', 'N/A')
        print(f"   Access: {access_token[:50]}...")
    else:
        print(f"   ❌ SÉRIALIZER ERRORS")
        for key, errors in serializer.errors.items():
            print(f"   - {key}: {errors}")

# ============================================================================
# TEST 4: Vérifier CustomTokenObtainPairSerializer
# ============================================================================

print("\n4️⃣ ÉTAPE 4: TESTER CustomTokenObtainPairSerializer")
print("-" * 70)

try:
    from users.serializers import CustomTokenObtainPairSerializer
    
    for username, password in test_users:
        print(f"\nTest: {username} / {password}")
        data = {'username': username, 'password': password}
        serializer = CustomTokenObtainPairSerializer(data=data)
        
        if serializer.is_valid():
            print(f"   ✅ CUSTOM SÉRIALIZER VALID")
            tokens = serializer.validated_data
            print(f"   Username: {tokens.get('username')}")
            print(f"   Email: {tokens.get('email')}")
            print(f"   Role: {tokens.get('role')}")
            access = tokens.get('access', 'N/A')
            print(f"   Access: {access[:50]}...")
        else:
            print(f"   ❌ CUSTOM SÉRIALIZER ERRORS")
            for key, errors in serializer.errors.items():
                print(f"   - {key}: {errors}")
except ImportError as e:
    print(f"❌ Erreur import: {e}")

# ============================================================================
# TEST 5: Vérifier les permissions
# ============================================================================

print("\n5️⃣ ÉTAPE 5: VÉRIFIER LES PERMISSIONS")
print("-" * 70)

from users.permissions import IsBoutiquier
from rest_framework.test import APIRequestFactory

factory = APIRequestFactory()

for username, password in test_users:
    print(f"\n{username}:")
    user = User.objects.get(username=username)
    
    request = factory.get('/')
    request.user = user
    
    permission = IsBoutiquier()
    has_perm = permission.has_permission(request, None)
    
    print(f"   Permission IsBoutiquier: {'✅ OK' if has_perm else '❌ REFUSÉE'}")

# ============================================================================
# RÉSUMÉ
# ============================================================================

print("\n" + "="*70)
print("📊 RÉSUMÉ FINAL")
print("="*70)

print("""
✅ SI TOUS LES TESTS PASSENT:
   - Les comptes existent ✓
   - Les mots de passe sont corrects ✓
   - Les tokens se génèrent ✓
   - Les permissions OK ✓
   
   → Le problème vient de l'API HTTP
   → Vérifiez les configurations REST Framework
   → Testez avec Postman directement

❌ SI UN TEST ÉCHOUE:
   - Identifiez quel test échoue
   - Vérifiez la configuration
   - Corrigez le problème spécifique
""")

print("="*70 + "\n")
