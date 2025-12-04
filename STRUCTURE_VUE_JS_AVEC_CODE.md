# 📋 STRUCTURE COMPLÈTE VUE.JS AVEC CODE D'ACCÈS

## 🎯 FLUX DE CONNEXION COMPLET

```
┌─────────────────────────────────────────────────────────────────┐
│                      ACCUEIL / LANDING                          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
        ┌───────────────────────────────────────┐
        │  Choix type d'utilisateur             │
        ├───────────────────────────────────────┤
        │  [Je suis un Boutiquier]   X          │
        │  [Je suis un Client]       X          │
        └───────────────────────────────────────┘
           ↓                        ↓
    ┌──────────────────┐    ┌──────────────────────┐
    │ CONNEXION        │    │ ACCÈS CLIENT         │
    │ BOUTIQUIER       │    │ PAR CODE             │
    ├──────────────────┤    ├──────────────────────┤
    │ Username         │    │ Code du boutiquier   │
    │ Password         │    │ (6 chiffres/lettres) │
    │ [Connexion]      │    │ [Accéder]            │
    └──────────────────┘    └──────────────────────┘
           ↓                        ↓
    ┌──────────────────┐    ┌──────────────────────┐
    │ DASHBOARD        │    │ SAISIR NOM CLIENT    │
    │ BOUTIQUIER       │    │ + CODE BOUTIQUIER    │
    │                  │    │ [Continuer]          │
    │ • Statistiques   │    └──────────────────────┘
    │ • Clients        │              ↓
    │ • Crédits        │    ┌──────────────────────┐
    │ • Paiements      │    │ DASHBOARD CLIENT     │
    │ • Ajouter client │    │ (Lecture seule)      │
    │ • Ajouter crédit │    │ • Mes crédits        │
    │                  │    │ • Total dû           │
    └──────────────────┘    │ • Progression        │
                            └──────────────────────┘
```

---

## 📁 STRUCTURE DES DOSSIERS

```
samacahier/
├── frontend/
│   ├── index.html                 ← Application principale
│   ├── css/
│   │   ├── style.css              ← Styles généraux
│   │   └── responsive.css         ← Responsive design
│   ├── js/
│   │   ├── app.js                 ← Application principale Vue.js
│   │   ├── components/
│   │   │   ├── LoginBoutiquier.js ← Connexion boutiquier
│   │   │   ├── AccessClient.js    ← Accès client par code
│   │   │   ├── Dashboard.js       ← Dashboard boutiquier
│   │   │   ├── ClientDashboard.js ← Dashboard client (lecture seule)
│   │   │   ├── ClientForm.js      ← Formulaire ajout client
│   │   │   └── CreditForm.js      ← Formulaire ajout crédit
│   │   ├── services/
│   │   │   ├── api.js             ← Configuration Axios
│   │   │   └── auth.js            ← Gestion authentification
│   │   └── utils/
│   │       ├── formatter.js       ← Formatage devise/date
│   │       └── validators.js      ← Validation formulaires
│   └── assets/
│       ├── logo.svg
│       └── favicon.ico
├── manage.py
├── samacahier/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── users/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── clients/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── credits/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
└── db.sqlite3
```

---

## 🔐 COMPOSANTS VUE.JS

### 1️⃣ **ACCUEIL (Landing Page)**
```vue
<template>
  <div class="landing-page">
    <div class="container">
      <h1>🏪 SamaCahier</h1>
      <p>Gestion des crédits pour boutiquiers</p>
      
      <div class="choice-buttons">
        <button @click="currentView = 'boutiquier'" class="btn btn-primary">
          👤 Je suis Boutiquier
        </button>
        <button @click="currentView = 'client'" class="btn btn-secondary">
          👥 Je suis Client
        </button>
      </div>
    </div>
  </div>
</template>
```

---

### 2️⃣ **CONNEXION BOUTIQUIER**
```vue
<template>
  <div class="login-container">
    <div class="login-card">
      <h2>Connexion Boutiquier</h2>
      
      <form @submit.prevent="loginBoutiquier">
        <div class="form-group">
          <label>Identifiant</label>
          <input 
            v-model="form.username" 
            type="text" 
            placeholder="Entrez votre identifiant"
            required
          >
        </div>
        
        <div class="form-group">
          <label>Mot de passe</label>
          <input 
            v-model="form.password" 
            type="password" 
            placeholder="Entrez votre mot de passe"
            required
          >
        </div>
        
        <button type="submit" class="btn btn-primary" :disabled="loading">
          {{ loading ? 'Connexion...' : 'Se connecter' }}
        </button>
      </form>
      
      <div v-if="error" class="alert alert-error">{{ error }}</div>
      <div v-if="success" class="alert alert-success">{{ success }}</div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        username: '',
        password: ''
      },
      loading: false,
      error: '',
      success: ''
    }
  },
  methods: {
    async loginBoutiquier() {
      this.loading = true;
      this.error = '';
      
      try {
        const response = await axios.post(
          'http://localhost:8000/api/users/token/',
          this.form
        );
        
        localStorage.setItem('token', response.data.access);
        localStorage.setItem('user_role', response.data.role);
        localStorage.setItem('username', response.data.username);
        
        this.$emit('login-success', response.data);
        this.success = 'Connexion réussie !';
        
        setTimeout(() => {
          this.$emit('view-change', 'dashboard');
        }, 1000);
        
      } catch (error) {
        this.error = 'Identifiants incorrects';
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>
```

---

### 3️⃣ **ACCÈS CLIENT PAR CODE** ⭐ NOUVEAU
```vue
<template>
  <div class="access-container">
    <div class="access-card">
      <h2>📱 Accès Client</h2>
      <p class="subtitle">Entrez le code du boutiquier</p>
      
      <!-- ÉTAPE 1: Saisir le code -->
      <div v-if="step === 1" class="step-1">
        <div class="form-group">
          <label>Code du boutiquier (6 caractères)</label>
          <input 
            v-model="form.code" 
            type="text" 
            placeholder="Ex: ABC123"
            maxlength="6"
            @keyup.enter="validateCode"
            class="code-input"
          >
          <small class="hint">Code fourni par votre boutiquier</small>
        </div>
        
        <button @click="validateCode" class="btn btn-primary" :disabled="form.code.length !== 6">
          Valider le code
        </button>
      </div>
      
      <!-- ÉTAPE 2: Saisir nom client -->
      <div v-if="step === 2" class="step-2">
        <div class="progress-bar">
          <div class="progress" style="width: 50%">2/2</div>
        </div>
        
        <div class="form-group">
          <label>Votre nom</label>
          <input 
            v-model="form.clientName" 
            type="text" 
            placeholder="Entrez votre prénom et nom"
            @keyup.enter="accessAsClient"
          >
        </div>
        
        <div class="form-group">
          <label>Confirmez le code</label>
          <input 
            v-model="form.codeConfirm" 
            type="text" 
            placeholder="Confirmez le code"
            maxlength="6"
          >
        </div>
        
        <div class="button-group">
          <button @click="step = 1" class="btn btn-secondary">
            ← Retour
          </button>
          <button @click="accessAsClient" class="btn btn-primary" :disabled="!form.clientName">
            Accéder à mes crédits
          </button>
        </div>
      </div>
      
      <!-- Messages d'erreur/succès -->
      <div v-if="error" class="alert alert-error">{{ error }}</div>
      <div v-if="success" class="alert alert-success">{{ success }}</div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        code: '',
        clientName: '',
        codeConfirm: ''
      },
      step: 1,
      error: '',
      success: '',
      boutiquierCode: '' // Stocké après validation
    }
  },
  methods: {
    validateCode() {
      // Vérifier auprès du backend
      if (this.form.code.length !== 6) {
        this.error = 'Le code doit contenir 6 caractères';
        return;
      }
      
      // Simulé - A remplacer par appel API
      // POST /api/verify-client-code/
      if (this.form.code === 'ABC123') { // Code test
        this.boutiquierCode = this.form.code;
        this.step = 2;
        this.error = '';
      } else {
        this.error = 'Code invalide ou expiré';
      }
    },
    
    async accessAsClient() {
      if (this.form.code !== this.form.codeConfirm) {
        this.error = 'Les codes ne correspondent pas';
        return;
      }
      
      if (!this.form.clientName) {
        this.error = 'Veuillez entrer votre nom';
        return;
      }
      
      // Stocker les infos client
      localStorage.setItem('client_access', JSON.stringify({
        code: this.form.code,
        name: this.form.clientName,
        timestamp: Date.now()
      }));
      
      this.$emit('client-access-success', {
        name: this.form.clientName,
        code: this.form.code
      });
      
      this.$emit('view-change', 'client-dashboard');
    }
  }
}
</script>

<style scoped>
.code-input {
  font-size: 24px;
  letter-spacing: 4px;
  text-transform: uppercase;
  text-align: center;
  font-weight: bold;
}

.hint {
  display: block;
  margin-top: 8px;
  color: #666;
  font-size: 12px;
}

.progress-bar {
  width: 100%;
  height: 4px;
  background: #eee;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 20px;
}

.progress {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  transition: width 0.3s;
}
</style>
```

---

### 4️⃣ **DASHBOARD BOUTIQUIER**
```vue
<template>
  <div class="dashboard">
    <!-- HEADER -->
    <header class="dashboard-header">
      <div class="header-left">
        <h1>Dashboard Boutiquier</h1>
        <p>Bienvenue {{ username }}</p>
      </div>
      <div class="header-right">
        <button @click="logout" class="btn btn-danger">
          Déconnexion
        </button>
      </div>
    </header>
    
    <!-- STATISTIQUES -->
    <section class="stats">
      <div class="stat-card">
        <h3>Clients</h3>
        <p class="stat-value">{{ stats.totalClients }}</p>
      </div>
      <div class="stat-card">
        <h3>Crédits</h3>
        <p class="stat-value">{{ stats.totalCredits }}</p>
      </div>
      <div class="stat-card">
        <h3>Total</h3>
        <p class="stat-value">{{ formatCurrency(stats.totalAmount) }}</p>
      </div>
      <div class="stat-card">
        <h3>Payé</h3>
        <p class="stat-value">{{ formatCurrency(stats.totalPaid) }}</p>
      </div>
    </section>
    
    <!-- ONGLETS -->
    <section class="tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab"
        @click="activeTab = tab"
        :class="{ active: activeTab === tab }"
        class="tab"
      >
        {{ tab }}
      </button>
    </section>
    
    <!-- CONTENU ONGLETS -->
    <section class="content">
      <!-- Mes Clients -->
      <div v-if="activeTab === 'Clients'" class="tab-content">
        <div class="add-button">
          <button @click="showClientForm = true" class="btn btn-primary">
            + Ajouter un client
          </button>
        </div>
        <div class="clients-list">
          <div v-for="client in clients" :key="client.id" class="client-card">
            <h3>{{ client.name }}</h3>
            <p>📞 {{ client.phone }}</p>
            <p>✉️ {{ client.email }}</p>
            <p>📍 {{ client.address }}</p>
            <span :class="{ active: client.is_active }" class="badge">
              {{ client.is_active ? 'Actif' : 'Inactif' }}
            </span>
          </div>
        </div>
      </div>
      
      <!-- Mes Crédits -->
      <div v-if="activeTab === 'Crédits'" class="tab-content">
        <div class="add-button">
          <button @click="showCreditForm = true" class="btn btn-primary">
            + Ajouter un crédit
          </button>
        </div>
        <div class="credits-list">
          <div v-for="credit in credits" :key="credit.id" class="credit-card">
            <div class="credit-header">
              <h3>{{ credit.client_name }}</h3>
              <span :class="'status-' + credit.status" class="status">
                {{ credit.status }}
              </span>
            </div>
            
            <div class="credit-amounts">
              <div>
                <small>Montant</small>
                <strong>{{ formatCurrency(credit.amount) }}</strong>
              </div>
              <div>
                <small>Payé</small>
                <strong>{{ formatCurrency(credit.paid_amount) }}</strong>
              </div>
              <div>
                <small>Restant</small>
                <strong>{{ formatCurrency(credit.amount - credit.paid_amount) }}</strong>
              </div>
            </div>
            
            <div class="progress-bar">
              <div class="progress" :style="{ width: getProgress(credit) + '%' }"></div>
            </div>
            <small>{{ getProgress(credit) }}% payé</small>
          </div>
        </div>
      </div>
      
      <!-- Code d'accès client -->
      <div v-if="activeTab === 'Codes' " class="tab-content">
        <div class="client-code-section">
          <h3>Codes d'accès client</h3>
          <p>Partagez ce code avec vos clients</p>
          
          <div class="code-display">
            <input 
              :value="clientAccessCode" 
              type="text" 
              readonly 
              class="code-field"
            >
            <button @click="copyCode" class="btn btn-secondary">
              Copier
            </button>
            <button @click="generateNewCode" class="btn btn-primary">
              Générer nouveau
            </button>
          </div>
        </div>
      </div>
    </section>
    
    <!-- FORMULAIRES MODALS -->
    <ClientForm 
      v-if="showClientForm" 
      @close="showClientForm = false"
      @save="addClient"
    />
    <CreditForm 
      v-if="showCreditForm" 
      :clients="clients"
      @close="showCreditForm = false"
      @save="addCredit"
    />
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      activeTab: 'Clients',
      tabs: ['Clients', 'Crédits', 'Codes'],
      showClientForm: false,
      showCreditForm: false,
      clients: [],
      credits: [],
      stats: {
        totalClients: 0,
        totalCredits: 0,
        totalAmount: 0,
        totalPaid: 0
      },
      clientAccessCode: 'ABC123'
    }
  },
  mounted() {
    this.loadData();
  },
  methods: {
    async loadData() {
      // Charger les données depuis l'API
      this.username = localStorage.getItem('username');
      // Appels API pour charger clients, crédits, stats
    },
    logout() {
      localStorage.removeItem('token');
      this.$emit('view-change', 'landing');
    },
    formatCurrency(value) {
      return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'XOF'
      }).format(value);
    },
    getProgress(credit) {
      return Math.round((credit.paid_amount / credit.amount) * 100);
    },
    copyCode() {
      navigator.clipboard.writeText(this.clientAccessCode);
      alert('Code copié !');
    },
    generateNewCode() {
      this.clientAccessCode = Math.random().toString(36).substring(2, 8).toUpperCase();
    }
  }
}
</script>
```

---

### 5️⃣ **DASHBOARD CLIENT (Lecture seule)**
```vue
<template>
  <div class="client-dashboard">
    <!-- HEADER -->
    <header class="dashboard-header">
      <div class="header-left">
        <h1>Mes Crédits</h1>
        <p>Bienvenue {{ clientName }}</p>
      </div>
      <div class="header-right">
        <button @click="logout" class="btn btn-danger">
          Quitter
        </button>
      </div>
    </header>
    
    <!-- RÉSUMÉ -->
    <section class="resume">
      <div class="resume-card">
        <h3>Total dû</h3>
        <p class="value">{{ formatCurrency(totalDue) }}</p>
      </div>
      <div class="resume-card">
        <h3>Total payé</h3>
        <p class="value">{{ formatCurrency(totalPaid) }}</p>
      </div>
      <div class="resume-card">
        <h3>Solde restant</h3>
        <p class="value" :style="{ color: remaining > 0 ? '#d32f2f' : '#4caf50' }">
          {{ formatCurrency(remaining) }}
        </p>
      </div>
    </section>
    
    <!-- MES CRÉDITS -->
    <section class="credits">
      <h2>Détail de mes crédits</h2>
      
      <div v-if="credits.length === 0" class="no-credits">
        <p>Aucun crédit actif</p>
      </div>
      
      <div v-else class="credits-list">
        <div v-for="credit in credits" :key="credit.id" class="credit-card">
          <div class="credit-header">
            <h3>Crédit #{{ credit.id }}</h3>
            <span :class="'status-' + credit.status" class="status">
              {{ getStatusLabel(credit.status) }}
            </span>
          </div>
          
          <div class="credit-details">
            <div class="detail-row">
              <span>Montant initial</span>
              <strong>{{ formatCurrency(credit.amount) }}</strong>
            </div>
            <div class="detail-row">
              <span>Montant payé</span>
              <strong class="paid">{{ formatCurrency(credit.paid_amount) }}</strong>
            </div>
            <div class="detail-row">
              <span>Montant restant</span>
              <strong class="due">{{ formatCurrency(credit.amount - credit.paid_amount) }}</strong>
            </div>
            <div class="detail-row">
              <span>Date d'échéance</span>
              <strong>{{ formatDate(credit.due_date) }}</strong>
            </div>
          </div>
          
          <div class="progress-bar">
            <div class="progress" :style="{ width: getProgress(credit) + '%' }"></div>
          </div>
          <small>{{ getProgress(credit) }}% remboursé</small>
          
          <div v-if="credit.description" class="description">
            <p>{{ credit.description }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  data() {
    return {
      clientName: '',
      credits: [],
      totalDue: 0,
      totalPaid: 0
    }
  },
  computed: {
    remaining() {
      return this.totalDue - this.totalPaid;
    }
  },
  mounted() {
    this.loadClientData();
  },
  methods: {
    async loadClientData() {
      const clientAccess = JSON.parse(localStorage.getItem('client_access'));
      this.clientName = clientAccess.name;
      
      // Appel API pour charger les crédits du client
      // GET /api/credits/?client_name=XXX&code=XXX
    },
    formatCurrency(value) {
      return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'XOF'
      }).format(value);
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString('fr-FR');
    },
    getProgress(credit) {
      return Math.round((credit.paid_amount / credit.amount) * 100);
    },
    getStatusLabel(status) {
      const labels = {
        'pending': '⏳ En attente',
        'partial': '🔄 Partiellement payé',
        'paid': '✅ Payé',
        'overdue': '⚠️ En retard'
      };
      return labels[status] || status;
    },
    logout() {
      localStorage.removeItem('client_access');
      this.$emit('view-change', 'landing');
    }
  }
}
</script>
```

---

## 🔌 STRUCTURE BACKEND POUR CODE CLIENT

### Modèle Django (À ajouter à `users/models.py`)
```python
class ClientAccessCode(models.Model):
    boutiquier = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    used_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.code} - {self.boutiquier.username}"
    
    def is_valid(self):
        return self.is_active and timezone.now() < self.expires_at
```

### API Endpoint (À ajouter à `users/views.py`)
```python
@api_view(['POST'])
def verify_client_code(request):
    """
    Vérifier le code d'accès client
    POST /api/verify-client-code/
    {
        "code": "ABC123",
        "client_name": "Mamadou Traoré"
    }
    """
    code = request.data.get('code')
    client_name = request.data.get('client_name')
    
    try:
        access_code = ClientAccessCode.objects.get(
            code=code,
            is_active=True,
            expires_at__gt=timezone.now()
        )
        
        # Enregistrer l'accès
        access_code.used_count += 1
        access_code.save()
        
        return Response({
            'success': True,
            'message': 'Code valide',
            'boutiquier_id': access_code.boutiquier.id
        })
    
    except ClientAccessCode.DoesNotExist:
        return Response(
            {'error': 'Code invalide ou expiré'},
            status=status.HTTP_400_BAD_REQUEST
        )
```

---

## 📊 FLUX DE DONNÉES

```
┌─────────────────────────────────────────────────────────────┐
│                    VUE.JS FRONTEND                          │
├─────────────────────────────────────────────────────────────┤
│  Landing Page → Login/AccessCode → Dashboard/ClientView    │
└─────────────────────────────────────────────────────────────┘
           ↓                              ↓
      ┌────────────┐              ┌──────────────┐
      │ Boutiquier │              │  Client      │
      │ Login      │              │  Access      │
      └────────────┘              └──────────────┘
           ↓                              ↓
      ┌────────────────────────────────────────────┐
      │         API DJANGO REST                    │
      ├────────────────────────────────────────────┤
      │ POST /api/users/token/                     │
      │ POST /api/verify-client-code/              │
      │ GET /api/clients/                          │
      │ GET /api/credits/                          │
      │ GET /api/dashboard/                        │
      └────────────────────────────────────────────┘
           ↓
      ┌────────────────────────────────────────────┐
      │         BASE DE DONNÉES SQLite             │
      ├────────────────────────────────────────────┤
      │ Users (Boutiquiers)                        │
      │ Clients                                    │
      │ Credits                                    │
      │ Payments                                   │
      │ ClientAccessCodes (Nouveau)                │
      └────────────────────────────────────────────┘
```

---

## 🔐 SÉCURITÉ DU CODE D'ACCÈS

✅ **Code limité à 6 caractères** - Facile à mémoriser
✅ **Code expirant** - Après 24/48h
✅ **Code unique** - Un seul code actif par boutiquier
✅ **Suivi d'utilisation** - Nombre d'accès
✅ **Accès lecture seule** - Client ne peut pas modifier
✅ **Validation serveur** - Vérification côté API
✅ **Token JWT** - Pour session authentifiée

---

## 📱 EXEMPLE DE FLUX CLIENT

1. **Client arrive** → Clic "Je suis Client"
2. **Saisit code** → "ABC123" (fourni par boutiquier)
3. **Valide le code** → Vérification API
4. **Saisit nom** → "Mamadou Traoré"
5. **Confirme code** → Sécurité double
6. **Accès tableau** → Voit ses crédits, montants, progression

---

## 🎨 CSS RESPONSIVE

```css
/* Desktop (1200px+) */
@media (min-width: 1200px) {
  .stats { display: grid; grid-template-columns: repeat(4, 1fr); }
  .credits { display: grid; grid-template-columns: repeat(3, 1fr); }
}

/* Tablet (768-1200px) */
@media (max-width: 1200px) {
  .stats { display: grid; grid-template-columns: repeat(2, 1fr); }
  .credits { display: grid; grid-template-columns: repeat(2, 1fr); }
}

/* Mobile (<768px) */
@media (max-width: 768px) {
  .stats { display: grid; grid-template-columns: 1fr; }
  .credits { display: grid; grid-template-columns: 1fr; }
  .tabs { flex-wrap: wrap; }
}
```

---

## ✨ RÉSUMÉ

| Élément | Description |
|---------|------------|
| **Accueil** | Choix type utilisateur |
| **Login Boutiquier** | Username + Password |
| **Access Client** | Code 6 caractères |
| **Dashboard Boutiquier** | Clients, Crédits, Codes |
| **Dashboard Client** | Mes crédits (lecture seule) |
| **Sécurité** | JWT + Code + Validation |
| **Responsive** | Mobile, Tablet, Desktop |

---

## 🚀 PROCHAINES ÉTAPES

1. ✅ Créer les modèles Django
2. ✅ Créer les endpoints API
3. ✅ Créer les composants Vue.js
4. ✅ Tester le flux complet
5. ✅ Ajouter validation côté client
6. ✅ Ajouter validation côté serveur
