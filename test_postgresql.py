#!/usr/bin/env python
"""
Test de connexion à PostgreSQL et vérification du JWT avec Django
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'samacahier.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

print("=" * 60)
print("🧪 TEST POSTGRESQL + JWT DJANGO")
print("=" * 60)

# Test 1: Connexion à la base
try:
    users = User.objects.all()
    print(f"\n✅ Connexion PostgreSQL OK - {users.count()} utilisateurs trouvés")
except Exception as e:
    print(f"\n❌ Erreur connexion PostgreSQL: {e}")
    exit(1)

# Test 2: Vérifier les boutiquiers
print("\n📊 BOUTIQUIERS DANS POSTGRESQL:")
boutiquiers = User.objects.filter(role='boutiquier', status='active')
for boutiquier in boutiquiers:
    print(f"  ✅ {boutiquier.username} ({boutiquier.email})")

# Test 3: Générer JWT pour chaque compte
print("\n🔐 GÉNÉRATION DE JWT:")
test_accounts = [
    ('admin', 'temp_admin_1'),
    ('mouhamed365@gmail.com', 'temp_mouhamed365@gmail.com_2'),
    ('pole45@gmail.com', 'temp_pole45@gmail.com_3'),
    ('boutiquier1@test.com', 'temp_boutiquier1@test.com_4'),
    ('MOMO@gmail.com', 'temp_MOMO@gmail.com_6'),
]

success = 0
failed = 0

for username, password in test_accounts:
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            print(f"✅ {username}")
            print(f"   Token: {str(refresh.access_token)[:50]}...")
            success += 1
        else:
            print(f"❌ {username} - Mot de passe incorrect")
            failed += 1
    except User.DoesNotExist:
        print(f"❌ {username} - Utilisateur non trouvé")
        failed += 1
    except Exception as e:
        print(f"❌ {username} - Erreur: {e}")
        failed += 1

print("\n" + "=" * 60)
print(f"📈 RÉSULTATS: {success} OK, {failed} ÉCHECS")
if failed == 0:
    print("✅ TOUS LES COMPTES FONCTIONNENT AVEC POSTGRESQL!")
print("=" * 60)
