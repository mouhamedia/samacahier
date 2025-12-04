# 🚀 DÉMARRAGE RAPIDE

## ✅ Serveur en cours d'exécution

**L'API est disponible à :** `http://localhost:8000`

---

## 🔐 Connexion par défaut

### Compte Administrateur (Boutiquier)
```
📧 Email: admin@example.com
👤 Username: admin
🔑 Password: admin123456
👔 Rôle: Boutiquier
```

### Pour obtenir le Token JWT:
```bash
POST http://localhost:8000/api/users/token/

Body:
{
  "username": "admin",
  "password": "admin123456"
}
```

---

## 📁 Fichiers d'aide

| Fichier | Description |
|---------|-------------|
| `ROUTES_API.md` | 📋 Toutes les routes avec exemples |
| `GUIDE_POSTMAN.md` | 📚 Guide complet de test |
| `SamaCahier_API_Postman.json` | 📤 Collection Postman prête à importer |

---

## 🎯 Les 5 routes principales pour commencer

### 1️⃣ Se connecter
```
POST http://localhost:8000/api/users/token/
{
  "username": "admin",
  "password": "admin123456"
}
```
📌 **Copier le token `access` pour les autres requêtes**

### 2️⃣ Créer un client
```
POST http://localhost:8000/api/clients/
Authorization: Bearer {ACCESS_TOKEN}
{
  "name": "Mamadou Traoré",
  "phone": "+223 70 123 4567",
  "email": "mamadou@example.com",
  "address": "Bamako, Mali",
  "is_active": true
}
```

### 3️⃣ Créer un crédit
```
POST http://localhost:8000/api/credits/credits/
Authorization: Bearer {ACCESS_TOKEN}
{
  "client": 1,
  "amount": 50000.00,
  "description": "Riz et millet",
  "due_date": "2025-12-15",
  "status": "pending"
}
```

### 4️⃣ Ajouter un paiement
```
POST http://localhost:8000/api/credits/credits/1/add_payment/
Authorization: Bearer {ACCESS_TOKEN}
{
  "amount": 25000.00,
  "payment_method": "cash",
  "note": "Paiement partiel"
}
```

### 5️⃣ Voir les statistiques
```
GET http://localhost:8000/api/credits/credits/stats/
Authorization: Bearer {ACCESS_TOKEN}
```

---

## 🌐 Liens utiles

- **API** : http://localhost:8000/
- **Admin Panel** : http://localhost:8000/admin/
  - Username: `admin`
  - Password: `admin123456`
- **API Root** : http://localhost:8000/api/

---

## 📊 Collection Postman

### Importer dans Postman:

1. Ouvrir **Postman**
2. Cliquer sur **"Import"**
3. Sélectionner **`SamaCahier_API_Postman.json`**
4. La collection s'importera avec tous les endpoints

Tous les endpoints sont organisés par catégorie:
- 🔐 AUTHENTIFICATION
- 👤 UTILISATEURS  
- 👥 CLIENTS
- 💳 CRÉDITS
- 📊 DASHBOARD

---

## 💡 Conseils pour tester

1. **Toujours obtenir un token d'abord** avant d'appeler les autres endpoints
2. **Ajouter le header** `Authorization: Bearer {token}` à chaque requête
3. **Vérifier le Content-Type** : `application/json`
4. **Remplacer les IDs** dans les URLs (par ex: `/api/clients/1/` -> `/api/clients/2/`)
5. **Copier les réponses** pour utiliser les IDs des objets créés

---

## 🐛 Dépannage

### Le serveur ne démarre pas?
```powershell
cd "c:\Users\Lenovo Yoga 6\Desktop\semestre 2\python\samacahier"
python manage.py runserver
```

### Erreur 401 Unauthorized?
- ✅ Vérifiez que vous avez copié le token `access` (pas `refresh`)
- ✅ Ajoutez le header: `Authorization: Bearer {token}`

### Erreur 403 Forbidden?
- ✅ Vérifiez votre rôle (boutiquier pour /clients/ et /credits/)

### Token expiré?
```
POST http://localhost:8000/api/users/token/refresh/
{
  "refresh": "YOUR_REFRESH_TOKEN"
}
```

---

## 📚 Documentation complète

Voir les fichiers :
- **ROUTES_API.md** - Toutes les routes avec exemples
- **GUIDE_POSTMAN.md** - Guide détaillé de test

---

**Bon test ! 🚀**
