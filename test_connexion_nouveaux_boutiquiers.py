#!/usr/bin/env python
"""
Test: Se connecter avec les nouveaux boutiquiers
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'samacahier.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

print("=" * 70)
print("🔐 TEST DE CONNEXION: NOUVEAUX BOUTIQUIERS")
print("=" * 70)

# Les nouveaux boutiquiers créés
test_accounts = [
    ('nouveau_boutiquier_1', 'TempPassword123!'),
    ('aissatou_diallo', 'SecurePass456!'),
]

success = 0
failed = 0

for username, password in test_accounts:
    try:
        user = User.objects.get(username=username)
        
        # Vérifier le mot de passe
        if not user.check_password(password):
            print(f"❌ {username} - Mot de passe INCORRECT")
            failed += 1
            continue
        
        # Vérifier qu'il est actif
        if not user.is_active:
            print(f"❌ {username} - Compte INACTIF")
            failed += 1
            continue
        
        # Générer le JWT
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        print(f"✅ {username}")
        print(f"   Email: {user.email}")
        print(f"   Role: {user.role}")
        print(f"   Status: {user.status}")
        print(f"   Is Active: {user.is_active}")
        print(f"   Token: {access_token[:50]}...")
        print()
        
        success += 1
        
    except User.DoesNotExist:
        print(f"❌ {username} - Utilisateur NON TROUVÉ")
        failed += 1
    except Exception as e:
        print(f"❌ {username} - Erreur: {e}")
        failed += 1

print("=" * 70)
print(f"📈 RÉSULTATS: {success} OK, {failed} ÉCHECS")
if failed == 0:
    print("✅ TOUS LES NOUVEAUX BOUTIQUIERS PEUVENT SE CONNECTER!")
print("=" * 70)
