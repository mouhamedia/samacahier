# ⚡ DÉMARRAGE RAPIDE - 5 MINUTES

## 🚀 Étape 1: Démarrer le Serveur

Ouvrez PowerShell dans le dossier du projet:

```powershell
cd "c:\Users\Lenovo Yoga 6\Desktop\semestre 2\python\samacahier"
python manage.py runserver
```

**Vous verrez:**
```
Starting development server at http://127.0.0.1:8000/
```

## 🌐 Étape 2: Ouvrir le Navigateur

Allez à:
```
http://localhost:8000/frontend/
```

Vous verrez la **page de login** 🎉

## 🔐 Étape 3: Se Connecter

**Comptes disponibles:**

### Admin
```
Username: admin
Password: admin123456
```

### Boutiquier (optionnel)
```
Username: ali
Password: ali123456
```

Cliquez **Se connecter**

## 🔧 Étape 4: Admin Dashboard

Vous voyez:
```
🔧 Panneau Administrateur

[👥 Boutiquiers] [👤 Clients] [💰 Crédits]

[➕ Créer un Boutiquier]

Tableau des boutiquiers...
```

## ➕ Étape 5: Créer un Boutiquier

1. Cliquez **"➕ Créer un Boutiquier"**
2. Une fenêtre s'ouvre
3. Remplissez avec:
   ```
   Identifiant: fatou
   Email: fatou@boutique.com
   Prénom: Fatou
   Nom: Ba
   Téléphone: 77 999 88 77
   Mot de passe: fatou123456
   Confirmer: fatou123456
   ```
4. Cliquez **"Créer"**

## ✅ Étape 6: Vérifier

Le boutiquier apparaît dans le tableau! 🎊

Vous voyez:
```
│ Fatou Ba │ fatou │ fatou@boutique.com │ 77 999 88 77 │ 0 │ active │ [🔒] │
```

## 🎯 Étape 7: Autres Onglets

### Onglet "Clients"
- Cliquez **[👤 Clients]**
- Voir tous les clients
- Toggle 🔒/🔓 pour désactiver

### Onglet "Crédits"
- Cliquez **[💰 Crédits]**
- Voir tous les crédits
- Montants, payés, restants
- Toggle 🔒/🔓 pour archiver

## 🚫 Étape 8: Tester la Désactivation

1. Dans onglet "Boutiquiers"
2. Cliquez le bouton **🔒 Désac** d'un boutiquier
3. Confirmez
4. Le statut passe à **inactive**
5. Cliquez **🔓 Activ** pour réactiver

## 📱 Étape 9: Test Mobile

Redimensionnez votre navigateur:
- **Desktop**: Tableaux complets
- **Tablet**: Tableaux adaptés
- **Mobile**: Scroll horizontal

L'interface s'adapte! 📱

## 🔄 Étape 10: Déconnexion

Cliquez **[Déconnexion]** en haut à droite

Vous revenez à la page de login ✅

---

## 🎓 C'est Tout!

Vous avez maintenant:
- ✅ Compris l'interface
- ✅ Créé un boutiquier
- ✅ Testé le dashboard
- ✅ Vérifié la soft-delete

---

## 🔗 Prochaines Étapes

### Pour Plus de Tests
- Voir: `GUIDE_TEST_DEPLOYMENT.md`

### Pour Comprendre l'Architecture
- Voir: `STRUCTURE_FINALISEE.md`

### Pour Déployer
- Voir: `ARRIVEE_A_DESTINATION.md`

### Pour le Code Vue.js
- Voir: `ADMIN_DASHBOARD_COMPLET.md`

---

## 🚨 Si Ça Ne Marche Pas

### "Erreur 404 - page not found"
```
Vérifier: http://localhost:8000/frontend/
Est-ce que le serveur tourne?
Voir: GUIDE_TEST_DEPLOYMENT.md → Erreurs
```

### "Erreur 401 - Unauthorized"
```
Vérifier: Avez-vous loggé?
Avez-vous les bons identifiants?
```

### "Connection refused"
```
Le serveur n'est pas démarré!
Relancez: python manage.py runserver
```

### "Aucun boutiquier ne s'affiche"
```
Ils sont peut-être dans la DB
Refreshez la page (F5)
```

---

## 💡 Astuces

### Ouvrir Devtools
```
F12 = Voir les erreurs console
Network = Voir les appels API
```

### Vider le Cache
```
Ctrl+Shift+Delete = Vider cache navigateur
Puis F5 = Recharger
```

### Vérifier le Token
```
Console JavaScript:
localStorage.getItem('token')
# Doit retourner un long token
```

### Réinitialiser la DB
```bash
# Dans PowerShell:
python manage.py flush
python manage.py migrate
# Puis recreez l'admin s'il faut
```

---

## 📊 Points de Contrôle

- [ ] Server démarre sans erreur
- [ ] Page login s'affiche
- [ ] Login fonctionne
- [ ] Dashboard s'affiche
- [ ] 3 onglets visibles
- [ ] Bouton "Créer boutiquier" visible
- [ ] Formulaire s'ouvre
- [ ] Créer boutiquier fonctionne
- [ ] Boutiquier apparaît dans tableau
- [ ] Toggle 🔒 fonctionne

---

## ✨ Résumé

**Fait:**
1. ✅ Démarré le serveur
2. ✅ Accédé à l'app
3. ✅ Loggé comme admin
4. ✅ Vu le dashboard
5. ✅ Créé un boutiquier
6. ✅ Testé les fonctionnalités

**Résultat:**
```
Vous avez une application web complète et fonctionnelle!
Prête pour localhost et production.
```

---

## 🎉 Bravo!

Vous avez complété le démarrage rapide.

**Pour la suite:**
- Lire les autres documentations
- Déployer sur un serveur
- Inviter les utilisateurs

**Bon dev! 🚀**

