#!/usr/bin/env python
"""
Script simple pour créer des boutiquiers
Usage: python create_boutiquier_simple.py
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'samacahier.settings')

import django
django.setup()

from users.models import CustomUser

print("\n" + "=" * 70)
print("➕ CRÉER UN NOUVEL UTILISATEUR BOUTIQUIER")
print("=" * 70 + "\n")

# Demander l'email
email = input("📧 Email (ex: boutiquier@example.com): ").strip()

# Vérifier si l'email existe déjà
if CustomUser.objects.filter(username=email).exists():
    print(f"❌ Erreur: L'utilisateur '{email}' existe déjà!\n")
    exit(1)

# Demander le mot de passe
password = input("🔑 Mot de passe: ").strip()

if len(password) < 8:
    print("❌ Erreur: Le mot de passe doit avoir au moins 8 caractères!\n")
    exit(1)

# Demander le prénom (optionnel)
first_name = input("👤 Prénom (optionnel): ").strip() or "Boutiquier"

# Créer l'utilisateur
try:
    user = CustomUser.objects.create_user(
        username=email,
        email=email,
        password=password,
        first_name=first_name,
        role='boutiquier',
        status='active',
        is_active=True
    )
    
    print("\n" + "=" * 70)
    print("✅ BOUTIQUIER CRÉÉ AVEC SUCCÈS!")
    print("=" * 70)
    print(f"\n📊 Détails du nouvel utilisateur:")
    print(f"   • ID: {user.id}")
    print(f"   • Email/Utilisateur: {user.username}")
    print(f"   • Nom: {user.first_name}")
    print(f"   • Rôle: {user.role}")
    print(f"   • Statut: {user.status}")
    print(f"   • Actif: {'Oui' if user.is_active else 'Non'}")
    print(f"\n🔗 URL de connexion: http://localhost:8000/frontend/")
    print(f"   Identifiants: {user.username} / {password}\n")
    
except Exception as e:
    print(f"\n❌ Erreur: {e}\n")
    exit(1)
