# 🎯 ROUTES API - SamaCahier

## 📍 URL Base
```
http://localhost:8000
```

---

## 🔐 **1. AUTHENTIFICATION**

| Méthode | Route | Description |
|---------|-------|-------------|
| `POST` | `/api/users/` | Créer un utilisateur |
| `POST` | `/api/users/token/` | Obtenir le token JWT |
| `POST` | `/api/users/token/refresh/` | Rafraîchir le token |

**Exemple Postman - Connexion:**
```
POST http://localhost:8000/api/users/token/
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123456"
}

RÉPONSE:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "username": "admin",
  "email": "admin@example.com",
  "role": "boutiquier"
}
```

---

## 👤 **2. UTILISATEURS**

| Méthode | Route | Description | Auth |
|---------|-------|-------------|------|
| `GET` | `/api/users/` | Lister tous les utilisateurs | ✅ |
| `GET` | `/api/users/{id}/` | Récupérer un utilisateur | ✅ |
| `GET` | `/api/users/me/` | Récupérer l'utilisateur connecté | ✅ |
| `PUT` | `/api/users/{id}/` | Modifier un utilisateur | ✅ |
| `DELETE` | `/api/users/{id}/` | Supprimer un utilisateur | ✅ |
| `POST` | `/api/users/change_password/` | Changer le mot de passe | ✅ |

**Exemple - Voir l'utilisateur connecté:**
```
GET http://localhost:8000/api/users/me/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

RÉPONSE:
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "first_name": "Admin",
  "last_name": "User",
  "phone": "+223 70 000 0000",
  "role": "boutiquier",
  "is_active": true,
  "created_at": "2025-12-03T21:05:38.123456Z"
}
```

---

## 👥 **3. CLIENTS** (Réservé aux Boutiquiers)

| Méthode | Route | Description | Auth | Role |
|---------|-------|-------------|------|------|
| `GET` | `/api/clients/` | Lister mes clients | ✅ | Boutiquier |
| `GET` | `/api/clients/{id}/` | Récupérer un client | ✅ | Boutiquier |
| `POST` | `/api/clients/` | Créer un client | ✅ | Boutiquier |
| `PUT` | `/api/clients/{id}/` | Modifier un client | ✅ | Boutiquier |
| `DELETE` | `/api/clients/{id}/` | Supprimer un client | ✅ | Boutiquier |
| `GET` | `/api/clients/my_clients/` | Tous mes clients | ✅ | Boutiquier |

**Exemple - Créer un client:**
```
POST http://localhost:8000/api/clients/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
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
  "is_active": true,
  "created_at": "2025-12-03T21:10:00Z"
}
```

---

## 💳 **4. CRÉDITS** (Réservé aux Boutiquiers)

### 4a. Crédits
| Méthode | Route | Description | Auth | Role |
|---------|-------|-------------|------|------|
| `GET` | `/api/credits/credits/` | Lister mes crédits | ✅ | Boutiquier |
| `GET` | `/api/credits/credits/{id}/` | Récupérer un crédit | ✅ | Boutiquier |
| `POST` | `/api/credits/credits/` | Créer un crédit | ✅ | Boutiquier |
| `PUT` | `/api/credits/credits/{id}/` | Modifier un crédit | ✅ | Boutiquier |
| `DELETE` | `/api/credits/credits/{id}/` | Supprimer un crédit | ✅ | Boutiquier |
| `GET` | `/api/credits/credits/stats/` | Statistiques des crédits | ✅ | Boutiquier |
| `POST` | `/api/credits/credits/{id}/add_payment/` | Ajouter un paiement | ✅ | Boutiquier |

### 4b. Paiements
| Méthode | Route | Description | Auth | Role |
|---------|-------|-------------|------|------|
| `GET` | `/api/credits/payments/` | Lister les paiements | ✅ | Boutiquier |
| `GET` | `/api/credits/payments/{id}/` | Récupérer un paiement | ✅ | Boutiquier |
| `POST` | `/api/credits/payments/` | Créer un paiement | ✅ | Boutiquier |

**Exemple - Créer un crédit:**
```
POST http://localhost:8000/api/credits/credits/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "client": 1,
  "amount": 50000.00,
  "description": "Riz, millet et sucre",
  "due_date": "2025-12-15",
  "status": "pending"
}

RÉPONSE (201 Created):
{
  "id": 1,
  "client": 1,
  "client_name": "Mamadou Traoré",
  "boutiquier": 1,
  "amount": 50000.00,
  "paid_amount": 0.00,
  "remaining_amount": 50000.00,
  "status": "pending",
  "description": "Riz, millet et sucre",
  "due_date": "2025-12-15",
  "payments": [],
  "created_at": "2025-12-03T21:15:00Z"
}
```

**Exemple - Ajouter un paiement:**
```
POST http://localhost:8000/api/credits/credits/1/add_payment/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "amount": 25000.00,
  "payment_method": "cash",
  "note": "Paiement partiel du 03/12/2025"
}

RÉPONSE (201 Created):
{
  "id": 1,
  "credit": 1,
  "amount": 25000.00,
  "payment_date": "2025-12-03",
  "payment_method": "cash",
  "note": "Paiement partiel du 03/12/2025",
  "created_at": "2025-12-03T21:20:00Z"
}
```

**Exemple - Voir les statistiques:**
```
GET http://localhost:8000/api/credits/credits/stats/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

RÉPONSE:
{
  "total_credits": 3,
  "total_amount": 150000.00,
  "total_paid": 25000.00,
  "remaining": 125000.00,
  "by_status": {
    "pending": 1,
    "partial": 1,
    "paid": 1,
    "overdue": 0
  }
}
```

---

## 📊 **5. DASHBOARD**

| Méthode | Route | Description | Auth | Role |
|---------|-------|-------------|------|------|
| `GET` | `/api/dashboard/boutiquier/` | Tableau de bord boutiquier | ✅ | Boutiquier |
| `GET` | `/api/dashboard/client/` | Tableau de bord client | ✅ | Client/Boutiquier |

**Exemple - Dashboard Boutiquier:**
```
GET http://localhost:8000/api/dashboard/boutiquier/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

RÉPONSE:
{
  "general_stats": {
    "total_clients": 5,
    "total_credits": 10,
    "total_amount": 500000.00,
    "total_paid": 125000.00,
    "total_remaining": 375000.00,
    "average_credit_per_client": 100000.00
  },
  "credits_by_status": {
    "pending": 3,
    "partial": 2,
    "paid": 5,
    "overdue": 0
  },
  "overdue_credits": 0,
  "top_clients": [
    {
      "id": 1,
      "name": "Mamadou Traoré",
      "credit_count": 3,
      "total_credit": 150000.00
    },
    {
      "id": 2,
      "name": "Abdou Diop",
      "credit_count": 2,
      "total_credit": 100000.00
    }
  ],
  "payments_this_month": 25000.00
}
```

---

## 🛠️ **TEMPLATES POSTMAN PRÊTS À COPIER**

### 1️⃣ Authentification
```
POST http://localhost:8000/api/users/token/
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123456"
}
```

### 2️⃣ Créer un client
```
POST http://localhost:8000/api/clients/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "name": "Nom Client",
  "phone": "+223 XX XXX XXXX",
  "email": "client@example.com",
  "address": "Adresse",
  "is_active": true
}
```

### 3️⃣ Créer un crédit
```
POST http://localhost:8000/api/credits/credits/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "client": 1,
  "amount": 50000.00,
  "description": "Description",
  "due_date": "2025-12-31",
  "status": "pending"
}
```

### 4️⃣ Ajouter un paiement
```
POST http://localhost:8000/api/credits/credits/1/add_payment/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "amount": 25000.00,
  "payment_method": "cash",
  "note": "Note du paiement"
}
```

---

## ✅ Résumé des Routes par Rôle

### 👤 **Boutiquier a accès à:**
- ✅ Authentification (POST /api/users/token/)
- ✅ Profil utilisateur (GET /api/users/me/)
- ✅ Tous les endpoints `/api/clients/`
- ✅ Tous les endpoints `/api/credits/`
- ✅ Dashboard boutiquier (`GET /api/dashboard/boutiquier/`)

### 👥 **Client a accès à:**
- ✅ Authentification (POST /api/users/token/)
- ✅ Profil utilisateur (GET /api/users/me/)
- ✅ Dashboard client (`GET /api/dashboard/client/`)
- ❌ Pas d'accès à `/api/clients/`
- ❌ Pas d'accès à `/api/credits/`

---

## 🎓 Ordre recommandé de test

1. **POST /api/users/token/** - Se connecter
2. **GET /api/users/me/** - Voir son profil
3. **POST /api/clients/** - Créer un client
4. **GET /api/clients/** - Lister les clients
5. **POST /api/credits/credits/** - Créer un crédit
6. **POST /api/credits/credits/{id}/add_payment/** - Ajouter un paiement
7. **GET /api/credits/credits/stats/** - Voir les stats
8. **GET /api/dashboard/boutiquier/** - Voir le dashboard

---

✨ **Prêt à tester !** Importe le fichier JSON dans Postman et commence 🚀
