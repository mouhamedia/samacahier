# 🖥️ Application Vue.js - SamaCahier

## 📋 Description

Application web simple et moderne en **Vue.js 3** pour :
- ✅ Connexion utilisateur (Boutiquier & Client)
- ✅ Tableau de bord Boutiquier avec statistiques
- ✅ Gestion et suivi des crédits
- ✅ Tableau de bord Client pour voir ses crédits

---

## 🚀 Démarrage

### **Option 1: Fichier local (Plus simple)**

1. Ouvrir le fichier `frontend/index.html` directement dans le navigateur
2. Utiliser les identifiants de test :
   ```
   Username: admin
   Password: admin123456
   ```

### **Option 2: Avec serveur (Recommandé)**

```powershell
# Aller dans le dossier frontend
cd "c:\Users\Lenovo Yoga 6\Desktop\semestre 2\python\samacahier\frontend"

# Lancer un serveur simple
python -m http.server 3000
```

Puis ouvrir : `http://localhost:3000`

---

## 🔐 Connexion

### Étape 1: Page de Connexion
```
Entrer votre username et password
Cliquer sur "Se connecter"
```

### Étape 2: Tableau de Bord
Après connexion, vous verrez :
- **Boutiquier**: Statistiques + Tous ses crédits
- **Client**: Ses crédits personnels

---

## 📊 Fonctionnalités

### 👔 **Pour les Boutiquiers**

#### Vue d'ensemble
```
📈 4 statistiques principales:
  - Total Clients
  - Total Crédits
  - Montant Total
  - Montant Payé
```

#### Gestion des crédits
```
Pour chaque crédit:
  - Nom du client
  - Montant total & payé
  - Montant restant
  - Statut (pending, partial, paid, overdue)
  - Barre de progression
  - Date d'échéance
  - Description
  - Nombre de paiements
```

### 👥 **Pour les Clients**

#### Vue personnelle
```
📊 3 statistiques:
  - Total Dû
  - Montant Payé
  - Montant Restant
```

#### Liste des crédits
```
Pour chaque crédit:
  - Nom du boutiquier
  - Montant & progression
  - Statut du crédit
  - Date d'échéance
  - Description
```

---

## 🎨 Design & UX

### Couleurs
```
Primaire: #667eea (Violet)
Secondaire: #764ba2 (Mauve)
Succès: #3c3 (Vert)
Erreur: #c33 (Rouge)
```

### Responsive Design
```
✅ Desktop (1200px+)
✅ Tablet (768px - 1200px)
✅ Mobile (< 768px)
```

### Fonctionnalités UX
```
✨ Animations fluides
✨ Statuts avec badges colorés
✨ Barre de progression pour les crédits
✨ Messages d'erreur/succès
✨ Loading state
```

---

## 📡 API Intégration

### Endpoints utilisés

```javascript
// Authentification
POST http://localhost:8000/api/users/token/
  → Récupère le token JWT

// Dashboard Boutiquier
GET http://localhost:8000/api/dashboard/boutiquier/
  → Statistiques et données

// Crédits
GET http://localhost:8000/api/credits/credits/
  → Liste des crédits

// Dashboard Client
GET http://localhost:8000/api/dashboard/client/
  → Crédits personnels
```

### Headers requis
```javascript
Authorization: Bearer {ACCESS_TOKEN}
```

---

## 🛠️ Structure du Code

### Données Vue
```javascript
data() {
  return {
    isAuthenticated: false,  // État de connexion
    user: null,              // Info utilisateur
    accessToken: '',         // Token JWT
    credits: [],             // Crédits (boutiquier)
    clientCredits: [],       // Crédits (client)
    dashboardStats: null,    // Statistiques
    loginForm: {             // Formulaire login
      username: '',
      password: ''
    }
  }
}
```

### Méthodes principales
```javascript
login()           // Authentification
logout()          // Déconnexion
loadBoutiquierData()  // Charge données boutiquier
loadClientData()      // Charge données client
formatCurrency()      // Formate les montants
formatDate()          // Formate les dates
```

---

## 🔄 Flux d'application

```
┌─────────────────────────────────────┐
│    Charger index.html               │
└──────────────┬──────────────────────┘
               │
               ▼
    ┌──────────────────────────┐
    │  Vérifier localStorage   │
    │  (token existant?)       │
    └──────────┬───────────────┘
               │
        ┌──────┴──────┐
        │             │
        ▼             ▼
    Token    Pas de token
    trouvé   
        │             │
        ▼             ▼
    Dashboard   Login Page
        │             │
        │    Entrer credentials
        │             │
        │    Cliquer "Se connecter"
        │             │
        │             ▼
        │    POST /api/users/token/
        │             │
        │    ✅ Reçoit token
        │             │
        │    Sauvegarder localStorage
        │             │
        └────────┬────┘
                 │
                 ▼
        Charger données
         (boutiquier ou client)
                 │
                 ▼
         Afficher Dashboard
```

---

## 📱 Responsive Breakpoints

```css
Desktop:     > 1200px
Tablet:      768px - 1200px
Mobile:      < 768px
```

Les grilles s'ajustent automatiquement selon la taille de l'écran.

---

## 🎯 Compte de Test

### Boutiquier
```
Username: admin
Password: admin123456
Rôle: boutiquier
```

### Créer d'autres comptes
Utiliser Postman pour créer d'autres utilisateurs :
```
POST http://localhost:8000/api/users/
{
  "username": "user123",
  "email": "user@example.com",
  "password": "password123456",
  "password_confirm": "password123456",
  "first_name": "John",
  "last_name": "Doe",
  "role": "client"
}
```

---

## 🐛 Dépannage

### Le formulaire ne fonctionne pas?
- ✅ Vérifier que le serveur Django tourne
- ✅ Vérifier l'URL : http://localhost:8000

### Erreur CORS?
```
Les headers CORS sont configurés dans settings.py
Vérifier que CORS_ALLOWED_ORIGINS inclut:
- http://localhost:3000
- http://127.0.0.1:3000
- http://localhost:8000
```

### Pas de données?
- ✅ Vérifier le token (Authorization header)
- ✅ Vérifier que l'utilisateur a les permissions
- ✅ Créer des clients/crédits via Postman d'abord

---

## 📦 Dépendances

```html
<script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
<script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
```

CDN uniquement - **Aucune installation requise !**

---

## ✨ Fonctionnalités futures possibles

- [ ] Ajouter/modifier/supprimer des crédits
- [ ] Ajouter des paiements
- [ ] Graphiques statistiques
- [ ] Export PDF
- [ ] Notifications
- [ ] Mode sombre
- [ ] Multilangue

---

## 📞 Support

Pour tester localement:
```powershell
# Terminal 1: Django
cd "c:\Users\Lenovo Yoga 6\Desktop\semestre 2\python\samacahier"
python manage.py runserver

# Terminal 2: Serveur Frontend (optionnel)
cd frontend
python -m http.server 3000
```

Puis ouvrir:
```
http://localhost:3000  (si serveur frontend)
ou
file:///C:/Users/Lenovo Yoga 6/Desktop/semestre 2/python/samacahier/frontend/index.html
```
