# 🧪 TEST POSTMAN - Connexion Client

## Test complet de la nouvelle route

### 1️⃣ Étape 1: Créer un client (Boutiquier)

```
POST http://localhost:8000/api/clients/

Authorization: Bearer YOUR_BOUTIQUIER_TOKEN
Content-Type: application/json

{
  "name": "Test Client",
  "phone": "+223 70 123 4567",
  "email": "client@test.com",
  "address": "Bamako, Mali",
  "is_active": true
}

RÉPONSE:
{
  "id": 1,
  "access_code": "ABC123",  ← COPIER CE CODE
  "name": "Test Client",
  ...
}
```

---

### 2️⃣ Étape 2: Créer un crédit pour ce client (Boutiquier)

```
POST http://localhost:8000/api/credits/credits/

Authorization: Bearer YOUR_BOUTIQUIER_TOKEN
Content-Type: application/json

{
  "client": 1,
  "amount": 50000.00,
  "description": "Riz et millet",
  "due_date": "2025-12-15",
  "status": "pending"
}

RÉPONSE: Credit créé ✅
```

---

### 3️⃣ Étape 3: ⭐ CLIENT SE CONNECTE AVEC SON CODE

```
POST http://localhost:8000/api/clients/access/

Content-Type: application/json
(⚠️ PAS d'Authorization header!)

{
  "access_code": "ABC123"
}

RÉPONSE (200):
{
  "client_id": 1,
  "client_name": "Test Client",
  "access_code": "ABC123",
  "phone": "+223 70 123 4567",
  "email": "client@test.com",
  "boutiquier_name": "Admin User",
  "credits_info": {
    "total_credits": 1,
    "total_amount": 50000.0,
    "total_paid": 0.0,
    "remaining": 50000.0,
    "credits": [
      {
        "id": 1,
        "amount": 50000.0,
        "paid_amount": 0.0,
        "remaining": 50000.0,
        "status": "pending",
        "description": "Riz et millet",
        "due_date": "2025-12-15"
      }
    ]
  }
}
```

✅ **CLIENT PEUT MAINTENANT VOIR SES CRÉDITS!**

---

## 📝 Notes importantes

1. **Pas d'authentification** - La route `/api/clients/access/` n'a pas besoin de Bearer token
2. **Code sensible à la casse** - "ABC123" ≠ "abc123" (ou convertir en majuscules)
3. **Code unique** - Chaque client en a un seul
4. **Impossible de modifier** - Le client ne peut que consulter

---

## 🔄 Test avec plusieurs clients

### Client 1: ABC123
```
POST http://localhost:8000/api/clients/access/
{
  "access_code": "ABC123"
}
→ Voit ses crédits
```

### Client 2: DEF456
```
POST http://localhost:8000/api/clients/access/
{
  "access_code": "DEF456"
}
→ Voit SES crédits (pas ceux du client 1)
```

---

## ❌ Erreurs possibles

### Erreur 1: Code manquant
```
POST http://localhost:8000/api/clients/access/

{}

RÉPONSE (400):
{
  "error": "Le code d'accès est requis"
}
```

### Erreur 2: Code invalide
```
POST http://localhost:8000/api/clients/access/

{
  "access_code": "INVALID"
}

RÉPONSE (404):
{
  "error": "Code d'accès invalide ou client inactif"
}
```

### Erreur 3: Client inactif
```
Si le client a is_active=false, même avec un code correct:

RÉPONSE (404):
{
  "error": "Code d'accès invalide ou client inactif"
}
```

---

## 💡 Cas de test recommandés

### Test 1: Client avec 1 crédit payé
```
✅ Créer client
✅ Créer crédit de 50 000 F
✅ Ajouter paiement de 50 000 F
✅ Client accède → Voit "paid"
```

### Test 2: Client avec crédit partiellement payé
```
✅ Créer client
✅ Créer crédit de 100 000 F
✅ Ajouter paiement de 30 000 F
✅ Client accède → Voit "partial" + 70 000 F restants
```

### Test 3: Client avec plusieurs crédits
```
✅ Créer client
✅ Créer 3 crédits différents
✅ Ajouter différents paiements
✅ Client accède → Voit les 3 crédits avec leurs statuts
```

### Test 4: Client inactif
```
✅ Créer client avec is_active=true
✅ Passer is_active=false (PUT)
✅ Client essaie d'accéder → Erreur 404
```

---

## 🎯 Intégration dans une application

### JavaScript/Fetch
```javascript
async function loginClient(accessCode) {
  const response = await fetch('http://localhost:8000/api/clients/access/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ access_code: accessCode })
  });
  
  if (response.ok) {
    const data = await response.json();
    console.log('Client:', data.client_name);
    console.log('Crédits:', data.credits_info);
  } else {
    console.log('Code invalide');
  }
}

// Utilisation
loginClient('ABC123');
```

### Python/Requests
```python
import requests

def login_client(access_code):
    url = 'http://localhost:8000/api/clients/access/'
    data = {'access_code': access_code}
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Client: {result['client_name']}")
        print(f"Crédits: {result['credits_info']}")
    else:
        print("Code invalide")

# Utilisation
login_client('ABC123')
```

---

## ✨ Résumé

| Aspect | Détail |
|--------|--------|
| **Route** | POST /api/clients/access/ |
| **Auth** | ❌ Pas requise |
| **Paramètre** | access_code (string) |
| **Réponse** | Client info + tous ses crédits |
| **Erreur 400** | Code manquant |
| **Erreur 404** | Code invalide ou client inactif |

---

**Prêt à tester!** 🚀
