# 📚 Guide de Test - SamaCahier API sur Postman

## 🚀 Serveur en cours d'exécution

L'API est disponible à : **http://localhost:8000**

### Informations de connexion par défaut :
```
Username: admin
Password: admin123456
Rôle: boutiquier
```

---

## 📋 Étapes de test recommandées

### 1️⃣ **AUTHENTIFICATION**

#### a) Se connecter (Obtenir le Token JWT)
```
POST http://localhost:8000/api/users/token/

Body (JSON):
{
  "username": "admin",
  "password": "admin123456"
}
```

**Réponse attendue:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

✅ **Copier la valeur `access` pour les requêtes suivantes**

---

### 2️⃣ **UTILISATEURS**

#### a) Voir l'utilisateur connecté
```
GET http://localhost:8000/api/users/me/

Header:
Authorization: Bearer {YOUR_ACCESS_TOKEN}
```

#### b) Créer un nouvel utilisateur (client)
```
POST http://localhost:8000/api/users/

Body (JSON):
{
  "username": "client1",
  "email": "client1@example.com",
  "password": "password123456",
  "password_confirm": "password123456",
  "first_name": "Abdou",
  "last_name": "Diop",
  "phone": "+223 70 XXX XXXX",
  "role": "client"
}
```

#### c) Créer un boutiquier
```
POST http://localhost:8000/api/users/

Body (JSON):
{
  "username": "boutiquier2",
  "email": "boutiquier2@example.com",
  "password": "password123456",
  "password_confirm": "password123456",
  "first_name": "Massa",
  "last_name": "Keita",
  "phone": "+223 71 XXX XXXX",
  "role": "boutiquier"
}
```

---

### 3️⃣ **CLIENTS** (Réservé aux Boutiquiers)

#### a) Lister mes clients
```
GET http://localhost:8000/api/clients/

Header:
Authorization: Bearer {BOUTIQUIER_TOKEN}
```

#### b) Créer un client
```
POST http://localhost:8000/api/clients/

Header:
Authorization: Bearer {BOUTIQUIER_TOKEN}
Content-Type: application/json

Body (JSON):
{
  "name": "Mamadou Traoré",
  "phone": "+223 XX XXX XXXX",
  "email": "mamadou@example.com",
  "address": "Bamako, Mali",
  "is_active": true
}
```

#### c) Modifier un client
```
PUT http://localhost:8000/api/clients/1/

Header:
Authorization: Bearer {BOUTIQUIER_TOKEN}
Content-Type: application/json

Body (JSON):
{
  "name": "Mamadou Traoré Updated",
  "phone": "+223 XX XXX YYYY",
  "email": "updated@example.com",
  "is_active": true
}
```

#### d) Supprimer un client
```
DELETE http://localhost:8000/api/clients/1/

Header:
Authorization: Bearer {BOUTIQUIER_TOKEN}
```

---

### 4️⃣ **CRÉDITS** (Réservé aux Boutiquiers)

#### a) Lister mes crédits
```
GET http://localhost:8000/api/credits/credits/

Header:
Authorization: Bearer {BOUTIQUIER_TOKEN}
```

#### b) Créer un crédit pour un client
```
POST http://localhost:8000/api/credits/credits/

Header:
Authorization: Bearer {BOUTIQUIER_TOKEN}
Content-Type: application/json

Body (JSON):
{
  "client": 1,
  "amount": 50000.00,
  "description": "Riz et millet",
  "due_date": "2025-12-15",
  "status": "pending"
}
```

💡 **Note:** Remplacer `"client": 1` avec l'ID du client créé

#### c) Ajouter un paiement
```
POST http://localhost:8000/api/credits/credits/1/add_payment/

Header:
Authorization: Bearer {BOUTIQUIER_TOKEN}
Content-Type: application/json

Body (JSON):
{
  "amount": 25000.00,
  "payment_method": "cash",
  "note": "Paiement partiel du 03/12/2025"
}
```

#### d) Voir les statistiques des crédits
```
GET http://localhost:8000/api/credits/credits/stats/

Header:
Authorization: Bearer {BOUTIQUIER_TOKEN}
```

**Réponse attendue:**
```json
{
  "total_credits": 5,
  "total_amount": 250000.00,
  "total_paid": 25000.00,
  "remaining": 225000.00,
  "by_status": {
    "pending": 2,
    "partial": 1,
    "paid": 2,
    "overdue": 0
  }
}
```

#### e) Lister tous les paiements
```
GET http://localhost:8000/api/credits/payments/

Header:
Authorization: Bearer {BOUTIQUIER_TOKEN}
```

---

### 5️⃣ **DASHBOARD**

#### a) Tableau de bord Boutiquier
```
GET http://localhost:8000/api/dashboard/boutiquier/

Header:
Authorization: Bearer {BOUTIQUIER_TOKEN}
```

**Réponse attendue:**
```json
{
  "general_stats": {
    "total_clients": 3,
    "total_credits": 5,
    "total_amount": 250000.00,
    "total_paid": 25000.00,
    "total_remaining": 225000.00,
    "average_credit_per_client": 83333.33
  },
  "credits_by_status": {
    "pending": 2,
    "partial": 1,
    "paid": 2,
    "overdue": 0
  },
  "overdue_credits": 0,
  "top_clients": [...],
  "payments_this_month": 25000.00
}
```

#### b) Tableau de bord Client
```
GET http://localhost:8000/api/dashboard/client/

Header:
Authorization: Bearer {CLIENT_TOKEN}
```

---

## 🔒 Configuration dans Postman

### Importer la collection

1. Ouvrir **Postman**
2. Cliquer sur **"Import"**
3. Choisir **"Upload Files"**
4. Sélectionner le fichier **`SamaCahier_API_Postman.json`**
5. La collection sera importée avec tous les endpoints

### Configurer le Token automatiquement

1. Aller à l'onglet **"Tests"** du endpoint `POST /api/users/token/`
2. Ajouter le script suivant :
```javascript
if (pm.response.code === 200) {
    var jsonData = pm.response.json();
    pm.environment.set("access_token", jsonData.access);
    pm.environment.set("refresh_token", jsonData.refresh);
}
```

3. Dans les autres endpoints, utiliser dans l'header Authorization :
```
Bearer {{access_token}}
```

---

## 📊 Scénario de test complet

### Étape 1: Inscription et Authentification
1. ✅ Créer un nouvel utilisateur (boutiquier)
2. ✅ Se connecter pour obtenir le token

### Étape 2: Gestion des Clients
1. ✅ Créer 3 clients
2. ✅ Récupérer la liste des clients
3. ✅ Modifier un client
4. ✅ Supprimer un client

### Étape 3: Gestion des Crédits
1. ✅ Créer 5 crédits pour différents clients
2. ✅ Ajouter des paiements partiels
3. ✅ Vérifier les statistiques
4. ✅ Voir les top clients

### Étape 4: Dashboard
1. ✅ Consulter le dashboard du boutiquier
2. ✅ Vérifier les statistiques globales

---

## 🐛 Codes d'erreur courants

| Code | Signification | Solution |
|------|--------------|----------|
| 400 | Bad Request | Vérifier le format JSON |
| 401 | Unauthorized | Ajouter le token Bearer dans les headers |
| 403 | Forbidden | L'utilisateur n'a pas les permissions (ex: client essayant d'accéder à /clients/) |
| 404 | Not Found | L'ID n'existe pas |
| 500 | Server Error | Vérifier les logs du serveur |

---

## 📞 Support

- **Admin**: `admin` / `admin123456`
- **Serveur**: `http://localhost:8000`
- **Admin Interface**: `http://localhost:8000/admin/`
