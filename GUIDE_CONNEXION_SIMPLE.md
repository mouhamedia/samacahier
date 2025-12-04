# ✅ GUIDE DE CONNEXION - BOUTIQUIERS

## 🎯 OBJECTIF
Connecter les boutiquiers et les utilisateurs au système SamaCahier

## 📋 COMPTES CRÉÉS

Tous les comptes sont créés et ont des mots de passe :

```
1. admin
   - Email: admin@example.com
   - Mot de passe: temp_admin_1

2. mouhamed365@gmail.com
   - Email: mouhamed365@gmail.com
   - Mot de passe: temp_mouhamed365@gmail.com_2

3. pole45@gmail.com
   - Email: pole45@gmail.com
   - Mot de passe: temp_pole45@gmail.com_3

4. boutiquier1@test.com
   - Email: boutiquier1@test.com
   - Mot de passe: temp_boutiquier1@test.com_4

5. MOMO@gmail.com
   - Email: bob@gmail.com
   - Mot de passe: temp_MOMO@gmail.com_6
```

## 🚀 DÉMARRER LE SERVEUR

**Option 1 : Double-cliquez sur le fichier batch (Windows)**
```
start_server.bat
```

**Option 2 : Ligne de commande (Windows PowerShell)**
```powershell
cd "c:\Users\Lenovo Yoga 6\Desktop\semestre 2\python\samacahier"
python manage.py runserver --noreload 8000
```

**Option 3 : Ligne de commande (CMD)**
```cmd
cd c:\Users\Lenovo Yoga 6\Desktop\semestre 2\python\samacahier
python manage.py runserver --noreload 8000
```

## 🌐 ACCÉDER À L'APPLICATION

Une fois le serveur démarré, ouvrez votre navigateur et allez à :

```
http://localhost:8000/frontend/
```

## 🔐 SE CONNECTER

1. Ouvrez http://localhost:8000/frontend/
2. Entrez votre **nom d'utilisateur** (ex: admin ou mouhamed365@gmail.com)
3. Entrez votre **mot de passe** (voir liste ci-dessus)
4. Cliquez sur **Connexion**

## ✅ VÉRIFIER QUE ÇA MARCHE

Les messages qui doivent s'afficher :

- ✅ Connecté avec succès
- ✅ Le dashboard s'affiche
- ✅ Vous voyez les onglets (Boutiquiers, Clients, Crédits)

## ❌ SI ERREUR "Identifiants incorrects"

1. Vérifiez que vous utilisez le **bon nom d'utilisateur** (pas l'email forcément)
2. Vérifiez que le **mot de passe est exact** (sensible à la casse)
3. Attendez 3 secondes après avoir démarré le serveur

## 📝 NOTES

- Les mots de passe sont **temporaires**
- Vous pouvez les changer après connexion
- Les comptes sont créés dans la **base de données SQLite** (db.sqlite3)
- Le serveur écoute sur le **port 8000**

## 🆘 PROBLÈMES COURANTS

### Le serveur s'arrête immédiatement
- Assurez-vous que le port 8000 est libre
- Fermez tous les processus Python
- Redémarrez le serveur

### Erreur "Connection refused"
- Le serveur n'a pas démarré correctement
- Vérifiez qu'il n'y a pas d'erreurs en démarrant le serveur
- Attendez 5 secondes après le démarrage

### Le frontend ne charge pas
- Attendez que le serveur affiche "Starting development server"
- Rafraîchissez la page (F5)
- Videz le cache (Ctrl+Shift+Delete)

## 💡 ASTUCE

Gardez le terminal ouvert avec le serveur actif pendant que vous testez l'application. Vous verrez les logs des requêtes.
