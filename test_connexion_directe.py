#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test de connexion direct - sans serveur web
Teste la base de données directement
"""

import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'samacahier.settings')

import django
django.setup()

from django.contrib.auth import authenticate
from users.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

print("\n" + "=" * 80)
print("TEST DIRECT DE CONNEXION - BOUTIQUIERS")
print("=" * 80 + "\n")

# Comptes à tester
credentials = [
    ("admin", "temp_admin_1"),
    ("mouhamed365@gmail.com", "temp_mouhamed365@gmail.com_2"),
    ("pole45@gmail.com", "temp_pole45@gmail.com_3"),
    ("boutiquier1@test.com", "temp_boutiquier1@test.com_4"),
    ("MOMO@gmail.com", "temp_MOMO@gmail.com_6"),
]

print(f"Nombre de comptes à tester: {len(credentials)}\n")

success_count = 0
failed_count = 0

for username, password in credentials:
    print(f"Test: {username}")
    
    try:
        # Tester l'authentification Django
        user = authenticate(username=username, password=password)
        
        if user:
            # Si authentification OK, générer un JWT token
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            print(f"  Status: OK")
            print(f"  Role: {user.role}")
            print(f"  Email: {user.email}")
            print(f"  Token: {access_token[:40]}...")
            success_count += 1
        else:
            print(f"  Status: ECHEC - Mauvais identifiants")
            failed_count += 1
            
    except Exception as e:
        print(f"  Status: ERREUR - {e}")
        failed_count += 1
    
    print()

print("=" * 80)
print(f"Résultats: {success_count} OK, {failed_count} ECHEC")
print("=" * 80 + "\n")

if success_count == len(credentials):
    print("✅ TOUS LES COMPTES FONCTIONNENT!")
    print("\nLes boutiquiers peuvent maintenant se connecter sur l'app.")
    print("Utilisez Postman pour tester via HTTP:")
    print("  POST http://localhost:8000/api/users/token/")
else:
    print(f"⚠️  {failed_count} compte(s) n'a/ont pas pu se connecter")
    print("Vérifiez les mots de passe dans credentials_boutiquiers.txt")

print()
