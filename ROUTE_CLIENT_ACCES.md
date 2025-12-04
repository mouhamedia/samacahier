# 📱 NOUVELLE ROUTE - Connexion Client par Code

## Route ajoutée

### POST /api/clients/access/
**Connexion simplifiée pour les clients** (pas d'authentification requise)

```
POST http://localhost:8000/api/clients/access/
Content-Type: application/json

{
  "access_code": "ABC123"
}
```

---

## 📥 Request Body

```json
{
  "access_code": "ABC123"
}
```

**Paramètre:**
- `access_code` (string, requis) - Le code unique du client

---

## 📤 Response (200 OK)

```json
{
  "client_id": 1,
  "client_name": "Mamadou Traoré",
  "access_code": "ABC123",
  "phone": "+223 70 123 4567",
  "email": "mamadou@example.com",
  "boutiquier_name": "Admin User",
  "credits_info": {
    "total_credits": 2,
    "total_amount": 100000.00,
    "total_paid": 25000.00,
    "remaining": 75000.00,
    "credits": [
      {
        "id": 1,
        "amount": 50000.00,
        "paid_amount": 25000.00,
        "remaining": 25000.00,
        "status": "partial",
        "description": "Riz et millet",
        "due_date": "2025-12-15"
      },
      {
        "id": 2,
        "amount": 50000.00,
        "paid_amount": 0.00,
        "remaining": 50000.00,
        "status": "pending",
        "description": "Sucre et huile",
        "due_date": "2025-12-20"
      }
    ]
  }
}
```

---

## ❌ Error Responses

### 400 - Code manquant
```json
{
  "error": "Le code d'accès est requis"
}
```

### 404 - Code invalide
```json
{
  "error": "Code d'accès invalide ou client inactif"
}
```

---

## 🎯 Cas d'usage

### 1. Client se connecte avec son code
```bash
curl -X POST http://localhost:8000/api/clients/access/ \
  -H "Content-Type: application/json" \
  -d '{"access_code": "ABC123"}'
```

### 2. Le client voit immédiatement:
- ✅ Son nom
- ✅ Le nom du boutiquier
- ✅ Total de ses crédits
- ✅ Montant payé / Montant restant
- ✅ Détail de chaque crédit

---

## ✨ Caractéristiques

| Caractéristique | Détail |
|---|---|
| **Authentification** | ❌ Non requise |
| **Autorisation** | ✅ Par code unique |
| **Format du code** | 3 lettres + 3 chiffres (ex: ABC123) |
| **Unicité** | ✅ Chaque client a un code unique |
| **Données retournées** | Infos client + tous ses crédits |

---

## 🔐 Sécurité

- ✅ Code unique pour chaque client
- ✅ Code difficile à deviner (format aléatoire)
- ✅ Impossible de modifier les données via cette route
- ✅ Client ne peut voir que ses propres crédits

---

## 🚀 Résumé des routes Client/Public

| Route | Méthode | Auth | Description |
|-------|---------|------|-------------|
| `/api/clients/access/` | POST | ❌ Non | Connexion par code d'accès |
| `/api/users/token/` | POST | ❌ Non | Obtenir token JWT |
| `/api/users/` | POST | ❌ Non | Créer un nouvel utilisateur |

---

## 💡 Comment utiliser dans une application mobile

### Step 1: Client ouvre l'app
```
┌─────────────────────┐
│   SAMACAHIER        │
│   Consulter Crédits │
├─────────────────────┤
│ Entrez votre code:  │
│ [____________]      │
│   [VALIDER]         │
└─────────────────────┘
```

### Step 2: Client tape son code
```
POST /api/clients/access/
{
  "access_code": "ABC123"
}
```

### Step 3: App affiche ses crédits
```
┌─────────────────────┐
│ Mamadou Traoré      │
│ Boutiquier: Admin   │
├─────────────────────┤
│ Total: 100 000 F    │
│ Payé:   25 000 F    │
│ Restant: 75 000 F   │
├─────────────────────┤
│ Crédit 1: 50k (25%) │
│ Crédit 2: 50k (0%)  │
└─────────────────────┘
```

---

**C'est tout! Pas de compte nécessaire, juste un code!** 🎉
