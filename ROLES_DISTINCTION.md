# 👥 RÔLES - Comment Ils Se Distinguent

## 🎯 Les 2 Rôles Principaux

```
SYSTÈME SAMACAHIER = 2 TYPES D'UTILISATEURS
│
├─ 🏪 BOUTIQUIER (Vendeur/Magasin)
│  ├─ Crée des crédits
│  ├─ Gère des clients
│  ├─ Reçoit de l'argent
│  ├─ Voit tout son tableau de bord
│  └─ Role = 'boutiquier'
│
└─ 👤 CLIENT (Emprunteur)
   ├─ Reçoit des crédits
   ├─ Emprunte de l'argent
   ├─ Rembourse progressivement
   ├─ Interface simple (ses données uniquement)
   └─ Role = 'client'
```

---

## 📊 TABLEAU COMPARATIF

| Aspect | 🏪 BOUTIQUIER | 👤 CLIENT |
|--------|--------------|----------|
| **Role DB** | `'boutiquier'` | `'client'` |
| **Fonction** | Vendeur de crédit | Emprunteur |
| **Login** | Username + Password | Code d'accès |
| **URL Frontend** | `/frontend/` | `/frontend/client.html` |
| **URL API** | `/api/users/token/` | `/api/clients/access/` |
| **Voir clients** | ✅ OUI | ❌ NON |
| **Voir crédits** | ✅ Tous les siens | ✅ Seulement les siens |
| **Créer crédit** | ✅ OUI | ❌ NON |
| **Payer** | ✅ Gérer paiements | ✅ Payer ses dettes |
| **Dashboard** | ✅ Complet (stats + table) | ✅ Simple (ses infos) |
| **Données privées** | Toutes ses données | Ses données uniquement |

---

## 🏪 BOUTIQUIER EN DÉTAIL

### Définition
```
Propriétaire d'un magasin qui:
- Prête de l'argent aux clients
- Gère la liste de ses clients
- Reçoit les paiements
- Analyse ses chiffres
```

### Accès
```
✅ PEUT VOIR:
   ├─ Tous ses clients
   ├─ Tous ses crédits
   ├─ Tous les paiements reçus
   ├─ Son tableau de bord
   └─ Ses statistiques

❌ NE PEUT PAS VOIR:
   ├─ Clients d'autres boutquiers
   ├─ Crédits d'autres boutquiers
   └─ Données confidentielles
```

### Interface
```
Affiche:
├─ Statistiques (4 nombres importants):
│  ├─ Total emprunté
│  ├─ Total payé
│  ├─ Montant restant
│  └─ Crédits actifs
├─ Tableau de tous les crédits
├─ Historique complet des transactions
└─ Profil utilisateur
```

### Exemple
```
Username: nouveau_boutiquier_1
Password: TempPassword123!
Email: nouveau1@example.com
Role: 'boutiquier' ✅
Status: 'active' ✅
```

---

## 👤 CLIENT EN DÉTAIL

### Définition
```
Quelqu'un qui:
- Emprunte de l'argent
- Reçoit du crédit
- Doit rembourser
- Consulte son solde
```

### Accès
```
✅ PEUT VOIR:
   ├─ Ses crédits personnels
   ├─ L'historique de ses paiements
   ├─ Le montant à rembourser
   └─ Son profil

❌ NE PEUT PAS VOIR:
   ├─ Crédits d'autres clients
   ├─ Autres clients
   ├─ Données du boutquier
   └─ Tableau de bord complet
```

### Interface
```
Affiche:
├─ Section "Mes Crédits"
│  ├─ Liste de ses crédits
│  ├─ Montant emprunté
│  ├─ Montant payé
│  └─ Montant restant
├─ Historique des transactions
├─ Bouton "Effectuer un paiement"
└─ Profil personnel
```

### Exemple
```
Login Code: 2F4EB4E4 (accès permanent)
Email: marie@gmail.com
Role: 'client' ✅
Status: 'active' ✅
```

---

## 🔑 COMMENT LE SYSTÈME DISTINGUE

### 1️⃣ BASE DE DONNÉES
```python
# Tous les utilisateurs ont un champ 'role'
User.role = 'boutiquier'  ← Boutquier
User.role = 'client'      ← Client
```

### 2️⃣ PERMISSIONS (Vérification au Login)
```python
# Permission pour boutquiers
class IsBoutiquier(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'boutiquier'

# Permission pour clients
class IsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'client'
```

### 3️⃣ ENDPOINTS API DIFFÉRENTS

**BOUTQUIER:**
```
POST   /api/users/token/              ← Login avec username/password
GET    /api/users/profile/            ← Mon profil
GET    /api/users/my-credits/         ← Tous mes crédits
GET    /api/users/transactions/       ← Tous mes paiements
```

**CLIENT:**
```
POST   /api/clients/access/           ← Login avec code d'accès
GET    /api/clients/my-credits/       ← Mes crédits
GET    /api/clients/transactions/     ← Mes paiements
POST   /api/clients/pay/              ← Effectuer un paiement
```

### 4️⃣ INTERFACES WEB DIFFÉRENTES

**BOUTQUIER:**
```
URL: http://localhost:8000/frontend/
Affiche: Tableau de bord complet
```

**CLIENT:**
```
URL: http://localhost:8000/frontend/client.html
Affiche: Interface simple et personnelle
```

---

## 🔐 VÉRIFICATION DANS LE CODE

### Python (Backend)
```python
# Vérifier le rôle
if request.user.role == 'boutiquier':
    return Response({'dashboard': get_boutquier_dashboard()})
elif request.user.role == 'client':
    return Response({'credits': get_client_credits()})
```

### JavaScript (Frontend)
```javascript
// Après login
const token = response.data.access;
const decoded = jwt_decode(token);

if (decoded.role === 'boutiquier') {
    showBoutquierUI();  // Affiche /frontend/
} else if (decoded.role === 'client') {
    showClientUI();     // Affiche /frontend/client.html
}
```

---

## 💡 RÉSUMÉ SIMPLE

```
🏪 BOUTIQUIER
   ↓
   Username + Password
   ↓
   Voit TOUT (ses clients, crédits, paiements)
   ↓
   Tableau de bord complet

👤 CLIENT
   ↓
   Code d'accès permanent
   ↓
   Voit SEULEMENT ses données
   ↓
   Interface simple
```

---

**Les 2 rôles donnent des accès COMPLÈTEMENT DIFFÉRENTS! 🎯**
