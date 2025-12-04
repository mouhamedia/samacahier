#!/usr/bin/env python
"""
Script de démarrage stable du serveur Django
Désactive le reloadeur pour éviter les redémarrages
"""

import os
import sys
import subprocess

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'samacahier.settings')

# Démarrer le serveur sans reloadeur
cmd = [sys.executable, 'manage.py', 'runserver', '--nothreading', '--noreload', '127.0.0.1:8000']

print("\n" + "=" * 70)
print("🚀 Démarrage du serveur Django (mode stable)")
print("=" * 70)
print(f"\nCommande: {' '.join(cmd)}")
print("\n📍 Accès: http://localhost:8000/frontend/")
print("⏹️  Arrêt: Ctrl+C")
print("\n" + "=" * 70 + "\n")

subprocess.run(cmd)
