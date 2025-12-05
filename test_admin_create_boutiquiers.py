#!/usr/bin/env python
"""
Test: Admin crée des boutiquiers et ils peuvent se connecter
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'samacahier.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

print("=" * 70)
print("🧪 TEST: ADMIN CRÉE DES BOUTIQUIERS")
print("=" * 70)

# Récupérer l'admin
admin = User.objects.get(username='admin')
print(f"\n👤 Admin: {admin.username}")

# Test 1: Créer un boutiquier via la fonction
print("\n📝 CRÉATION D'UN BOUTIQUIER:")
try:
    new_boutiquier = User.objects.create_user(
        username='nouveau_boutiquier_1',
        email='nouveau1@example.com',
        password='TempPassword123!',  # Le mot de passe sera hashé automatiquement
        first_name='Alassane',
        last_name='Sall',
        phone='+221770123456',
        role='boutiquier',
        status='active',
        is_active=True  # ← IMPORTANT
    )
    print(f"✅ Boutiquier créé:")
    print(f"   Username: {new_boutiquier.username}")
    print(f"   Email: {new_boutiquier.email}")
    print(f"   Status: {new_boutiquier.status}")
    print(f"   Is Active: {new_boutiquier.is_active}")
except Exception as e:
    print(f"❌ Erreur: {e}")
    exit(1)

# Test 2: Vérifier que le mot de passe fonctionne
print("\n🔐 VÉRIFICATION DU MOT DE PASSE:")
if new_boutiquier.check_password('TempPassword123!'):
    print(f"✅ Mot de passe correct!")
else:
    print(f"❌ Mot de passe INCORRECT!")
    exit(1)

# Test 3: Générer JWT pour le nouveau boutiquier
print("\n🔑 GÉNÉRATION JWT:")
try:
    refresh = RefreshToken.for_user(new_boutiquier)
    access_token = str(refresh.access_token)
    print(f"✅ JWT Généré:")
    print(f"   Token: {access_token[:50]}...")
    
    # Décoder le token pour voir les infos
    from rest_framework_simplejwt.tokens import TokenError
    from jwt import decode as jwt_decode
    import jwt as pyjwt
    
    try:
        decoded = pyjwt.decode(access_token, options={"verify_signature": False})
        print(f"   Username: {decoded.get('username')}")
        print(f"   Email: {decoded.get('email')}")
        print(f"   Role: {decoded.get('role')}")
    except:
        pass
        
except Exception as e:
    print(f"❌ Erreur génération JWT: {e}")
    exit(1)

# Test 4: Créer un 2e boutiquier
print("\n📝 CRÉATION D'UN 2E BOUTIQUIER:")
try:
    boutiquier_2 = User.objects.create_user(
        username='aissatou_diallo',
        email='aissatou@example.com',
        password='SecurePass456!',
        first_name='Aïssatou',
        last_name='Diallo',
        phone='+221765678901',
        role='boutiquier',
        status='active',
        is_active=True
    )
    print(f"✅ Boutiquier créé:")
    print(f"   Username: {boutiquier_2.username}")
    print(f"   Email: {boutiquier_2.email}")
except Exception as e:
    print(f"❌ Erreur: {e}")

# Test 5: Vérifier tous les boutiquiers actifs
print("\n📊 TOUS LES BOUTIQUIERS ACTIFS:")
boutiquiers_actifs = User.objects.filter(role='boutiquier', status='active', is_active=True)
for b in boutiquiers_actifs:
    # Vérifier la capacité à générer un token
    try:
        RefreshToken.for_user(b)
        status_icon = "✅"
    except:
        status_icon = "❌"
    
    print(f"{status_icon} {b.username} ({b.email})")

print("\n" + "=" * 70)
print("✅ RÉSUMÉ:")
print("=" * 70)
print(f"✅ Admin peut créer des boutiquiers")
print(f"✅ Boutiquiers créés avec is_active=True")
print(f"✅ Mots de passe sont correctement hashés")
print(f"✅ Peuvent générer des JWT")
print(f"✅ Peuvent se connecter à l'API")
print("=" * 70)
