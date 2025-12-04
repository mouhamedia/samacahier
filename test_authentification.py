#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de diagnostic pour tester l'authentification
"""

import os
import sys
import io

# Forcer UTF-8 pour Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'samacahier.settings')

import django
django.setup()

from django.contrib.auth import authenticate
from users.models import CustomUser

print("\n" + "=" * 70)
print("🔐 DIAGNOSTIC D'AUTHENTIFICATION")
print("=" * 70 + "\n")

# 1. Vérifier les comptes créés
users = CustomUser.objects.filter(role='boutiquier')
print(f"📊 Nombre de boutiquiers: {users.count()}\n")

if not users.exists():
    print("❌ Aucun boutiquier trouvé!")
    sys.exit(1)

# 2. Afficher les comptes
print("📋 COMPTES BOUTIQUIERS:")
print("-" * 70)
for i, u in enumerate(users, 1):
    print(f"\n[{i}] {u.username}")
    print(f"    Email: {u.email}")
    print(f"    Status: {u.status}")
    print(f"    is_active: {u.is_active}")
    print(f"    is_staff: {u.is_staff}")
    print(f"    Password hash: {u.password[:30]}...")

# 3. Tester l'authentification
print("\n\n🔑 TEST D'AUTHENTIFICATION:")
print("-" * 70)

success = False
for u in users:
    pwd = f"temp_{u.username}_{u.id}"
    result = authenticate(username=u.username, password=pwd)
    status = "✅ OK" if result else "❌ ÉCHOUÉ"
    print(f"\n{status} {u.username}")
    print(f"    Mot de passe testé: {pwd}")
    if result:
        success = True

if not success:
    print("\n\n⚠️  AUCUNE AUTHENTIFICATION RÉUSSIE!")
    print("\nVérification des données:")
    for u in users:
        has_password = bool(u.password)
        print(f"  • {u.username}: password={has_password}")

print("\n" + "=" * 70)
