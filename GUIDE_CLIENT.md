# 🎯 GUIDE CLIENT - Connexion Simplifiée

## ✅ Système de code d'accès simple

Chaque client a automatiquement un **code d'accès unique** (par exemple: `ABC123`).
Le client peut entrer ce code dans l'application mobile/web pour voir ses crédits.

---

## 🔐 Comment ça marche

### 1️⃣ Boutiquier crée un client
```
POST http://localhost:8000/api/clients/
Authorization: Bearer {BOUTIQUIER_TOKEN}
Content-Type: application/json

{
  "name": "Mamadou Traoré",
  "phone": "+223 70 123 4567",
  "email": "mamadou@example.com",
  "address": "Bamako, Mali",
  "is_active": true
}

RÉPONSE (201 Created):
{
  "id": 1,
  "boutiquier": 1,
  "boutiquier_name": "admin",
  "name": "Mamadou Traoré",
  "phone": "+223 70 123 4567",
  "email": "mamadou@example.com",
  "address": "Bamako, Mali",
  "access_code": "ABC123",        ← CODE GÉNÉRÉ AUTOMATIQUEMENT
  "is_active": true,
  "created_at": "2025-12-03T21:10:00Z"
}
```

### 2️⃣ Le client se connecte avec son code
```
POST http://localhost:8000/api/clients/access/
Content-Type: application/json

{
  "access_code": "ABC123"
}

RÉPONSE (200 OK):
{
  "client_id": 1,
  "client_name": "Mamadou Traoré",
  "access_code": "ABC123",
  "phone": "+223 70 123 4567",
  "email": "mamadou@example.com",
  "boutiquier_name": "Admin User",
  "credits_info": {
    "total_credits": 2,
    "total_amount": 100000.00,
    "total_paid": 25000.00,
    "remaining": 75000.00,
    "credits": [
      {
        "id": 1,
        "amount": 50000.00,
        "paid_amount": 25000.00,
        "remaining": 25000.00,
        "status": "partial",
        "description": "Riz et millet",
        "due_date": "2025-12-15"
      },
      {
        "id": 2,
        "amount": 50000.00,
        "paid_amount": 0.00,
        "remaining": 50000.00,
        "status": "pending",
        "description": "Sucre et huile",
        "due_date": "2025-12-20"
      }
    ]
  }
}
```

---

## 📋 Liste complète des Routes Client

### 🎫 Connexion Client (Pas d'authentification requise)
| Méthode | Route | Description |
|---------|-------|-------------|
| `POST` | `/api/clients/access/` | Se connecter avec un code d'accès |

**Paramètre:**
- `access_code` (string) - Le code unique du client (ex: ABC123)

**Erreurs possibles:**
- `400` - Code d'accès manquant
- `404` - Code invalide ou client inactif

---

## 🎯 Scénario complet: Création et Connexion Client

### Étape 1: Boutiquier se connecte
```
POST http://localhost:8000/api/users/token/
{
  "username": "admin",
  "password": "admin123456"
}

RÉPONSE:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Étape 2: Boutiquier crée un client
```
POST http://localhost:8000/api/clients/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
{
  "name": "Abdou Diop",
  "phone": "+223 70 234 5678",
  "address": "Segou, Mali",
  "is_active": true
}

RÉPONSE:
{
  "id": 2,
  "access_code": "DEF456"    ← À communiquer au client
}
```

### Étape 3: Boutiquier crée des crédits pour ce client
```
POST http://localhost:8000/api/credits/credits/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
{
  "client": 2,
  "amount": 75000.00,
  "description": "Riz de qualité",
  "due_date": "2025-12-20"
}
```

### Étape 4: Le client se connecte avec son code
```
POST http://localhost:8000/api/clients/access/
{
  "access_code": "DEF456"
}

RÉPONSE:
{
  "client_id": 2,
  "client_name": "Abdou Diop",
  "access_code": "DEF456",
  "phone": "+223 70 234 5678",
  "boutiquier_name": "Admin User",
  "credits_info": {
    "total_credits": 1,
    "total_amount": 75000.00,
    "total_paid": 0.00,
    "remaining": 75000.00,
    "credits": [
      {
        "id": 3,
        "amount": 75000.00,
        "paid_amount": 0.00,
        "remaining": 75000.00,
        "status": "pending",
        "description": "Riz de qualité",
        "due_date": "2025-12-20"
      }
    ]
  }
}
```

---

## 📱 Exemple d'affichage pour le client

```
┌─────────────────────────────────┐
│   CONSULTER MES CRÉDITS         │
├─────────────────────────────────┤
│                                 │
│  Entrez votre code d'accès:     │
│  ┌─────────────────────────────┐│
│  │ ABC123                      ││
│  └─────────────────────────────┘│
│                                 │
│        [  VALIDER  ]            │
│                                 │
└─────────────────────────────────┘

↓ APRÈS VALIDATION ↓

┌─────────────────────────────────┐
│   CLIENT: Mamadou Traoré        │
│   BOUTIQUIER: Admin User        │
├─────────────────────────────────┤
│   RÉSUMÉ DES CRÉDITS            │
│                                 │
│   Total dû:      100 000 F      │
│   Payé:           25 000 F      │
│   Restant:        75 000 F      │
│                                 │
├─────────────────────────────────┤
│   DÉTAIL DES CRÉDITS            │
│                                 │
│   📦 Crédit #1                  │
│   Montant: 50 000 F             │
│   Payé: 25 000 F                │
│   Statut: Partiellement payé    │
│   Échéance: 15/12/2025          │
│   Description: Riz et millet    │
│                                 │
│   📦 Crédit #2                  │
│   Montant: 50 000 F             │
│   Payé: 0 F                     │
│   Statut: En attente de paiement│
│   Échéance: 20/12/2025          │
│   Description: Sucre et huile   │
│                                 │
└─────────────────────────────────┘
```

---

## 🔄 Statuts des crédits affichés au client

| Statut | Couleur | Signification |
|--------|---------|---------------|
| `pending` | 🔴 Rouge | En attente de paiement |
| `partial` | 🟡 Orange | Partiellement payé |
| `paid` | 🟢 Vert | Entièrement payé |
| `overdue` | 🔴 Rouge foncé | En retard |

---

## 💡 Points clés pour l'implémentation

### 1️⃣ **Code généré automatiquement**
- Format: 3 lettres + 3 chiffres (ABC123)
- Unique pour chaque client
- Généré une seule fois à la création

### 2️⃣ **Pas d'authentification requise**
- Le client n'a pas besoin de compte utilisateur
- Juste le code d'accès

### 3️⃣ **Informations visibles au client**
- ✅ Son nom
- ✅ Le nom du boutiquier
- ✅ Total des crédits
- ✅ Montant payé
- ✅ Montant restant
- ✅ Détail de chaque crédit
- ✅ Statut de chaque crédit
- ✅ Dates d'échéance

### 4️⃣ **Sécurité**
- Le code est unique et difficile à deviner
- Seuls les crédits du client sont affichés
- Le client ne peut pas modifier les données

---

## 🧪 Test sur Postman

### Créer un client
```
POST http://localhost:8000/api/clients/

Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "name": "Test Client",
  "phone": "+223 70 000 0001",
  "address": "Bamako",
  "is_active": true
}

👉 Copier le access_code de la réponse
```

### Accéder avec le code
```
POST http://localhost:8000/api/clients/access/

Content-Type: application/json

{
  "access_code": "ABC123"
}
```

### Voir la réponse avec tous les crédits!
✅ C'est prêt!

---

## 🚀 Résumé des avantages

✅ **Simple** - Juste entrer un code  
✅ **Rapide** - Pas de création de compte  
✅ **Sûr** - Code unique pour chaque client  
✅ **Transparent** - Voir tous ses crédits et paiements  
✅ **Sans Internet** - Peut être imprimé et donné au client  

---

**Le client reçoit juste son code d'accès (ABC123) et peut le taper dans l'app mobile pour voir ses crédits!** 🎉
