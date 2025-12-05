# 🚀 DÉPLOIEMENT SUR RENDER

## **ÉTAPE 1: Préparation GitHub (2 minutes)**

✅ Vos fichiers sont déjà sur GitHub:
- Repository: https://github.com/mouhamedia/samacahier
- Branch: main

✅ Fichiers ajoutés:
- `Procfile` - configuration du serveur
- `requirements.txt` - dépendances (avec gunicorn)
- `.gitignore` - fichiers à exclure

## **ÉTAPE 2: Créer Compte Render (2 minutes)**

1. Allez sur https://render.com
2. Cliquez "Sign up" → GitHub → Autorisez l'accès
3. Email de confirmation (check your email)

## **ÉTAPE 3: Créer une Nouvelle Web Service (5 minutes)**

1. Dashboard Render → "New +" → "Web Service"
2. Connecter votre repository GitHub:
   - Sélectionner: `mouhamedia/samacahier`
   - Click "Connect"
3. Configurer le service:
   - **Name**: `samacahier-api` (ou votre choix)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn samacahier.wsgi`
   - **Instance Type**: Free (gratuit!)

## **ÉTAPE 4: Créer une Base de Données PostgreSQL (5 minutes)**

1. Dashboard Render → "New +" → "PostgreSQL"
2. Configurer:
   - **Name**: `samacahier-db`
   - **Region**: (laissez par défaut)
   - **Database**: `samacahier`
   - **User**: (auto-généré)
3. Click "Create Database"
4. **IMPORTANT**: Copier la **External Database URL** (vous en aurez besoin!)

Exemple format:
```
postgresql://user:password@host:5432/samacahier
```

## **ÉTAPE 5: Configurer les Variables d'Environnement (5 minutes)**

Dans votre Web Service Render, allez à **Environment**:

Ajoutez ces variables:

```
DEBUG=False
SECRET_KEY=<générer_une_clé_sécurisée>
ALLOWED_HOSTS=samacahier-api.onrender.com,yourdomain.com
CORS_ALLOWED_ORIGINS=https://samacahier-api.onrender.com,https://yourdomain.com
DATABASE_URL=<coller_la_PostgreSQL_URL_de_Render>
```

**Pour générer SECRET_KEY**, ouvrez un terminal Python:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## **ÉTAPE 6: Déployer (1 minute)**

1. Dans Render, retournez au Web Service
2. Allez à **Deploys**
3. Click "Deploy latest commit"
4. Attendez que le déploiement finisse (~2-3 minutes)

🎉 Votre API sera accessible sur: `https://samacahier-api.onrender.com`

## **ÉTAPE 7: Vérifier le Déploiement (2 minutes)**

```bash
# Test de la connexion
curl -X POST https://samacahier-api.onrender.com/api/users/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"your_password"}'
```

## **ÉTAPE 8: Exécuter les Migrations (Important!)**

Render fournit un terminal pour exécuter des commandes:

1. Dans votre Web Service Render
2. Allez à **Shell**
3. Exécutez:
```bash
python manage.py migrate
python manage.py createsuperuser  # Optionnel - si vous voulez l'admin web
python manage.py collectstatic --noinput
```

## **ÉTAPE 9: Tester l'API (2 minutes)**

Depuis Postman ou votre navigateur:

```
URL: https://samacahier-api.onrender.com/api/users/token/
Method: POST
Headers: Content-Type: application/json
Body: {
  "username": "admin",
  "password": "your_password"
}
```

Réponse attendue:
```json
{
  "access": "eyJhbGciOiJIUzI1NiI...",
  "refresh": "eyJhbGciOiJIUzI1NiI...",
  "username": "admin",
  "email": "admin@example.com",
  "role": "admin"
}
```

## **DÉPANNAGE COURANT**

### ❌ Erreur "Application failed to start"
**Solution**: Vérifier les logs Render
- Render → Web Service → "Logs"
- Regarder l'erreur (généralement DATABASE_URL incorrect)

### ❌ Erreur "ALLOWED_HOSTS"
**Solution**: Ajouter votre domaine Render à ALLOWED_HOSTS
- Render vous donne: `samacahier-api.onrender.com`
- Ajouter cette URL à la variable d'environnement

### ❌ Migrations non appliquées
**Solution**: Exécuter via le shell Render
```bash
python manage.py migrate
```

### ❌ Database connection refused
**Solution**: 
1. Vérifier que la DATABASE_URL est correcte
2. Vérifier que la DB PostgreSQL Render est en "Available" (pas en création)
3. Attendre 30 secondes que la DB soit prête

## **COÛTS RENDER (FREE TIER)**

✅ Web Service: Gratuit (ralentit après 15 min d'inactivité)
✅ PostgreSQL: 90 jours gratuits, puis payant
❌ Après 90 jours: ~$15/mois pour DB

## **ALTERNATIVE GRATUITE - DATABASE**

Si vous voulez rester 100% gratuit après 90 jours:
- Utiliser **Railway.app** ($5/mth, meilleur rapport qualité-prix)
- Ou **PythonAnywhere** (gratuit avec limitations)

## **RÉSUMÉ TIMING TOTAL**

- Préparation: 2 min
- Créer compte Render: 2 min
- Web Service: 5 min
- Database: 5 min
- Variables: 5 min
- Déploiement: 3 min (automatique)
- Migrations: 2 min
- **TOTAL: ~25 minutes ⏱️**

Votre API sera en ligne sur:
🌐 **https://samacahier-api.onrender.com**
