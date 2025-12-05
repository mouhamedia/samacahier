#!/usr/bin/env python
"""
Test: Connexion API directe avec les boutiquiers créés
"""
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'samacahier.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client as TestClient
from django.urls import reverse

User = get_user_model()

print("=" * 80)
print("🧪 TEST CONNEXION API - BOUTIQUIERS CRÉÉS")
print("=" * 80)

# Les boutiquiers créés
test_accounts = [
    ('nouveau_boutiquier_1', 'TempPassword123!'),
    ('aissatou_diallo', 'SecurePass456!'),
    ('admin', 'temp_admin_1'),  # Référence
]

client = TestClient()

for username, password in test_accounts:
    print(f"\n{'='*80}")
    print(f"🔑 Test: {username}")
    print(f"{'='*80}")
    
    try:
        # Vérifier que l'utilisateur existe
        user = User.objects.get(username=username)
        print(f"✅ Utilisateur trouvé")
        print(f"   Role: {user.role}")
        print(f"   Status: {user.status}")
        print(f"   Is Active: {user.is_active}")
        print(f"   Mot de passe correct: {user.check_password(password)}")
        
        # Tester la connexion via l'API
        print(f"\n📱 Test connexion API...")
        response = client.post(
            'http://localhost:8000/api/users/token/',
            data=json.dumps({
                'username': username,
                'password': password
            }),
            content_type='application/json'
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ CONNEXION RÉUSSIE!")
            print(f"   Access Token: {data.get('access', '')[:50]}...")
            print(f"   Role: {data.get('role')}")
            print(f"   Email: {data.get('email')}")
        else:
            print(f"   ❌ ERREUR {response.status_code}")
            print(f"   Response: {response.json()}")
            
    except User.DoesNotExist:
        print(f"❌ Utilisateur NON TROUVÉ")
    except Exception as e:
        print(f"❌ Erreur: {e}")

print("\n" + "=" * 80)
print("✅ TEST TERMINÉ")
print("=" * 80)
