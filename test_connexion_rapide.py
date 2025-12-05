#!/usr/bin/env python3
"""
TEST RAPIDE - Vérifier que tous les boutquiers peuvent se connecter
Exécutez: python test_connexion_rapide.py
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'samacahier.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth import get_user_model
from users.serializers import CustomTokenObtainPairSerializer

User = get_user_model()

# ============================================================================
# TEST DATA
# ============================================================================

TEST_ACCOUNTS = [
    {
        'username': 'nouveau_boutiquier_1',
        'password': 'TempPassword123!',
        'type': 'Créé par admin'
    },
    {
        'username': 'aissatou_diallo',
        'password': 'SecurePass456!',
        'type': 'Créé par admin'
    },
    {
        'username': 'admin',
        'password': 'temp_admin_1',
        'type': 'Original'
    }
]

# ============================================================================
# FUNCTIONS
# ============================================================================

def test_account_login(username, password):
    """Teste si un compte peut se connecter"""
    try:
        user = User.objects.get(username=username)
        
        # Vérifier le mot de passe
        if not user.check_password(password):
            return False, "Mot de passe incorrect"
        
        # Générer le token
        data = {'username': username, 'password': password}
        serializer = CustomTokenObtainPairSerializer(data=data)
        
        if serializer.is_valid():
            token_data = serializer.validated_data
            return True, token_data
        else:
            return False, f"Erreur sérialisation: {serializer.errors}"
            
    except User.DoesNotExist:
        return False, "Utilisateur non trouvé"
    except Exception as e:
        return False, f"Erreur: {str(e)}"

def print_test_result(username, password, account_type, success, data):
    """Affiche les résultats du test"""
    
    print("\n" + "="*70)
    print(f"🔑 TEST: {username}")
    print("="*70)
    print(f"Type: {account_type}")
    print(f"Mot de passe: {password}")
    print()
    
    if success:
        print("✅ CONNEXION RÉUSSIE!")
        print()
        print(f"Access Token: {data.get('access', '')[:50]}...")
        print(f"Refresh Token: {data.get('refresh', '')[:50]}...")
        print(f"Username: {data.get('username')}")
        print(f"Email: {data.get('email')}")
        print(f"Role: {data.get('role')}")
        print()
        print("✅ Cet utilisateur peut se connecter!")
    else:
        print(f"❌ ERREUR: {data}")
        print()
        print("❌ Cet utilisateur NE peut pas se connecter")
    
    print()

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  TEST RAPIDE - CONNEXION DES BOUTQUIERS".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    passed = 0
    failed = 0
    
    for account in TEST_ACCOUNTS:
        username = account['username']
        password = account['password']
        account_type = account['type']
        
        success, data = test_account_login(username, password)
        print_test_result(username, password, account_type, success, data)
        
        if success:
            passed += 1
        else:
            failed += 1
    
    # Summary
    print("\n" + "="*70)
    print("📊 RÉSUMÉ")
    print("="*70)
    print(f"✅ Réussies: {passed}")
    print(f"❌ Échouées: {failed}")
    
    if failed == 0:
        print("\n🎉 TOUS LES TESTS RÉUSSIS!")
        print("✅ Tous les boutquiers peuvent se connecter!")
    else:
        print(f"\n⚠️  {failed} test(s) échoué(s)")
        print("❌ Vérifiez les identifiants")
    
    print("="*70 + "\n")
    
    return 0 if failed == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
