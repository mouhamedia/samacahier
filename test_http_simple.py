#!/usr/bin/env python3
"""
Test HTTP de la connexion - Vérifiez directement la réponse API
"""
import urllib.request
import json

print("\n" + "="*70)
print("🧪 TEST CONNEXION BOUTQUIER - HTTP DIRECT")
print("="*70 + "\n")

# Tester le nouvel endpoint
url = "http://localhost:8000/api/users/login/"
data = json.dumps({
    "username": "nouveau_boutiquier_1",
    "password": "TempPassword123!"
}).encode('utf-8')

headers = {
    "Content-Type": "application/json"
}

try:
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        
        print("✅ CONNEXION RÉUSSIE!\n")
        print(f"Status: {response.status}")
        print(f"Username: {result.get('username')}")
        print(f"Email: {result.get('email')}")
        print(f"Role: {result.get('role')}")
        print(f"Access Token: {result.get('access', '')[:50]}...")
        print(f"Refresh Token: {result.get('refresh', '')[:50]}...")
        
except urllib.error.HTTPError as e:
    print(f"❌ Erreur HTTP {e.code}")
    error_response = e.read().decode('utf-8')
    print(f"Response: {error_response}\n")
    
except Exception as e:
    print(f"❌ Erreur: {str(e)}\n")

print("="*70 + "\n")
