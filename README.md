# SamaCahier - API REST de gestion des crédits

Plateforme complète pour la gestion des crédits entre boutiquiers et clients.

## Structure du projet

```
SamaCahier/
├── samacahier/                 # Configuration principale Django
│   ├── __init__.py
│   ├── settings.py             # Réglages Django
│   ├── urls.py                 # Routes principales
│   ├── wsgi.py                 # Configuration WSGI
│   └── asgi.py                 # Configuration ASGI
│
├── users/                      # Authentification et gestion des utilisateurs
│   ├── models.py               # CustomUser (boutiquier / client)
│   ├── views.py                # Endpoints d'authentification
│   ├── urls.py                 # Routes utilisateurs
│   ├── serializers.py          # Sérializeurs DRF
│   ├── permissions.py          # Permissions personnalisées
│   └── admin.py                # Interface admin
│
├── clients/                    # Gestion des clients créés par les boutiquiers
│   ├── models.py               # Modèle Client
│   ├── views.py                # CRUD des clients
│   ├── urls.py                 # Routes clients
│   ├── serializers.py          # Sérializeurs
│   └── admin.py                # Interface admin
│
├── credits/                    # Gestion des crédits et paiements
│   ├── models.py               # Modèles Credit et Payment
│   ├── views.py                # CRUD des crédits et paiements
│   ├── urls.py                 # Routes crédits
│   ├── serializers.py          # Sérializeurs
│   └── admin.py                # Interface admin
│
├── dashboard/                  # Tableaux de bord et statistiques
│   ├── views.py                # Vues de statistiques
│   ├── urls.py                 # Routes dashboard
│   └── admin.py                # Interface admin
│
├── config/                     # Configuration centralisée
│   ├── __init__.py
│   └── env.py                  # Gestion des variables d'environnement
│
├── manage.py                   # Script de gestion Django
├── requirements.txt            # Dépendances Python
├── .env.example                # Template pour les variables d'environnement
└── README.md                   # Ce fichier
```

## Installation

### 1. Cloner et configurer l'environnement

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configurer les variables d'environnement

```bash
# Copier le fichier template
copy .env.example .env

# Éditer .env avec vos paramètres (notamment DB)
```

### 4. Exécuter les migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Créer un superutilisateur

```bash
python manage.py createsuperuser
```

### 6. Lancer le serveur

```bash
python manage.py runserver
```

L'application sera disponible à `http://localhost:8000`

## API Endpoints

### Authentification
- `POST /api/users/token/` - Obtenir un token JWT
- `POST /api/users/token/refresh/` - Rafraîchir le token
- `POST /api/users/` - Créer un nouvel utilisateur

### Utilisateurs
- `GET /api/users/` - Lister les utilisateurs
- `GET /api/users/me/` - Récupérer l'utilisateur connecté
- `PUT /api/users/{id}/` - Modifier un utilisateur
- `POST /api/users/change_password/` - Changer le mot de passe

### Clients (Boutiquier uniquement)
- `GET /api/clients/` - Lister ses clients
- `POST /api/clients/` - Créer un nouveau client
- `PUT /api/clients/{id}/` - Modifier un client
- `DELETE /api/clients/{id}/` - Supprimer un client
- `GET /api/clients/my_clients/` - Tous les clients

### Crédits (Boutiquier)
- `GET /api/credits/credits/` - Lister les crédits
- `POST /api/credits/credits/` - Créer un crédit
- `GET /api/credits/credits/stats/` - Statistiques des crédits
- `POST /api/credits/credits/{id}/add_payment/` - Ajouter un paiement
- `GET /api/credits/payments/` - Lister les paiements

### Dashboard
- `GET /api/dashboard/boutiquier/` - Tableau de bord boutiquier (stats globales)
- `GET /api/dashboard/client/` - Tableau de bord client (ses crédits)

## Configuration de la Base de Données

### SQLite (Développement)
Configuration par défaut, aucune configuration nécessaire.

### PostgreSQL (Production)

#### Installation de PostgreSQL
```bash
# Windows - Télécharger depuis https://www.postgresql.org/download/windows/
# Ou via chocolatey : choco install postgresql
```

#### Configuration de la DB
```bash
# Créer la base de données
createdb samacahier_db

# Créer un utilisateur (optionnel)
createuser samacahier_user
```

#### Configuration du .env
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=samacahier_db
DB_USER=samacahier_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

## Modèles de données

### CustomUser
- Hérite de `AbstractUser`
- Rôles : `client` ou `boutiquier`
- Champs supplémentaires : `phone`, `role`

### Client
- Propriétaire : Boutiquier
- Champs : name, phone, email, address, is_active

### Credit
- Client : Lien vers Client
- Montant : amount, paid_amount
- Statuts : pending, partial, paid, overdue
- Date : due_date

### Payment
- Crédit : Lien vers Credit
- Montant : amount
- Méthode : payment_method (cash, transfer, etc.)

## Permissions

- **Anonyme** : Peut s'inscrire, obtenir un token
- **Authentifié** : Peut voir son profil, changer son mot de passe
- **Boutiquier** : Accès complet clients, crédits, dashboard
- **Client** : Accès au dashboard client (ses crédits)

## Variables d'environnement

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# JWT
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440

# Application
LANGUAGE_CODE=fr-fr
TIME_ZONE=UTC
```

## Technologies utilisées

- **Django** 4.2
- **Django REST Framework** 3.14
- **JWT** (django-rest-framework-simplejwt)
- **PostgreSQL** (Production)
- **CORS** (django-cors-headers)

## Support

Pour toute question ou problème, créez une issue sur le repository.
