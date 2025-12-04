# 📬 Guide Postman - Tester la Connexion des Boutiquiers

## 📌 Étapes Simples

### 1️⃣ Ouvrir Postman

Téléchargez et ouvrez **Postman** (https://www.postman.com/downloads/)

### 2️⃣ Importer la Collection

1. Cliquez sur **Import**
2. Choisissez **File** → Sélectionnez `SamaCahier_API_Postman.json`
3. Cliquez **Import**

### 3️⃣ Tester la Connexion des Boutiquiers

#### **Étape 1: Démarrer le serveur**

```bash
cd c:\Users\Lenovo Yoga 6\Desktop\semestre 2\python\samacahier
python manage.py runserver --noreload
```

#### **Étape 2: Dans Postman**

1. Allez à **Collections** → **SamaCahier API**
2. Ouvrez le dossier **AUTHENTIFICATION**
3. Sélectionnez la requête **"Se connecter (Obtenir le Token JWT)"**

#### **Étape 3: Changer les identifiants**

Remplacez le body JSON par :

```json
{
  "username": "admin",
  "password": "temp_admin_1"
}
```

Ou utilisez l'un des autres comptes :

| Utilisateur | Mot de passe |
|-------------|-------------|
| admin | temp_admin_1 |
| mouhamed365@gmail.com | temp_mouhamed365@gmail.com_2 |
| pole45@gmail.com | temp_pole45@gmail.com_3 |
| boutiquier1@test.com | temp_boutiquier1@test.com_4 |
| MOMO@gmail.com | temp_MOMO@gmail.com_6 |

#### **Étape 4: Envoyer la Requête**

Cliquez sur **Send** (bleu)

#### **Étape 5: Vérifier la Réponse**

Vous devriez voir :

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "username": "admin",
  "email": "admin@example.com",
  "role": "boutiquier",
  "is_superuser": true
}
```

✅ **Si vous voyez cela = SUCCÈS!**

---

## 🔧 Tester d'autres endpoints

### Créer un Nouvel Utilisateur

1. Sélectionnez **"Inscription (Créer un utilisateur)"**
2. Modifiez le body :

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

3. Cliquez **Send**

### Obtenir les Informations de l'Utilisateur Connecté

1. Sélectionnez **"Informations de l'utilisateur"** ou **"me"**
2. Allez à l'onglet **Headers**
3. Ajoutez un header :
   - Key: `Authorization`
   - Value: `Bearer [VOTRE_TOKEN]` (remplacez par le token obtenu plus haut)
4. Cliquez **Send**

---

## ✅ Résultat Attendu

Si tout fonctionne :
- ✅ Les boutiquiers se connectent avec leurs identifiants
- ✅ Ils reçoivent un JWT token
- ✅ Le token les authentifie pour les autres requêtes

---

## ❌ Troubleshooting

| Erreur | Cause | Solution |
|--------|-------|----------|
| 401 Unauthorized | Mauvais mot de passe | Vérifiez le fichier `credentials_boutiquiers.txt` |
| 404 Not Found | URL incorrecte | Vérifiez l'URL : `http://localhost:8000/api/users/token/` |
| Cannot GET request | Serveur pas démarré | Exécutez `python manage.py runserver --noreload` |
| CORS error | Problème de domaine | Vérifiez `CORS_ALLOWED_ORIGINS` dans `settings.py` |

---

## 📝 Notes

- Les tokens JWT expirent après un certain temps
- Pour rafraîchir le token, utilisez le endpoint `Refresh Token`
- Les mots de passe temporaires doivent être changés après la première connexion
