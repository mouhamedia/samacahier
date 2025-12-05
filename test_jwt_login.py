#!/usr/bin/env python
"""
Test DIRECT: Connexion avec les boutiquiers créés via serializer
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'samacahier.settings')
django.setup()

from django.contrib.auth import get_user_model
from users.serializers import CustomTokenObtainPairSerializer
from rest_framework import serializers

User = get_user_model()

print("=" * 80)
print("🧪 TEST CONNEXION DIRECT - SERIALIZER JWT")
print("=" * 80)

test_accounts = [
    ('nouveau_boutiquier_1', 'TempPassword123!'),
    ('aissatou_diallo', 'SecurePass456!'),
    ('admin', 'temp_admin_1'),
]

for username, password in test_accounts:
    print(f"\n{'='*80}")
    print(f"🔑 {username}")
    print(f"{'='*80}")
    
    try:
        user = User.objects.get(username=username)
        print(f"✅ Utilisateur trouvé")
        print(f"   Email: {user.email}")
        print(f"   Role: {user.role}")
        print(f"   Status: {user.status}")
        
        # Test 1: Vérifier le mot de passe
        if not user.check_password(password):
            print(f"❌ Mot de passe INCORRECT")
            continue
        
        print(f"✅ Mot de passe correct")
        
        # Test 2: Créer le serializer
        data = {
            'username': username,
            'password': password
        }
        
        serializer = CustomTokenObtainPairSerializer(data=data)
        
        if serializer.is_valid():
            tokens = serializer.validated_data
            print(f"✅ CONNEXION RÉUSSIE!")
            print(f"   Access: {str(tokens['access'])[:50]}...")
            print(f"   Refresh: {str(tokens.get('refresh', ''))[:50]}...")
            
            # Décoder le token pour voir les infos
            from jwt import decode
            import jwt as pyjwt
            
            try:
                decoded = pyjwt.decode(str(tokens['access']), options={"verify_signature": False})
                print(f"   Claims: username={decoded.get('username')}, role={decoded.get('role')}, email={decoded.get('email')}")
            except:
                pass
                
        else:
            print(f"❌ Erreur validation:")
            for error in serializer.errors:
                print(f"   {error}: {serializer.errors[error]}")
                
    except User.DoesNotExist:
        print(f"❌ Utilisateur NON TROUVÉ")
    except Exception as e:
        print(f"❌ Erreur: {e}")

print("\n" + "=" * 80)
print("✅ TEST TERMINÉ")
print("=" * 80)
