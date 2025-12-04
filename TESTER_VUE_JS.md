# 🚀 COMMENT TESTER L'APPLICATION VUE.JS

## 📌 Méthode 1: Ouvrir le fichier directement (Plus simple!)

### Étape 1: Ouvrir le fichier
```
Cliquer sur: frontend/index.html
Puis: "Ouvrir avec" → Navigateur (Chrome, Firefox, Edge, etc.)
```

OU dans l'explorateur Windows:
```
Double-cliquer sur: index.html
```

### Étape 2: Se connecter
```
Username: admin
Password: admin123456
Cliquer sur "Se connecter"
```

### Étape 3: Voir le dashboard
✅ Tableau de bord chargé automatiquement !

---

## 📌 Méthode 2: Avec un serveur local (Recommandé)

### Si vous avez Python:

```powershell
# Terminal PowerShell
cd "c:\Users\Lenovo Yoga 6\Desktop\semestre 2\python\samacahier\frontend"
python -m http.server 3000
```

Puis ouvrir: **http://localhost:3000**

### Si vous avez Node.js:

```powershell
npx http-server -p 3000
```

Puis ouvrir: **http://localhost:3000**

---

## 🎯 Flux de connexion

```
┌─────────────────────────────────────┐
│   Ouvrir frontend/index.html        │
└──────────────┬──────────────────────┘
               │
               ▼
    ┌──────────────────────────┐
    │   Page de connexion      │
    │   ┌────────────────────┐ │
    │   │ Username: _______  │ │
    │   │ Password: _______  │ │
    │   │ [Se connecter]     │ │
    │   └────────────────────┘ │
    └──────────────┬───────────┘
                   │
        Entrer: admin / admin123456
                   │
                   ▼
        ┌──────────────────────────┐
        │ Appel API:               │
        │ POST /api/users/token/   │
        └──────────────┬───────────┘
                       │
                       ▼
            ✅ Token reçu
            Sauvegarder localStorage
                       │
                       ▼
        ┌──────────────────────────┐
        │   Tableau de Bord        │
        │                          │
        │ Pour Boutiquier:         │
        │ - Statistiques           │
        │ - Liste des crédits      │
        │                          │
        │ Pour Client:             │
        │ - Ses crédits            │
        └──────────────────────────┘
```

---

## 🔐 Points clés de la connexion

### 1️⃣ Identifiant
```javascript
POST http://localhost:8000/api/users/token/

Données envoyées:
{
  "username": "admin",
  "password": "admin123456"
}

Réponse reçue:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "username": "admin",
  "email": "admin@example.com",
  "role": "boutiquier",
  "first_name": "Admin"
}
```

### 2️⃣ Stockage du Token
```javascript
Le token est sauvegardé dans localStorage:
localStorage.setItem('token', access_token)

À chaque requête suivante, le token est utilisé:
Authorization: Bearer {token}
```

### 3️⃣ Chargement des données
```javascript
Selon le rôle:

Si Boutiquier:
  - GET /api/dashboard/boutiquier/
  - GET /api/credits/credits/

Si Client:
  - GET /api/dashboard/client/
```

---

## 🎨 Interface de connexion

L'interface montre:

```
┌─────────────────────────────────┐
│      🏪 SamaCahier              │
│   Gestion des Crédits           │
│                                 │
│  [×] Erreur / [✓] Succès        │
│                                 │
│  👤 Nom d'utilisateur           │
│  [_______________]              │
│                                 │
│  🔑 Mot de passe                │
│  [_______________]              │
│                                 │
│  [Se connecter]                 │
│                                 │
│  Compte de test :               │
│  Username: admin                │
│  Password: admin123456          │
└─────────────────────────────────┘
```

---

## 📊 Dashboard après connexion

### Pour Boutiquier:

```
┌──────────────────────────────────┐
│ 📊 Tableau de bord               │
│ Bienvenue Admin                  │
│                        Déconnexion│
├──────────────────────────────────┤
│ 📈 Statistiques                  │
│ ┌─────────┬─────────┬─────────┬──┐
│ │ Clients │ Crédits │ Total   │Payé
│ │    5    │   10    │ 500 000 │...
│ └─────────┴─────────┴─────────┴──┘
│                                  │
│ 💳 Mes Crédits                   │
│ ┌────────────────────────────────┐
│ │ Mamadou Traoré        [Partial]│
│ │ 50,000 | Payé: 25,000          │
│ │ [████████░░░░░░░░░] 50%        │
│ │ Échéance: 15 décembre 2025     │
│ └────────────────────────────────┘
│                                  │
│ Crédit 2, 3, 4...               │
└──────────────────────────────────┘
```

### Pour Client:

```
┌──────────────────────────────────┐
│ 📊 Tableau de bord               │
│ Bienvenue Mamadou               │
│                        Déconnexion│
├──────────────────────────────────┤
│ 💳 Mes Crédits                   │
│ ┌─────────┬─────────┬─────────┐  │
│ │Total Dû │  Payé   │ Restant │  │
│ │ 50,000  │ 25,000  │ 25,000  │  │
│ └─────────┴─────────┴─────────┘  │
│                                  │
│ Crédit 1 - Chez Admin [Partial]  │
│ 50,000 | Payé: 25,000           │
│ [████████░░░░░░░░░] 50%         │
│ Échéance: 15 décembre 2025      │
│                                  │
│ Crédit 2 (si plusieurs)         │
└──────────────────────────────────┘
```

---

## 🌈 Couleurs des statuts

```
Pending (En attente)  → 🟡 Jaune
Partial (Partiel)     → 🔵 Bleu
Paid (Payé)           → 🟢 Vert
Overdue (En retard)   → 🔴 Rouge
```

---

## ⚙️ Configuration requise

### Serveur Django doit tourner:
```powershell
http://localhost:8000
```

### CORS configuré pour:
```
http://localhost:3000
http://127.0.0.1:3000
file:///
```

### Navigateur moderne (tous supportent Vue.js 3):
```
✅ Chrome 51+
✅ Firefox 54+
✅ Safari 10+
✅ Edge 15+
```

---

## 🔧 Résolution des problèmes

### "Erreur de connexion" ou "Network Error"
❌ Django ne tourne pas
✅ Lancer: `python manage.py runserver`

### "Erreur CORS"
❌ Les domaines ne sont pas autorisés
✅ Vérifier settings.py CORS_ALLOWED_ORIGINS

### "Aucun crédit n'apparaît"
❌ Pas de crédits créés
✅ Créer des crédits via Postman d'abord

### "Le token a expiré"
❌ Token expiré après 60 minutes
✅ Se reconnecter

---

## 📱 Responsive Design

L'application s'adapte automatiquement:

```
PC (1200px+)      : 4 colonnes pour les stats
Tablette          : 2 colonnes
Mobile (<600px)   : 1 colonne
```

Testez en redimensionnant la fenêtre!

---

## ✨ Fonctionnalités visibles

- ✅ Connexion/Déconnexion
- ✅ Affichage des crédits
- ✅ Barre de progression (% payé)
- ✅ Statuts avec badges colorés
- ✅ Formatage des devises (XOF)
- ✅ Formatage des dates (français)
- ✅ Messages d'erreur/succès
- ✅ Loading state pendant la connexion
- ✅ Responsive design

---

## 🎓 Prochaines étapes

Après avoir testé la connexion, vous pourrez:

1. **Créer des clients** via Postman
2. **Ajouter des crédits** pour les clients
3. **Enregistrer des paiements**
4. **Voir les statistiques** en temps réel

Tout sera automatiquement mis à jour dans le dashboard !

---

**Bon test ! 🚀**
