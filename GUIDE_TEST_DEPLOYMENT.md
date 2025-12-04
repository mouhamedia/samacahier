# 🚀 GUIDE COMPLET: TEST ET DÉPLOIEMENT

## ✅ ÉTAPE 1: VÉRIFIER QUE TOUT EST EN PLACE

```bash
# Terminal à la racine du projet:
ls -la
# Vous devez voir:
#  - manage.py
#  - samacahier/
#  - users/
#  - clients/
#  - credits/
#  - frontend/
```

---

## ✅ ÉTAPE 2: DÉMARRER LE SERVEUR

```bash
cd "c:\Users\Lenovo Yoga 6\Desktop\semestre 2\python\samacahier"
python manage.py runserver
```

**Résultat attendu:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

## ✅ ÉTAPE 3: TESTER L'APPLICATION

1. **Ouvrir le navigateur** et aller à: `http://localhost:8000/frontend/`
   
2. **Vue de connexion** doit s'afficher

---

## 🔐 ÉTAPE 4: TESTER LOGIN ADMIN

**Identifiants:**
- Username: `admin`
- Password: `admin123456`

**Attendu:**
- ✅ Redirection vers Panneau Administrateur
- ✅ 3 onglets: Boutiquiers, Clients, Crédits
- ✅ Bouton "Créer un Boutiquier"

---

## 🏪 ÉTAPE 5: CRÉER UN BOUTIQUIER VIA L'APP

1. Cliquer sur "➕ Créer un Boutiquier"
2. Remplir le formulaire:
   ```
   Identifiant: ali
   Email: ali@boutique.com
   Prénom: Ali
   Nom: Diallo
   Téléphone: 77 123 45 67
   Mot de passe: ali123456
   Confirmer: ali123456
   ```
3. Cliquer "Créer"

**Attendu:**
- ✅ Le boutiquier apparaît dans le tableau
- ✅ Statut: "active"
- ✅ is_active: true

---

## 🔐 ÉTAPE 6: TESTER LOGIN BOUTIQUIER

1. Déconnecter
2. Login avec:
   - Username: `ali`
   - Password: `ali123456`

**Attendu:**
- ✅ Dashboard boutiquier s'affiche

---

## 📊 ÉTAPE 7: TESTER LES ONGLETS ADMIN

### Onglet "Clients"
- Affiche tous les clients de tous les boutiquiers
- Bouton 🔒/🔓 pour activer/désactiver

### Onglet "Crédits"
- Affiche tous les crédits
- Montant, Payé, Restant
- Bouton 🔒/🔓 pour activer/désactiver

---

## 🐛 TESTS DES ENDPOINTS API

Tester avec Postman ou Thunder Client:

### 1️⃣ Authentification
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
    "access": "eyJ0eXAi...",
    "username": "admin",
    "is_superuser": true,
    "role": "admin"
}
```

### 2️⃣ Lister les Boutiquiers (Admin)
```
GET http://localhost:8000/api/admin/boutiquiers/
Headers:
  Authorization: Bearer <ACCESS_TOKEN>
```

### 3️⃣ Créer un Boutiquier via API
```
POST http://localhost:8000/api/users/
Headers:
  Authorization: Bearer <ACCESS_TOKEN>
  Content-Type: application/json
Body:
{
    "username": "fatou",
    "email": "fatou@boutique.com",
    "first_name": "Fatou",
    "last_name": "Ba",
    "phone": "77 987 65 43",
    "password": "fatou123456",
    "role": "boutiquier"
}
```

### 4️⃣ Désactiver un Boutiquier
```
PATCH http://localhost:8000/api/admin/boutiquiers/2/toggle-status/
Headers:
  Authorization: Bearer <ACCESS_TOKEN>
Body:
{
    "status": "inactive"
}
```

### 5️⃣ Lister tous les Clients
```
GET http://localhost:8000/api/clients/
Headers:
  Authorization: Bearer <ACCESS_TOKEN>
```

### 6️⃣ Lister tous les Crédits
```
GET http://localhost:8000/api/credits/
Headers:
  Authorization: Bearer <ACCESS_TOKEN>
```

---

## 🎯 CHECKLIST FINALE

- [ ] Server démarre sans erreur
- [ ] Page de login s'affiche
- [ ] Login admin fonctionne
- [ ] Dashboard admin affiche 3 onglets
- [ ] Créer un boutiquier fonctionne
- [ ] Boutiquier apparaît dans le tableau
- [ ] Lister clients fonctionne
- [ ] Lister crédits fonctionne
- [ ] Désactiver boutiquier fonctionne
- [ ] Désactiver client fonctionne
- [ ] Désactiver crédit fonctionne

---

## 🌐 APRÈS HÉBERGEMENT

Une fois hébergé:

1. **Accès au site:**
   ```
   https://votredomaine.com/frontend/
   ```

2. **Créer premiers boutiquiers:**
   - Login comme Admin
   - Onglet "Boutiquiers"
   - Créer chaque boutiquier
   - **PLUS BESOIN DE DJANGO ADMIN** ✅

3. **Boutiquiers gèrent leurs clients:**
   - Ils se connectent avec leurs identifiants
   - Créent leurs propres clients
   - Créent leurs propres crédits

4. **Clients accèdent avec code permanent:**
   - URL: `https://votredomaine.com/frontend/`
   - Enter leur code d'accès
   - Voir leurs crédits

---

## 🚨 EN CAS D'ERREUR

### Erreur: "Cannot POST /api/users/"
```
Solution: Vérifier que users/urls.py inclut l'endpoint de création
Check: GET /api/users/ doit être possible
```

### Erreur: "Cannot PATCH /api/admin/..."
```
Solution: Vérifier que samacahier/urls.py inclut:
path('api/admin/', include('users.admin_urls'))
```

### Erreur 401: "Unauthorized"
```
Solution: Vérifier le token est valide
Recreate token: POST /api/users/token/
```

### Boutiquiers ne s'affichent pas
```
Solution: Vérifier la base de données a les migrations appliquées
python manage.py migrate
```

---

## 📝 NOTES IMPORTANTES

✅ **Plus besoin de Django Admin après hébergement**
✅ **Les codes clients sont permanents (UUID)**
✅ **Soft-delete préserve les données (pas de suppression vraie)**
✅ **Admin peut tout gérer via l'app Vue.js**
✅ **Boutiquiers créent leurs propres clients directement**

---

## 🎉 RÉSULTAT FINAL

Vous avez un système complet qui:

1. ✅ Fonctionne sur localhost
2. ✅ Admin crée les boutiquiers depuis l'app
3. ✅ Boutiquiers créent leurs clients
4. ✅ Clients accèdent avec codes permanents
5. ✅ Rien n'est jamais supprimé (soft-delete)
6. ✅ **Prêt pour la production sans Django admin**

