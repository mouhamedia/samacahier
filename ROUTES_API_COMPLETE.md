# 🛣️ Routes Complètes - SamaCahier API

## 📌 Configuration Générale

**Base URL:** `http://localhost:8000`
**API Prefix:** `/api/`

---

## 👥 USERS (Authentification & Utilisateurs)

| Méthode | Route | Description | Auth |
|---------|-------|-------------|------|
| POST | `/api/users/token/` | **CONNEXION** - Obtenir JWT | ❌ |
| POST | `/api/users/token/refresh/` | Rafraîchir token | ❌ |
| POST | `/api/users/` | Créer utilisateur | ❌ |
| GET | `/api/users/` | Lister tous les utilisateurs | ✅ |
| GET | `/api/users/{id}/` | Détails utilisateur | ✅ |
| PUT | `/api/users/{id}/` | Modifier utilisateur | ✅ |
| PATCH | `/api/users/{id}/` | Modifier partiellement | ✅ |
| DELETE | `/api/users/{id}/` | Supprimer utilisateur | ✅ |
| GET | `/api/users/me/` | Infos utilisateur connecté | ✅ |
| POST | `/api/users/change_password/` | Changer mot de passe | ✅ |

---

## 👨‍💼 CLIENTS

| Méthode | Route | Description | Auth |
|---------|-------|-------------|------|
| GET | `/api/clients/` | Lister clients | ✅ |
| POST | `/api/clients/` | Créer client | ✅ |
| GET | `/api/clients/{id}/` | Détails client | ✅ |
| PUT | `/api/clients/{id}/` | Modifier client | ✅ |
| PATCH | `/api/clients/{id}/` | Modifier partiellement | ✅ |
| DELETE | `/api/clients/{id}/` | Supprimer client | ✅ |

**Paramètres:**
- `?boutiquier={id}` - Filtrer par boutiquier
- `?status=active` - Filtrer par statut

---

## 💳 CRÉDITS

| Méthode | Route | Description | Auth |
|---------|-------|-------------|------|
| GET | `/api/credits/` | Lister crédits | ✅ |
| POST | `/api/credits/` | Créer crédit | ✅ |
| GET | `/api/credits/{id}/` | Détails crédit | ✅ |
| PUT | `/api/credits/{id}/` | Modifier crédit | ✅ |
| PATCH | `/api/credits/{id}/` | Modifier partiellement | ✅ |
| DELETE | `/api/credits/{id}/` | Supprimer crédit | ✅ |

**Paramètres:**
- `?client={id}` - Filtrer par client
- `?status=paid` - Filtrer par statut

---

## 📊 DASHBOARD

| Méthode | Route | Description | Auth |
|---------|-------|-------------|------|
| GET | `/api/dashboard/stats/` | Stats générales | ✅ |
| GET | `/api/dashboard/boutiquier/{id}/stats/` | Stats boutiquier | ✅ |

---

## 🔧 ADMIN (Routes Spéciales)

| Méthode | Route | Description | Auth |
|---------|-------|-------------|------|
| GET | `/api/admin/boutiquiers/` | Lister tous boutiquiers | ✅ |
| GET | `/api/admin/boutiquiers/{id}/` | Détails boutiquier | ✅ |
| PATCH | `/api/admin/boutiquiers/{id}/toggle-status/` | Activer/Désactiver | ✅ |
| PATCH | `/api/admin/clients/{id}/toggle-status/` | Activer/Désactiver client | ✅ |
| PATCH | `/api/admin/credits/{id}/toggle-status/` | Activer/Désactiver crédit | ✅ |

---

## 🔑 Authentification

### Headers Requis (pour routes avec ✅)

```json
{
  "Authorization": "Bearer {JWT_TOKEN}",
  "Content-Type": "application/json"
}
```

### Comment Obtenir le Token

1. **POST à `/api/users/token/`**

```bash
curl -X POST http://localhost:8000/api/users/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"temp_admin_1"}'
```

2. **Copier le "access" token**

3. **Utiliser dans les requêtes**

```bash
curl -X GET http://localhost:8000/api/users/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

---

## 📝 Format des Données

### Utilisateur
```json
{
  "username": "admin",
  "email": "admin@example.com",
  "password": "password123456",
  "password_confirm": "password123456",
  "first_name": "Prénom",
  "last_name": "Nom",
  "phone": "+223 XX XXX XXXX",
  "role": "boutiquier"
}
```

### Client
```json
{
  "name": "Nom du client",
  "phone": "+223 XX XXX XXXX",
  "boutiquier": 1,
  "status": "active"
}
```

### Crédit
```json
{
  "client": 1,
  "amount": 50000,
  "paid_amount": 20000,
  "product": "Riz",
  "status": "partial"
}
```

---

## ✅ Comptes de Test

```
1. admin
   Password: temp_admin_1
   Role: admin (boutiquier)

2. mouhamed365@gmail.com
   Password: temp_mouhamed365@gmail.com_2
   Role: boutiquier

3. pole45@gmail.com
   Password: temp_pole45@gmail.com_3
   Role: boutiquier

4. boutiquier1@test.com
   Password: temp_boutiquier1@test.com_4
   Role: boutiquier

5. MOMO@gmail.com
   Password: temp_MOMO@gmail.com_6
   Role: boutiquier
```

---

## 🧪 Tests Rapides

### 1. Connexion
```bash
curl -X POST http://localhost:8000/api/users/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"temp_admin_1"}'
```

### 2. Lister Boutiquiers
```bash
curl -X GET http://localhost:8000/api/admin/boutiquiers/ \
  -H "Authorization: Bearer {TOKEN}"
```

### 3. Créer Client
```bash
curl -X POST http://localhost:8000/api/clients/ \
  -H "Authorization: Bearer {TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"name":"Client Test","phone":"+223 XX","boutiquier":1}'
```

### 4. Créer Crédit
```bash
curl -X POST http://localhost:8000/api/credits/ \
  -H "Authorization: Bearer {TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"client":1,"amount":100000,"product":"Riz"}'
```

---

## 📚 Codes de Réponse

| Code | Signification |
|------|---------------|
| 200 | OK - Succès |
| 201 | Created - Ressource créée |
| 204 | No Content - Suppression réussie |
| 400 | Bad Request - Données invalides |
| 401 | Unauthorized - Auth requise |
| 403 | Forbidden - Accès refusé |
| 404 | Not Found - Ressource inexistante |
| 500 | Server Error - Erreur serveur |

---

## 🚀 Démarrage

```bash
# Démarrer le serveur
python manage.py runserver

# Serveur accessible à
http://localhost:8000/api/

# Tests avec Postman
Importer: SamaCahier_API_Postman.json
```
