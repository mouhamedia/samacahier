# 🔧 SOLUTION: Problème de Connexion des Boutiquiers

## ❌ Le Problème

Vous avez créé des boutiquiers via l'admin Django, mais **ils ne peuvent pas se connecter** parce que:
- **Les mots de passe n'étaient jamais définis** quand créés via l'interface admin
- Même si vous aviez défini un mot de passe via l'admin, les boutiquiers ne pouvaient le utiliser que pour Django admin, **pas pour l'API REST**

## ✅ La Solution

### Étape 1: Réinitialiser les Mots de Passe

J'ai créé un script `reset_boutiquier_passwords.py` qui:
1. **Génère un mot de passe temporaire** pour chaque boutiquier: `temp_{username}_{id}`
2. **Sauvegarde les identifiants** dans `credentials_boutiquiers.txt`
3. **Crée les hashs corrects** pour l'API REST

**Exécutez:**
```bash
python reset_boutiquier_passwords.py
```

### Étape 2: Les Identifiants Actuels

Regardez le fichier `credentials_boutiquiers.txt` créé. Vous verrez:

```
Utilisateur: pole45@gmail.com
Mot de passe temporaire: temp_pole45@gmail.com_3
```

### Étape 3: Tester la Connexion

1. **Ouvrez** http://localhost:8000/frontend/
2. **Entrez** les identifiants du fichier
3. **Cliquez** "Connexion"

🎉 Le boutiquier devrait maintenant se connecter !

## 🔑 Comment Ça Fonctionne

L'authentification Django utilise **3 couches**:

| Couche | Utilisée Pour | Mot de passe |
|--------|---------------|-------------|
| **Django Admin** | `/admin/` | Hash Django standard |
| **API REST** | `/api/users/token/` | **JWT via DRF** |
| **Frontend** | `/frontend/` | API REST JWT |

**Avant:** Les boutiquiers avaient un hash Django admin uniquement ❌
**Après:** Les boutiquiers ont un hash correct pour l'API REST ✅

## 📋 Vue.js Connexion Frontend

Le code Vue.js dans `index.html` envoie:

```javascript
POST /api/users/token/
{
    "username": "pole45@gmail.com",
    "password": "temp_pole45@gmail.com_3"
}
```

Les Django REST Framework valide le mot de passe et retourne un **JWT token**.

## 💡 Après la Première Connexion

Les boutiquiers peuvent **changer leur mot de passe** via le bouton de changement de mot de passe (à implémenter dans le dashboard boutiquier).

## 📂 Fichiers Modifiés/Créés

| Fichier | Changement |
|---------|-----------|
| `users/urls.py` | ✏️ Ajouté endpoint `/init-password/` |
| `users/views.py` | ✏️ Ajoutée fonction `initialize_boutiquier_password` |
| `reset_boutiquier_passwords.py` | ✨ **CRÉÉ** - Script de réinitialisation |
| `credentials_boutiquiers.txt` | ✨ **CRÉÉ** - Identifiants temporaires |

## 🚀 Prochaines Étapes

1. **Testez** les boutiquiers existants
2. **À l'avenir**, quand vous créez un nouvel utilisateur via l'API (`POST /api/users/`), les mots de passe sont **automatiquement hashés correctement**
3. **Ajoutez** un dashboard boutiquier pour changer le mot de passe

## ⚠️ Important

- **Ne partagez pas** le fichier `credentials_boutiquiers.txt` publiquement
- Les mots de passe temporaires doivent être **changés** après la première connexion
- Pour créer des boutiquiers à l'avenir, utilisez le dashboard admin Vue.js (`/frontend/`) au lieu de Django admin `/admin/`
