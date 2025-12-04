#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script simple pour démarrer le serveur et tester la connexion
"""

import os
import sys
import time
import threading
import requests
import json
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'samacahier.settings')

import django
django.setup()

from django.core.management import execute_from_command_line

def start_server():
    """Démarrer le serveur Django"""
    sys.argv = ['manage.py', 'runserver', '--nothreading', '--noreload', '127.0.0.1:8000']
    try:
        execute_from_command_line(sys.argv)
    except KeyboardInterrupt:
        pass

def test_connection(delay=5):
    """Tester la connexion après un délai"""
    time.sleep(delay)
    
    print("\n" + "=" * 70)
    print("[TEST] CONNEXION DES BOUTIQUIERS")
    print("=" * 70 + "\n")
    
    credentials = [
        ("admin", "temp_admin_1"),
        ("mouhamed365@gmail.com", "temp_mouhamed365@gmail.com_2"),
        ("pole45@gmail.com", "temp_pole45@gmail.com_3"),
        ("boutiquier1@test.com", "temp_boutiquier1@test.com_4"),
        ("MOMO@gmail.com", "temp_MOMO@gmail.com_6"),
    ]
    
    url = "http://localhost:8000/api/users/token/"
    success_count = 0
    
    for username, password in credentials:
        try:
            response = requests.post(
                url,
                json={"username": username, "password": password},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"[OK] {username}")
                print(f"     Role: {data.get('role', 'N/A')}")
                print(f"     Token: {data.get('access', '')[:30]}...")
                success_count += 1
            else:
                print(f"[ERREUR] {username} - Status {response.status_code}")
                
        except Exception as e:
            print(f"[ERREUR] {username} - {str(e)[:50]}")
    
    print("\n" + "=" * 70)
    print(f"[RESULTAT] {success_count}/{len(credentials)} connexions reussies")
    print("=" * 70 + "\n")

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("[*] DEMARRAGE DU SERVEUR DJANGO")
    print("=" * 70)
    print(f"\n[*] URL: http://localhost:8000/")
    print("[*] Frontend: http://localhost:8000/frontend/")
    print("[*] Arret: Ctrl+C\n")
    
    # Démarrer le serveur dans un thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Tester la connexion dans un thread séparé
    test_thread = threading.Thread(target=test_connection, args=(6,), daemon=False)
    test_thread.start()
    
    # Garder le script actif
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n[*] Serveur arrête")
