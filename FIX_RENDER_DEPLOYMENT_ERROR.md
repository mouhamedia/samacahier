# 🔧 FIX - RENDER DEPLOYMENT ERROR

## ❌ L'Erreur

```
ModuleNotFoundError: No module named 'app'
==> Running 'gunicorn app:app'
```

## 🔍 Cause du Problème

**Render ignore votre Procfile** et utilise sa configuration par défaut qui essaie de lancer:
```bash
gunicorn app:app  # ❌ MAUVAIS - Flask style
```

Au lieu de:
```bash
gunicorn samacahier.wsgi  # ✅ CORRECT - Django style
```

## ✅ SOLUTION

### Option 1: Via Dashboard Render (RECOMMANDÉ)

1. Allez dans votre **Web Service** Render
2. Allez à **Settings** (en haut à droite)
3. Trouvez **Start Command**
4. Remplacez par:
```bash
gunicorn samacahier.wsgi --bind 0.0.0.0:$PORT --workers 3 --timeout 60
```
5. Cliquez **Save**
6. Allez à **Deploys** → **Redeploy latest commit**

### Option 2: Via Fichiers de Configuration

Les fichiers suivants ont été ajoutés:

**`Procfile`** (mis à jour)
```
web: gunicorn samacahier.wsgi --bind 0.0.0.0:$PORT --workers 3 --timeout 60
```

**`render.yaml`** (nouveau)
```yaml
services:
  - type: web
    name: samacahier-api
    startCommand: gunicorn samacahier.wsgi --bind 0.0.0.0:$PORT
```

**`render-build.sh`** (nouveau)
```bash
#!/bin/bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

### Option 3: Configuration via Dashboard (Plus Détaillé)

1. **Web Service Settings** → **Build Command**
```bash
pip install -r requirements.txt
```

2. **Web Service Settings** → **Start Command**
```bash
gunicorn samacahier.wsgi --bind 0.0.0.0:$PORT
```

3. **Environment** → Ajouter:
```
PYTHON_VERSION=3.13
```

## 🚀 Après la Correction

1. Render relancera le déploiement automatiquement
2. Vous verrez:
```
Building your application...
✅ Build successful
Starting your application...
✅ Application is running
```

3. Votre API sera accessible:
```
https://samacahier-api.onrender.com/api/users/token/
```

## 🧪 Test après Correction

```bash
curl -X POST https://samacahier-api.onrender.com/api/users/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

Réponse attendue:
```json
{
  "access": "eyJhbGc...",
  "refresh": "eyJhbGc...",
  "username": "admin",
  "email": "admin@example.com",
  "role": "admin"
}
```

## ⚠️ Points Importants

✅ `samacahier.wsgi` = le module Django correct
✅ `--bind 0.0.0.0:$PORT` = accepte les connexions externes
✅ `--workers 3` = meilleure performance
✅ `$PORT` = variable Render (normalement 8000 ou 10000)

## 📝 Checklist Post-Fix

- [ ] Start Command changé dans Render Settings
- [ ] Application redéployée
- [ ] Logs affichent "✅ Application is running"
- [ ] Endpoint /api/users/token/ répond avec 200
- [ ] JWT token généré avec succès
- [ ] Database connectée (pas d'erreur "psycopg2")

## 🔗 Ressources Render

- Docs: https://render.com/docs/deploy-python
- Procfile: https://render.com/docs/procfile
- Troubleshooting: https://render.com/docs/troubleshooting-deploys

---

**Status**: ✅ Configuration corrigée
**Next**: Redéployer depuis Render Dashboard
**ETA**: 3-4 minutes pour que l'app soit live
