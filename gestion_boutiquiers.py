#!/usr/bin/env python
"""
Gestionnaire complet de boutiquiers - CLI
Pas besoin du serveur web !
"""

import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'samacahier.settings')
import django
django.setup()

from users.models import CustomUser
from django.contrib.auth import authenticate

def menu():
    print("\n" + "=" * 70)
    print("👨‍💼 GESTIONNAIRE DE BOUTIQUIERS")
    print("=" * 70)
    print("\n1️⃣  Créer un nouvel utilisateur")
    print("2️⃣  Lister tous les utilisateurs")
    print("3️⃣  Tester une connexion")
    print("4️⃣  Réinitialiser mot de passe")
    print("5️⃣  Supprimer un utilisateur")
    print("0️⃣  Quitter")
    print("\n" + "-" * 70)
    return input("\n➡️  Choix (0-5): ").strip()

def create_user():
    print("\n📝 CRÉER UN NOUVEL UTILISATEUR")
    print("-" * 70)
    
    email = input("\n📧 Email/Utilisateur: ").strip()
    
    if not email:
        print("❌ Email requis!")
        return
    
    if CustomUser.objects.filter(username=email).exists():
        print(f"❌ L'utilisateur '{email}' existe déjà!")
        return
    
    password = input("🔑 Mot de passe (min 8 caractères): ").strip()
    
    if len(password) < 8:
        print("❌ Mot de passe trop court!")
        return
    
    first_name = input("👤 Prénom (optionnel): ").strip() or "Boutiquier"
    
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
        
        print("\n✅ UTILISATEUR CRÉÉ!")
        print(f"   ID: {user.id}")
        print(f"   Email: {user.username}")
        print(f"   Nom: {user.first_name}")
        print(f"   Rôle: {user.role}")
        print(f"   Statut: {user.status}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

def list_users():
    print("\n📋 LISTE DE TOUS LES UTILISATEURS")
    print("-" * 70)
    
    users = CustomUser.objects.all().order_by('username')
    
    if not users:
        print("Aucun utilisateur trouvé!")
        return
    
    print(f"\n{'ID':<4} {'Email':<30} {'Rôle':<12} {'Statut':<10} {'Actif':<6}")
    print("-" * 70)
    
    for user in users:
        print(f"{user.id:<4} {user.username:<30} {user.role:<12} {user.status:<10} {'✅' if user.is_active else '❌':<6}")

def test_login():
    print("\n🔐 TESTER UNE CONNEXION")
    print("-" * 70)
    
    email = input("\n📧 Email: ").strip()
    password = input("🔑 Mot de passe: ").strip()
    
    user = authenticate(username=email, password=password)
    
    if user:
        print(f"\n✅ CONNEXION RÉUSSIE!")
        print(f"   Email: {user.username}")
        print(f"   Nom: {user.first_name}")
        print(f"   Rôle: {user.role}")
        print(f"   Statut: {user.status}")
    else:
        print("\n❌ Identifiants incorrects!")

def reset_password():
    print("\n🔑 RÉINITIALISER UN MOT DE PASSE")
    print("-" * 70)
    
    email = input("\n📧 Email de l'utilisateur: ").strip()
    
    try:
        user = CustomUser.objects.get(username=email)
    except CustomUser.DoesNotExist:
        print(f"❌ Utilisateur '{email}' non trouvé!")
        return
    
    password = input("🔑 Nouveau mot de passe (min 8 caractères): ").strip()
    
    if len(password) < 8:
        print("❌ Mot de passe trop court!")
        return
    
    user.set_password(password)
    user.save()
    
    print(f"\n✅ MOT DE PASSE RÉINITIALISÉ!")
    print(f"   Email: {user.username}")
    print(f"   Nouveau mot de passe: {password}")

def delete_user():
    print("\n🗑️  SUPPRIMER UN UTILISATEUR")
    print("-" * 70)
    
    email = input("\n📧 Email de l'utilisateur: ").strip()
    
    try:
        user = CustomUser.objects.get(username=email)
    except CustomUser.DoesNotExist:
        print(f"❌ Utilisateur '{email}' non trouvé!")
        return
    
    confirm = input(f"\n⚠️  Êtes-vous sûr de vouloir supprimer '{email}'? (oui/non): ").strip().lower()
    
    if confirm == 'oui':
        user.delete()
        print(f"\n✅ UTILISATEUR SUPPRIMÉ!")
    else:
        print("❌ Suppression annulée!")

if __name__ == '__main__':
    while True:
        choice = menu()
        
        if choice == '1':
            create_user()
        elif choice == '2':
            list_users()
        elif choice == '3':
            test_login()
        elif choice == '4':
            reset_password()
        elif choice == '5':
            delete_user()
        elif choice == '0':
            print("\n👋 Au revoir!\n")
            sys.exit(0)
        else:
            print("\n❌ Choix invalide!")
        
        input("\n➡️  Appuyez sur Entrée pour continuer...")
