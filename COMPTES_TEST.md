# 🔐 COMPTES DE TEST & CONFIGURATION

## 👤 Comptes Disponibles

### Admin (Superuser)
```
Username: admin
Password: admin123456
Email: admin@example.com
Role: admin (is_superuser=True)
```

**Accès à:**
- Dashboard Admin (créer boutiquiers)
- Voir tous les boutiquiers
- Voir tous les clients
- Voir tous les crédits
- Gérer les statuts

### Boutiquier (Test)
```
Username: ali
Password: ali123456
Email: ali@boutique.com
First Name: Ali
Last Name: Diallo
Phone: 77 123 45 67
Role: boutiquier
```

**Accès à:**
- Dashboard Boutiquier
- Ses clients
- Ses crédits
- Ajouter clients
- Ajouter crédits

---

## 🔑 Créer des Nouveaux Comptes

### Via l'App (Recommandé)
1. Login comme admin
2. Onglet "Boutiquiers"
3. Cliquer "Créer un Boutiquier"
4. Remplir le formulaire
5. Cliquer "Créer"

**Exemple:**
```
Identifiant: fatou
Email: fatou@boutique.com
Prénom: Fatou
Nom: Ba
Téléphone: 77 999 88 77
Mot de passe: fatou123456
Confirmer: fatou123456
```

### Via Terminal (Dev Only)
```bash
# 1. Lancer Django shell
python manage.py shell

# 2. Créer un utilisateur
from users.models import CustomUser
CustomUser.objects.create_user(
    username='newuser',
    email='newuser@test.com',
    password='newpass123456',
    first_name='New',
    last_name='User',
    phone='77 123 45 67',
    role='boutiquier'
)

# 3. Vérifier
CustomUser.objects.filter(username='newuser').values()
```

### Via Django Admin
```bash
# 1. Aller à
http://localhost:8000/admin/

# 2. Login avec admin/admin123456

# 3. Users → Add User

# 4. Remplir formulaire
```

---

## 📱 Tester avec Différents Comptes

### Scénario 1: Admin Crée Boutiquiers
```
1. Login: admin / admin123456
2. Dashboard Admin
3. Créer plusieurs boutiquiers
4. Voir dans tableau
5. Déconnectez-vous
```

### Scénario 2: Boutiquier Gère Ses Clients
```
1. Login: ali / ali123456
2. Dashboard Boutiquier
3. Créer clients
4. Créer crédits
5. Voir statistiques
```

### Scénario 3: Client Voit Ses Crédits
```
1. Accès client: Enter code
2. Dashboard Client
3. Voir ses crédits
4. Voir montants dus/payés
```

---

## 🔑 Comptes API

### Authentification Complète

```bash
# 1. Obtenir token
curl -X POST http://localhost:8000/api/users/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123456"}'

# Réponse:
{
  "access": "eyJ0eXAi...",
  "refresh": "eyJ0eXAi...",
  "username": "admin",
  "email": "admin@example.com",
  "is_superuser": true
}

# 2. Utiliser le token
curl http://localhost:8000/api/admin/boutiquiers/ \
  -H "Authorization: Bearer eyJ0eXAi..."
```

---

## 🧪 Test Scenarios

### Scénario 1: Create Boutiquier Flow
```
Step 1: Login Admin
  POST /api/users/token/
  username: admin, password: admin123456
  Response: access token

Step 2: List Boutiquiers
  GET /api/admin/boutiquiers/
  Headers: Authorization Bearer <token>
  Response: [ { "id": 1, "username": "admin", ... } ]

Step 3: Create Boutiquier
  POST /api/users/
  Headers: Authorization Bearer <token>
  Body: {
    "username": "newbout",
    "email": "newbout@test.com",
    "first_name": "New",
    "last_name": "Bout",
    "phone": "77 123 45 67",
    "password": "test123456",
    "role": "boutiquier"
  }
  Response: { "id": 2, "username": "newbout", ... }

Step 4: Verify
  GET /api/admin/boutiquiers/
  Response: [ admin record, newbout record ]
```

### Scénario 2: Toggle Status Flow
```
Step 1: Get Boutiquiers
  GET /api/admin/boutiquiers/
  Response: [ { "id": 2, "is_active": true, "status": "active" } ]

Step 2: Toggle Status
  PATCH /api/admin/boutiquiers/2/toggle-status/
  Body: { "status": "inactive" }
  Response: { "id": 2, "is_active": false, "status": "inactive" }

Step 3: Verify
  GET /api/admin/boutiquiers/2/
  Response: { "id": 2, "is_active": false }
```

### Scénario 3: List All Clients
```
Step 1: Get Token (as admin)
  POST /api/users/token/
  Response: access token

Step 2: List Clients
  GET /api/clients/
  Headers: Authorization Bearer <token>
  Response: [ { client1 }, { client2 }, ... ]
```

### Scénario 4: List All Credits
```
Step 1: Get Token
  POST /api/users/token/

Step 2: List Credits
  GET /api/credits/
  Headers: Authorization Bearer <token>
  Response: [ { credit1 }, { credit2 }, ... ]
```

---

## 🗄️ Database Test Data

### Voir les Données dans SQLite

```bash
# 1. Ouvrir SQLite shell
python manage.py shell

# 2. Voir les utilisateurs
from users.models import CustomUser
print(CustomUser.objects.all().values())

# 3. Voir les clients
from clients.models import Client
print(Client.objects.all().values())

# 4. Voir les crédits
from credits.models import Credit
print(Credit.objects.all().values())

# 5. Quitter
exit()
```

### Voir les Données via Django Admin

```
1. Go to: http://localhost:8000/admin/
2. Login: admin / admin123456
3. Users → Voir tous les utilisateurs
4. Clients → Voir tous les clients
5. Credits → Voir tous les crédits
```

---

## 🔄 Réinitialiser la Base de Données

### Flush Database (Efface tout!)
```bash
# ⚠️ ATTENTION: Cela efface TOUTES les données!

python manage.py flush

# Confirmez: type "yes"

# Puis remigrez:
python manage.py migrate

# Créer nouveau superuser si nécessaire:
python manage.py createsuperuser
```

### Backup Database
```bash
# Créer une sauvegarde
python manage.py dumpdata > backup.json

# Restaurer une sauvegarde
python manage.py flush
python manage.py loaddata backup.json
```

---

## 🛡️ Sécurité Test

### Vérifier Permissions

```bash
# Test 1: Access as Client (should fail)
curl http://localhost:8000/api/admin/boutiquiers/
# Response: 401 Unauthorized

# Test 2: Access with Bad Token
curl http://localhost:8000/api/admin/boutiquiers/ \
  -H "Authorization: Bearer badtoken"
# Response: 401 Unauthorized

# Test 3: Access with Expired Token
# (After token expiration)
# Response: 401 Unauthorized
```

### Password Security
```bash
# Passwords are hashed
# Never send password in requests after login
# Use tokens for authentication

# Example: Never do this after login
curl -u admin:admin123456 http://localhost:8000/api/admin/boutiquiers/

# Always do this instead
curl http://localhost:8000/api/admin/boutiquiers/ \
  -H "Authorization: Bearer <token>"
```

---

## 📊 Performance Test

### Load Testing
```bash
# Install locust
pip install locust

# Create locustfile.py
# Run tests
locust -f locustfile.py -u 100 -r 10 -t 5m
```

---

## ✅ Validation Checklist

- [ ] Admin account works
- [ ] Boutiquier account works
- [ ] Create new user via app works
- [ ] API endpoints respond correctly
- [ ] Tokens are generated correctly
- [ ] Database contains correct data
- [ ] Permissions are enforced
- [ ] Soft-delete works
- [ ] Statuses toggle correctly
- [ ] No data is actually deleted

---

## 🎯 Comptes pour Différents Cas

### Dev Testing
```
admin / admin123456
ali / ali123456
```

### Production Deployment
```
Create new admin via:
python manage.py createsuperuser

Create boutiquiers via app dashboard
(Never use terminal or Django admin)
```

### Client Access
```
Each client gets unique UUID code
Example: 550e8400-e29b-41d4-a716-446655440000
```

---

## 📝 Notes Importantes

- ✅ Mots de passe min 8 caractères
- ✅ Usernames doivent être uniques
- ✅ Emails doivent être uniques
- ✅ Tokens expirent (JWT_ACCESS_TOKEN_LIFETIME)
- ✅ Aucun compte n'est supprimé réellement (soft-delete)
- ✅ Tous les changements sont enregistrés

---

## 🔄 Cycle Complet

### Jour 1: Développement
```
1. Use admin/admin123456
2. Create test boutiquiers
3. Test dashboards
4. Verify API endpoints
```

### Jour 2: Testing
```
1. Create additional test accounts
2. Run full test scenarios
3. Verify data persistence
4. Check responsive design
```

### Jour 3: Deployment Prep
```
1. Review database backup
2. Check all endpoints
3. Verify security
4. Prepare production credentials
```

---

**Vous êtes maintenant prêt à tester SamaCahier! 🚀**

