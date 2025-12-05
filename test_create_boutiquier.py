#!/usr/bin/env python3
"""
Test: Créer un nouveau boutquiers via l'admin
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'samacahier.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import string
import secrets

User = get_user_model()

print("\n" + "="*70)
print("🧪 TEST: CRÉATION D'UN NOUVEAU BOUTQUIER PAR L'ADMIN")
print("="*70)

# ============================================================================
# ÉTAPE 1: Vérifier que l'admin existe
# ============================================================================

print("\n1️⃣ ÉTAPE 1: VÉRIFIER L'ADMIN")
print("-" * 70)

try:
    admin = User.objects.get(username='admin')
    print(f"✅ Admin trouvé")
    print(f"   Username: {admin.username}")
    print(f"   Is Superuser: {admin.is_superuser}")
    print(f"   Role: {admin.role}")
except User.DoesNotExist:
    print(f"❌ Admin non trouvé")
    sys.exit(1)

# ============================================================================
# ÉTAPE 2: Générer un mot de passe temporaire
# ============================================================================

print("\n2️⃣ ÉTAPE 2: GÉNÉRER MOT DE PASSE TEMPORAIRE")
print("-" * 70)

def generate_temp_password():
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(12))

temp_password = generate_temp_password()
print(f"✅ Mot de passe généré: {temp_password}")

# ============================================================================
# ÉTAPE 3: Créer le nouveau boutquier
# ============================================================================

print("\n3️⃣ ÉTAPE 3: CRÉER LE NOUVEAU BOUTQUIER")
print("-" * 70)

new_username = f"test_boutquier_{secrets.token_hex(3)}"
new_email = f"test.boutquier.{secrets.token_hex(2)}@example.com"

print(f"📝 Création de:")
print(f"   Username: {new_username}")
print(f"   Email: {new_email}")
print(f"   Password: {temp_password}")

try:
    new_boutiquier = User.objects.create_user(
        username=new_username,
        email=new_email,
        password=temp_password,
        first_name="Test",
        last_name="Boutquier",
        phone="+221770123456",
        role='boutiquier',
        status='active',
        is_active=True
    )
    print(f"\n✅ BOUTIQUIER CRÉÉ!")
    print(f"   ID: {new_boutiquier.id}")
    print(f"   Username: {new_boutiquier.username}")
    print(f"   Email: {new_boutiquier.email}")
    print(f"   Role: {new_boutiquier.role}")
    print(f"   Status: {new_boutiquier.status}")
    print(f"   Is Active: {new_boutiquier.is_active}")
except Exception as e:
    print(f"❌ ERREUR: {e}")
    sys.exit(1)

# ============================================================================
# ÉTAPE 4: Vérifier que le mot de passe est correct
# ============================================================================

print("\n4️⃣ ÉTAPE 4: VÉRIFIER LE MOT DE PASSE")
print("-" * 70)

if new_boutiquier.check_password(temp_password):
    print(f"✅ Mot de passe correct!")
else:
    print(f"❌ Mot de passe INCORRECT!")
    sys.exit(1)

# ============================================================================
# ÉTAPE 5: Tester l'authentification Django
# ============================================================================

print("\n5️⃣ ÉTAPE 5: TESTER authenticate()")
print("-" * 70)

authenticated_user = authenticate(username=new_username, password=temp_password)
if authenticated_user:
    print(f"✅ authenticate() OK")
    print(f"   User: {authenticated_user.username}")
    print(f"   Role: {authenticated_user.role}")
else:
    print(f"❌ authenticate() ÉCHOUÉ")
    sys.exit(1)

# ============================================================================
# ÉTAPE 6: Générer un JWT token
# ============================================================================

print("\n6️⃣ ÉTAPE 6: GÉNÉRER JWT TOKEN")
print("-" * 70)

try:
    refresh = RefreshToken.for_user(new_boutiquier)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)
    
    print(f"✅ JWT TOKENS GÉNÉRÉS!")
    print(f"   Access: {access_token[:50]}...")
    print(f"   Refresh: {refresh_token[:50]}...")
except Exception as e:
    print(f"❌ ERREUR: {e}")
    sys.exit(1)

# ============================================================================
# RÉSUMÉ
# ============================================================================

print("\n" + "="*70)
print("✅ RÉSUMÉ - CRÉATION RÉUSSIE!")
print("="*70)

print(f"""
🎯 NOUVEAU BOUTQUIER CRÉÉ AVEC SUCCÈS!

Identifiants:
- Username: {new_username}
- Password: {temp_password}
- Email: {new_email}

Configuration:
- Role: boutiquier
- Status: active
- Is Active: True

Tests Passés:
✅ Créé en base de données
✅ Mot de passe correct
✅ Django authenticate() OK
✅ JWT Token généré

🚀 CE BOUTQUIER PEUT MAINTENANT SE CONNECTER!
""")

print("="*70 + "\n")
