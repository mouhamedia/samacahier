# 🔐 Routes de Connexion - SamaCahier API

## 📋 Résumé des Routes

| Méthode | Route | Description |
|---------|-------|-------------|
| POST | `/api/users/token/` | **Connexion - Obtenir JWT Token** |
| POST | `/api/users/token/refresh/` | Rafraîchir le token |
| POST | `/api/users/` | Créer un nouvel utilisateur |
| GET | `/api/users/me/` | Obtenir infos utilisateur connecté |
| POST | `/api/users/change_password/` | Changer le mot de passe |

---

## 🔑 1. CONNEXION (Endpoint Principal)

### URL
```
POST http://localhost:8000/api/users/token/
```

### Headers
```json
{
  "Content-Type": "application/json"
}
```

### Body (JSON)
```json
{
  "username": "admin",
  "password": "temp_admin_1"
}
```

### Réponse (200 OK)
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "username": "admin",
  "email": "admin@example.com",
  "role": "boutiquier",
  "is_superuser": true
}
```

### Codes d'Erreur
- **401 Unauthorized** - Identifiants incorrects
- **400 Bad Request** - Données manquantes ou invalides

---

## 🔄 2. RAFRAÎCHIR LE TOKEN

### URL
```
POST http://localhost:8000/api/users/token/refresh/
```

### Body
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Réponse
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

## ➕ 3. CRÉER UN NOUVEL UTILISATEUR

### URL
```
POST http://localhost:8000/api/users/
```

### Headers
```json
{
  "Content-Type": "application/json"
}
```

### Body
```json
{
  "username": "nouveau_boutiquier",
  "email": "nouveau@test.com",
  "password": "password123456",
  "password_confirm": "password123456",
  "first_name": "Prénom",
  "last_name": "Nom",
  "phone": "+223 XX XXX XXXX",
  "role": "boutiquier"
}
```

### Réponse (201 Created)
```json
{
  "id": 10,
  "username": "nouveau_boutiquier",
  "email": "nouveau@test.com",
  "first_name": "Prénom",
  "last_name": "Nom",
  "phone": "+223 XX XXX XXXX",
  "role": "boutiquier",
  "is_active": true,
  "created_at": "2025-12-04T10:40:45Z"
}
```

---

## 👤 4. OBTENIR INFOS UTILISATEUR CONNECTÉ

### URL
```
GET http://localhost:8000/api/users/me/
```

### Headers
```json
{
  "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Réponse (200 OK)
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "first_name": "",
  "last_name": "",
  "phone": "",
  "role": "boutiquier",
  "is_active": true,
  "created_at": "2025-12-04T08:30:00Z"
}
```

---

## 🔑 5. CHANGER LE MOT DE PASSE

### URL
```
POST http://localhost:8000/api/users/change_password/
```

### Headers
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Body
```json
{
  "old_password": "temp_admin_1",
  "new_password": "nouveau_mot_de_passe_123"
}
```

### Réponse (200 OK)
```json
{
  "detail": "Mot de passe changé avec succès."
}
```

---

## 📝 Comptes de Test

```
1. admin
   Mot de passe: temp_admin_1

2. mouhamed365@gmail.com
   Mot de passe: temp_mouhamed365@gmail.com_2

3. pole45@gmail.com
   Mot de passe: temp_pole45@gmail.com_3

4. boutiquier1@test.com
   Mot de passe: temp_boutiquier1@test.com_4

5. MOMO@gmail.com
   Mot de passe: temp_MOMO@gmail.com_6
```

---

## 🧪 Test Rapide avec curl

### 1. Se connecter
```bash
curl -X POST http://localhost:8000/api/users/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"temp_admin_1"}'
```

### 2. Copier le token "access" de la réponse

### 3. Tester l'accès
```bash
curl -X GET http://localhost:8000/api/users/me/ \
  -H "Authorization: Bearer [VOTRE_TOKEN_ICI]"
```

---

## 🎯 Flux de Connexion Complet

1. **Utilisateur saisit identifiants** → `/api/users/token/` (POST)
2. **Reçoit JWT token** → Stocké localement
3. **Envoie token pour requêtes** → Header `Authorization: Bearer [token]`
4. **Token expire** → Utiliser `refresh` → `/api/users/token/refresh/` (POST)
5. **Reçoit nouveau token** → Continuer l'utilisation

---

## ⚠️ Erreurs Courantes

| Erreur | Cause | Solution |
|--------|-------|----------|
| 401 Unauthorized | Mauvais identifiants | Vérifier username/password |
| 403 Forbidden | Token expiré | Rafraîchir le token |
| 400 Bad Request | Données manquantes | Vérifier le JSON |
| 404 Not Found | Route incorrecte | Vérifier l'URL |
| CORS Error | Domaine non autorisé | Vérifier CORS settings |

---

## 📚 Frontend (Vue.js)

Le frontend accède aux routes via :

```javascript
// Connexion
const response = await axios.post(
  'http://localhost:8000/api/users/token/',
  { username, password }
);

// Stocker le token
localStorage.setItem('token', response.data.access);

// Utiliser le token pour d'autres requêtes
const headers = { Authorization: `Bearer ${token}` };
```

---

## 🚀 Démarrer l'API

```bash
python manage.py runserver
```

Accès : `http://localhost:8000/api/users/token/`
