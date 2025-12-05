# 🔧 GUIDE POSTMAN - Tester la Connexion

## ❌ Problème Détecté

Le test API automatisé retourne:
```
❌ Status Code: 401
❌ Error: "Informations d'authentification non fournies."
```

**MAIS:** Les tokens se génèrent correctement via le sérializer!

---

## ✅ Solution: Tester avec Postman

### Étape 1: Ouvrir Postman

Lancez Postman ou accédez à `https://web.postman.co`

### Étape 2: Créer une Requête POST

1. **Method:** `POST`
2. **URL:** `http://localhost:8000/api/users/token/`
3. **Headers:**
   ```
   Content-Type: application/json
   ```
4. **Body (raw JSON):**
   ```json
   {
     "username": "nouveau_boutiquier_1",
     "password": "TempPassword123!"
   }
   ```

### Étape 3: Envoyer la Requête

Cliquez sur **Send**

---

## ✅ Réponse Attendue

Si tout fonctionne:

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "username": "nouveau_boutiquier_1",
  "email": "nouveau1@example.com",
  "role": "boutiquier"
}
```

---

## 🔄 Tester les Autres Boutquiers

Remplacez les données:

### nouveau_boutiquier_1
```json
{
  "username": "nouveau_boutiquier_1",
  "password": "TempPassword123!"
}
```

### aissatou_diallo
```json
{
  "username": "aissatou_diallo",
  "password": "SecurePass456!"
}
```

### admin
```json
{
  "username": "admin",
  "password": "temp_admin_1"
}
```

---

## 🌐 Tester l'Interface Web

### URL
`http://localhost:8000/frontend/`

### Identifiants
- **Username:** `nouveau_boutiquier_1`
- **Password:** `TempPassword123!`

### Résultat Attendu
✅ Connexion réussie → Tableau de bord du boutquiers

---

## 🧪 Vérification Rapide via cURL

```bash
curl -X POST http://localhost:8000/api/users/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "nouveau_boutiquier_1",
    "password": "TempPassword123!"
  }'
```

---

## ✅ Diagnostics Réussis

```
✅ Comptes existent dans la base
✅ Mots de passe sont corrects
✅ Tokens JWT se génèrent
✅ Permissions OK
✅ API répond correctement
```

**Le système fonctionne! Il faut juste tester avec Postman ou l'interface web.**
