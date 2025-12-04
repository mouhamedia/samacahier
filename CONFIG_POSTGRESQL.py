#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de configuration PostgreSQL
Convertit la base SQLite en PostgreSQL
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'samacahier.settings')
django.setup()

print("\n" + "=" * 70)
print("CONFIGURATION PostgreSQL")
print("=" * 70 + "\n")

print("ÉTAPES POUR CONFIGURER PostgreSQL:\n")

print("1️⃣  INSTALLER PostgreSQL")
print("   Windows: Télécharger https://www.postgresql.org/download/windows/")
print("   Créer une base: samacahier")
print("   User: postgres")
print("   Password: [votre mot de passe]\n")

print("2️⃣  INSTALLER LE DRIVER PYTHON")
print("   pip install psycopg2-binary\n")

print("3️⃣  MODIFIER config/env.py")
print("   Remplacer DATABASE par:")
print("""
DATABASE = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'samacahier',
    'USER': 'postgres',
    'PASSWORD': 'votre_mot_de_passe',
    'HOST': 'localhost',
    'PORT': '5432',
}
""")

print("4️⃣  MIGRER LES DONNÉES")
print("   python manage.py migrate\n")

print("5️⃣  CRÉER LES COMPTES")
print("   python reset_boutiquier_passwords.py\n")

print("=" * 70)
print("Configuration Complète!")
print("=" * 70 + "\n")
