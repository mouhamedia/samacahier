#!/usr/bin/env python
"""
Diagnostic: Pourquoi les boutiquiers créés ne peuvent pas se connecter?
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'samacahier.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

print("=" * 80)
print("🔍 DIAGNOSTIC: PROBLÈME DE CONNEXION BOUTIQUIERS")
print("=" * 80)

# Test 1: Lister tous les boutiquiers
print("\n1️⃣ TOUS LES BOUTIQUIERS:")
boutiquiers = User.objects.filter(role='boutiquier')
print(f"Total: {boutiquiers.count()}\n")

for b in boutiquiers:
    print(f"👤 {b.username:<30} | Status: {b.status:<8} | Active: {b.is_active} | Staff: {b.is_staff}")

# Test 2: Détails des boutiquiers créés
print("\n" + "=" * 80)
print("2️⃣ DÉTAILS DES BOUTIQUIERS CRÉÉS PAR ADMIN:")
print("=" * 80)

created_boutiquiers = [
    ('nouveau_boutiquier_1', 'TempPassword123!'),
    ('aissatou_diallo', 'SecurePass456!'),
]

for username, password in created_boutiquiers:
    try:
        user = User.objects.get(username=username)
        
        print(f"\n👤 {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Role: {user.role}")
        print(f"   Status: {user.status}")
        print(f"   Is Active: {user.is_active}")
        print(f"   Is Staff: {user.is_staff}")
        print(f"   Is Superuser: {user.is_superuser}")
        
        # Vérifier le mot de passe
        pwd_check = user.check_password(password)
        print(f"   Mot de passe correct: {pwd_check} ({password})")
        
        # Essayer de générer un JWT
        try:
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)
            print(f"   ✅ JWT Token généré: {access[:50]}...")
        except Exception as e:
            print(f"   ❌ Erreur JWT: {e}")
            
    except User.DoesNotExist:
        print(f"\n❌ {username} - NON TROUVÉ")

# Test 3: Tenter la connexion API
print("\n" + "=" * 80)
print("3️⃣ TEST DE CONNEXION API:")
print("=" * 80)

for username, password in created_boutiquiers:
    try:
        user = User.objects.get(username=username)
        
        # Vérifier les pré-requis pour la connexion
        checks = {
            'Utilisateur existe': user is not None,
            'Rôle = boutiquier': user.role == 'boutiquier',
            'Status = active': user.status == 'active',
            'Is_active = True': user.is_active == True,
            'Mot de passe correct': user.check_password(password),
        }
        
        print(f"\n{username}:")
        all_pass = True
        for check_name, result in checks.items():
            icon = "✅" if result else "❌"
            print(f"   {icon} {check_name}")
            if not result:
                all_pass = False
        
        if all_pass:
            print(f"   🎉 DEVRAIT POUVOIR SE CONNECTER!")
        else:
            print(f"   ⚠️ PROBLÈME DÉTECTÉ")
            
    except User.DoesNotExist:
        print(f"\n❌ {username} - NON TROUVÉ")

# Test 4: Vérifier les permissions
print("\n" + "=" * 80)
print("4️⃣ VÉRIFICATIONS DE PERMISSIONS:")
print("=" * 80)

for username, _ in created_boutiquiers:
    try:
        user = User.objects.get(username=username)
        
        from users.permissions import IsBoutiquier
        perm = IsBoutiquier()
        
        # Créer un mock request
        class MockRequest:
            pass
        
        request = MockRequest()
        request.user = user
        
        # Vérifier la permission
        can_access = perm.has_permission(request, None)
        
        print(f"\n{username}:")
        print(f"   Permission IsBoutiquier: {can_access}")
        
    except Exception as e:
        print(f"   Erreur: {e}")

print("\n" + "=" * 80)
print("✅ DIAGNOSTIC TERMINÉ")
print("=" * 80)
