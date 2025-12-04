#!/usr/bin/env python
"""
Script pour réinitialiser les mots de passe des boutiquiers
Exécutez avec: python reset_boutiquier_passwords.py
"""

import os
import sys

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'samacahier.settings')

import django
django.setup()

from users.models import CustomUser

print("\n" + "=" * 70)
print("🔑  RÉINITIALISATION DES MOTS DE PASSE BOUTIQUIERS")
print("=" * 70 + "\n")

# Récupérer tous les boutiquiers
boutiquiers = CustomUser.objects.filter(role='boutiquier').order_by('username')

if not boutiquiers.exists():
    print("❌ Aucun boutiquier trouvé!\n")
    sys.exit(1)

print(f"📊 Nombre de boutiquiers trouvés: {boutiquiers.count()}\n")

credentials = []
success_count = 0

for i, boutiquier in enumerate(boutiquiers, 1):
    try:
        # Générer un mot de passe temporaire simple
        temp_password = f"temp_{boutiquier.username}_{boutiquier.id}"
        
        # Définir le mot de passe
        boutiquier.set_password(temp_password)
        boutiquier.save()
        
        credentials.append({
            'username': boutiquier.username,
            'email': boutiquier.email,
            'password': temp_password,
            'first_name': boutiquier.first_name or 'N/A'
        })
        
        print(f"✅ [{i}] {boutiquier.username}")
        print(f"    Email: {boutiquier.email}")
        print(f"    Mot de passe: {temp_password}")
        print(f"    Statut: {boutiquier.status}\n")
        success_count += 1
        
    except Exception as e:
        print(f"❌ [{i}] Erreur avec {boutiquier.username}: {e}\n")

# Sauvegarder les identifiants
try:
    with open('credentials_boutiquiers.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("IDENTIFIANTS TEMPORAIRES DES BOUTIQUIERS\n")
        f.write("=" * 70 + "\n\n")
        f.write("⚠️  CONFIDENTIEL - À NE PAS PARTAGER PUBLIQUEMENT\n\n")
        
        for cred in credentials:
            f.write(f"Nom: {cred['first_name']}\n")
            f.write(f"Utilisateur: {cred['username']}\n")
            f.write(f"Email: {cred['email']}\n")
            f.write(f"Mot de passe temporaire: {cred['password']}\n")
            f.write(f"URL de connexion: http://localhost:8000/frontend/\n")
            f.write("-" * 70 + "\n\n")
    
    print("=" * 70)
    print(f"✅ {success_count} boutiquier(s) réinitialisé(s) avec succès!")
    print("=" * 70)
    print(f"\n📁 Identifiants sauvegardés dans: credentials_boutiquiers.txt")
    print("\n💡 PROCHAINES ÉTAPES:")
    print("   1. Démarrer le serveur: python manage.py runserver")
    print("   2. Aller à: http://localhost:8000/frontend/")
    print("   3. Se connecter avec les identifiants ci-dessus")
    print("   4. Changer le mot de passe après connexion\n")
    
except Exception as e:
    print(f"\n❌ Erreur lors de la sauvegarde: {e}\n")
