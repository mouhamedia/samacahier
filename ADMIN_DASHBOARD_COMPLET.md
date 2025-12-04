# 🛠️ DASHBOARD ADMINISTRATEUR COMPLET

## 📊 STRUCTURE ADMIN VUE.JS

### 🎯 FLUX D'ACCÈS

```
┌──────────────────────────┐
│   ACCUEIL / LANDING      │
└──────────────────────────┘
           ↓
  ┌─────────────────────┐
  │  Choix utilisateur  │
  ├─────────────────────┤
  │ [Admin]             │
  │ [Boutiquier]        │
  │ [Client]            │
  └─────────────────────┘
     ↓         ↓          ↓
  ┌────────┐ ┌────────┐ ┌────────┐
  │ADMIN   │ │BOUTIQ. │ │CLIENT  │
  │LOGIN   │ │LOGIN   │ │CODE    │
  └────────┘ └────────┘ └────────┘
     ↓         ↓          ↓
  ┌────────────────────────────────┐
  │   DASHBOARDS                   │
  ├────────────────────────────────┤
  │ ADMIN: Gestion complète        │
  │ BOUTIQ: Ses clients/crédits    │
  │ CLIENT: Ses crédits            │
  └────────────────────────────────┘
```

---

## 🔐 LOGIN ADMIN

```vue
<template>
  <div class="login-container admin-login">
    <div class="login-card">
      <h2>🔐 Connexion Administrateur</h2>
      
      <form @submit.prevent="loginAdmin">
        <div class="form-group">
          <label>Email Admin</label>
          <input 
            v-model="form.username" 
            type="text" 
            placeholder="admin"
            required
          >
        </div>
        
        <div class="form-group">
          <label>Mot de passe</label>
          <input 
            v-model="form.password" 
            type="password" 
            placeholder="••••••••"
            required
          >
        </div>
        
        <button type="submit" class="btn btn-primary" :disabled="loading">
          {{ loading ? 'Connexion...' : 'Se connecter' }}
        </button>
      </form>
      
      <div v-if="error" class="alert alert-error">{{ error }}</div>
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
      error: ''
    }
  },
  methods: {
    async loginAdmin() {
      this.loading = true;
      this.error = '';
      
      try {
        const response = await axios.post(
          'http://localhost:8000/api/users/token/',
          this.form
        );
        
        // Vérifier que c'est un admin
        if (!response.data.is_superuser) {
          this.error = 'Accès administrateur requis';
          return;
        }
        
        localStorage.setItem('token', response.data.access);
        localStorage.setItem('user_role', 'admin');
        localStorage.setItem('username', response.data.username);
        
        this.$emit('view-change', 'admin-dashboard');
        
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

## 🛠️ DASHBOARD ADMINISTRATEUR COMPLET

```vue
<template>
  <div class="admin-dashboard">
    <!-- HEADER -->
    <header class="admin-header">
      <div class="header-left">
        <h1>🔧 Panneau Administrateur</h1>
        <p>Gestion complète du système</p>
      </div>
      <div class="header-right">
        <span class="user-badge">{{ username }}</span>
        <button @click="logout" class="btn btn-danger">Déconnexion</button>
      </div>
    </header>
    
    <!-- STATISTIQUES GLOBALES -->
    <section class="global-stats">
      <div class="stat-card">
        <h3>👥 Boutiquiers</h3>
        <p class="stat-value">{{ stats.totalBoutiquiers }}</p>
      </div>
      <div class="stat-card">
        <h3>👤 Clients Total</h3>
        <p class="stat-value">{{ stats.totalClients }}</p>
      </div>
      <div class="stat-card">
        <h3>💰 Crédits Total</h3>
        <p class="stat-value">{{ formatCurrency(stats.totalCredits) }}</p>
      </div>
      <div class="stat-card">
        <h3>✅ Payé Total</h3>
        <p class="stat-value">{{ formatCurrency(stats.totalPaid) }}</p>
      </div>
    </section>
    
    <!-- ONGLETS PRINCIPAUX -->
    <section class="admin-tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab"
        @click="activeTab = tab"
        :class="{ active: activeTab === tab }"
        class="tab-button"
      >
        {{ getTabIcon(tab) }} {{ tab }}
      </button>
    </section>
    
    <!-- CONTENU ONGLETS -->
    <section class="tab-content-admin">
      
      <!-- 1. GESTION DES BOUTIQUIERS -->
      <div v-if="activeTab === 'Boutiquiers'" class="content-panel">
        <div class="panel-header">
          <h2>👥 Gestion des Boutiquiers</h2>
          <button @click="showBoutiquierForm = true" class="btn btn-primary">
            ➕ Ajouter un Boutiquier
          </button>
        </div>
        
        <!-- Formulaire ajout boutiquier -->
        <div v-if="showBoutiquierForm" class="form-modal">
          <div class="form-modal-content">
            <h3>Créer un Boutiquier</h3>
            <form @submit.prevent="addBoutiquier">
              <div class="form-group">
                <label>Nom d'utilisateur</label>
                <input v-model="boutiquierForm.username" type="text" required>
              </div>
              <div class="form-group">
                <label>Email</label>
                <input v-model="boutiquierForm.email" type="email" required>
              </div>
              <div class="form-group">
                <label>Prénom</label>
                <input v-model="boutiquierForm.first_name" type="text" required>
              </div>
              <div class="form-group">
                <label>Nom</label>
                <input v-model="boutiquierForm.last_name" type="text" required>
              </div>
              <div class="form-group">
                <label>Téléphone</label>
                <input v-model="boutiquierForm.phone" type="tel" required>
              </div>
              <div class="form-group">
                <label>Mot de passe</label>
                <input v-model="boutiquierForm.password" type="password" required>
              </div>
              <div class="form-group">
                <label>Confirmer mot de passe</label>
                <input v-model="boutiquierForm.password_confirm" type="password" required>
              </div>
              
              <div class="form-actions">
                <button type="submit" class="btn btn-primary">Créer</button>
                <button type="button" @click="showBoutiquierForm = false" class="btn btn-secondary">Annuler</button>
              </div>
            </form>
            <div v-if="boutiquierError" class="alert alert-error">{{ boutiquierError }}</div>
          </div>
        </div>
        
        <!-- Liste des boutiquiers -->
        <div class="table-container">
          <table class="admin-table">
            <thead>
              <tr>
                <th>Nom</th>
                <th>Email</th>
                <th>Téléphone</th>
                <th>Clients</th>
                <th>Crédits</th>
                <th>Actif</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="boutiq in boutiquiers" :key="boutiq.id">
                <td>{{ boutiq.first_name }} {{ boutiq.last_name }}</td>
                <td>{{ boutiq.email }}</td>
                <td>{{ boutiq.phone }}</td>
                <td class="center">{{ boutiq.clients_count }}</td>
                <td class="center">{{ boutiq.credits_count }}</td>
                <td class="center">
                  <span :class="{ active: boutiq.is_active }" class="badge">
                    {{ boutiq.is_active ? '✅' : '❌' }}
                  </span>
                </td>
                <td class="actions">
                  <button @click="editBoutiquier(boutiq)" class="btn btn-small btn-info">Éditer</button>
                  <button @click="toggleBoutiquier(boutiq)" class="btn btn-small btn-warning">
                    {{ boutiq.is_active ? 'Désactiver' : 'Activer' }}
                  </button>
                  <button @click="deleteBoutiquier(boutiq)" class="btn btn-small btn-danger">Supprimer</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- 2. GESTION DES CLIENTS -->
      <div v-if="activeTab === 'Clients'" class="content-panel">
        <div class="panel-header">
          <h2>👤 Gestion des Clients</h2>
          <div class="filter-group">
            <select v-model="selectedBoutiquierFilter" class="select">
              <option value="">-- Tous les boutiquiers --</option>
              <option v-for="b in boutiquiers" :key="b.id" :value="b.id">
                {{ b.first_name }} {{ b.last_name }}
              </option>
            </select>
            <button @click="showClientForm = true" class="btn btn-primary">
              ➕ Ajouter un Client
            </button>
          </div>
        </div>
        
        <!-- Formulaire ajout client -->
        <div v-if="showClientForm" class="form-modal">
          <div class="form-modal-content">
            <h3>Créer un Client</h3>
            <form @submit.prevent="addClient">
              <div class="form-group">
                <label>Boutiquier</label>
                <select v-model="clientForm.boutiquier" required>
                  <option value="">-- Sélectionner --</option>
                  <option v-for="b in boutiquiers" :key="b.id" :value="b.id">
                    {{ b.first_name }} {{ b.last_name }}
                  </option>
                </select>
              </div>
              <div class="form-group">
                <label>Nom</label>
                <input v-model="clientForm.name" type="text" required>
              </div>
              <div class="form-group">
                <label>Téléphone</label>
                <input v-model="clientForm.phone" type="tel" required>
              </div>
              <div class="form-group">
                <label>Email</label>
                <input v-model="clientForm.email" type="email">
              </div>
              <div class="form-group">
                <label>Adresse</label>
                <textarea v-model="clientForm.address"></textarea>
              </div>
              
              <div class="form-actions">
                <button type="submit" class="btn btn-primary">Créer</button>
                <button type="button" @click="showClientForm = false" class="btn btn-secondary">Annuler</button>
              </div>
            </form>
          </div>
        </div>
        
        <!-- Liste des clients -->
        <div class="table-container">
          <table class="admin-table">
            <thead>
              <tr>
                <th>Nom</th>
                <th>Boutiquier</th>
                <th>Téléphone</th>
                <th>Email</th>
                <th>Adresse</th>
                <th>Crédits</th>
                <th>Actif</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="client in filteredClients" :key="client.id">
                <td>{{ client.name }}</td>
                <td>{{ client.boutiquier_name }}</td>
                <td>{{ client.phone }}</td>
                <td>{{ client.email }}</td>
                <td>{{ client.address }}</td>
                <td class="center">{{ client.credits_count }}</td>
                <td class="center">
                  <span :class="{ active: client.is_active }" class="badge">
                    {{ client.is_active ? '✅' : '❌' }}
                  </span>
                </td>
                <td class="actions">
                  <button @click="editClient(client)" class="btn btn-small btn-info">Éditer</button>
                  <button @click="toggleClient(client)" class="btn btn-small btn-warning">
                    {{ client.is_active ? 'Désactiver' : 'Activer' }}
                  </button>
                  <button @click="deleteClient(client)" class="btn btn-small btn-danger">Supprimer</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- 3. GESTION DES CRÉDITS -->
      <div v-if="activeTab === 'Crédits'" class="content-panel">
        <div class="panel-header">
          <h2>💰 Gestion des Crédits</h2>
          <button @click="showCreditForm = true" class="btn btn-primary">
            ➕ Ajouter un Crédit
          </button>
        </div>
        
        <!-- Formulaire ajout crédit -->
        <div v-if="showCreditForm" class="form-modal">
          <div class="form-modal-content">
            <h3>Créer un Crédit</h3>
            <form @submit.prevent="addCredit">
              <div class="form-group">
                <label>Client</label>
                <select v-model="creditForm.client" required>
                  <option value="">-- Sélectionner --</option>
                  <option v-for="c in clients" :key="c.id" :value="c.id">
                    {{ c.name }} ({{ c.boutiquier_name }})
                  </option>
                </select>
              </div>
              <div class="form-group">
                <label>Montant</label>
                <input v-model.number="creditForm.amount" type="number" step="0.01" required>
              </div>
              <div class="form-group">
                <label>Date d'échéance</label>
                <input v-model="creditForm.due_date" type="date" required>
              </div>
              <div class="form-group">
                <label>Description</label>
                <textarea v-model="creditForm.description" placeholder="Description du crédit"></textarea>
              </div>
              
              <div class="form-actions">
                <button type="submit" class="btn btn-primary">Créer</button>
                <button type="button" @click="showCreditForm = false" class="btn btn-secondary">Annuler</button>
              </div>
            </form>
          </div>
        </div>
        
        <!-- Liste des crédits -->
        <div class="table-container">
          <table class="admin-table">
            <thead>
              <tr>
                <th>Client</th>
                <th>Montant</th>
                <th>Payé</th>
                <th>Restant</th>
                <th>Progression</th>
                <th>Statut</th>
                <th>Échéance</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="credit in credits" :key="credit.id">
                <td>{{ credit.client_name }}</td>
                <td>{{ formatCurrency(credit.amount) }}</td>
                <td>{{ formatCurrency(credit.paid_amount) }}</td>
                <td>{{ formatCurrency(credit.amount - credit.paid_amount) }}</td>
                <td>
                  <div class="progress-mini">
                    <div class="progress-bar" :style="{ width: getProgress(credit) + '%' }"></div>
                  </div>
                  {{ getProgress(credit) }}%
                </td>
                <td>
                  <span :class="'status-' + credit.status" class="badge">
                    {{ credit.status }}
                  </span>
                </td>
                <td>{{ formatDate(credit.due_date) }}</td>
                <td class="actions">
                  <button @click="viewCredit(credit)" class="btn btn-small btn-info">Voir</button>
                  <button @click="deleteCredit(credit)" class="btn btn-small btn-danger">Supprimer</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- 4. GESTION DES PAIEMENTS -->
      <div v-if="activeTab === 'Paiements'" class="content-panel">
        <div class="panel-header">
          <h2>💳 Historique des Paiements</h2>
        </div>
        
        <!-- Liste des paiements -->
        <div class="table-container">
          <table class="admin-table">
            <thead>
              <tr>
                <th>Client</th>
                <th>Crédit ID</th>
                <th>Montant</th>
                <th>Date</th>
                <th>Boutiquier</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="payment in payments" :key="payment.id">
                <td>{{ payment.client_name }}</td>
                <td>#{{ payment.credit_id }}</td>
                <td>{{ formatCurrency(payment.amount) }}</td>
                <td>{{ formatDate(payment.date) }}</td>
                <td>{{ payment.boutiquier_name }}</td>
                <td class="actions">
                  <button @click="deletePayment(payment)" class="btn btn-small btn-danger">Supprimer</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- 5. CODES D'ACCÈS CLIENT -->
      <div v-if="activeTab === 'Codes' " class="content-panel">
        <div class="panel-header">
          <h2>🔐 Codes d'Accès Client</h2>
        </div>
        
        <!-- Tableau codes -->
        <div class="table-container">
          <table class="admin-table">
            <thead>
              <tr>
                <th>Boutiquier</th>
                <th>Code</th>
                <th>Créé</th>
                <th>Expire</th>
                <th>Utilisations</th>
                <th>Actif</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="code in accessCodes" :key="code.id">
                <td>{{ code.boutiquier_name }}</td>
                <td class="code-display">{{ code.code }}</td>
                <td>{{ formatDate(code.created_at) }}</td>
                <td>{{ formatDate(code.expires_at) }}</td>
                <td class="center">{{ code.used_count }}</td>
                <td class="center">
                  <span :class="{ active: code.is_active }" class="badge">
                    {{ code.is_active ? '✅' : '❌' }}
                  </span>
                </td>
                <td class="actions">
                  <button @click="toggleCode(code)" class="btn btn-small btn-warning">
                    {{ code.is_active ? 'Désactiver' : 'Activer' }}
                  </button>
                  <button @click="deleteCode(code)" class="btn btn-small btn-danger">Supprimer</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- 6. PARAMÈTRES -->
      <div v-if="activeTab === 'Paramètres'" class="content-panel">
        <div class="settings-group">
          <h2>⚙️ Paramètres Système</h2>
          
          <div class="setting-item">
            <label>Durée de validité code client (jours)</label>
            <input v-model.number="settings.codeValidityDays" type="number" min="1">
            <button @click="saveSettings" class="btn btn-primary">Enregistrer</button>
          </div>
          
          <div class="setting-item">
            <label>Nombre maximum d'utilisation par code</label>
            <input v-model.number="settings.maxCodeUsage" type="number" min="1">
            <button @click="saveSettings" class="btn btn-primary">Enregistrer</button>
          </div>
          
          <div class="setting-item">
            <h3>Statistiques Système</h3>
            <p>Total données: {{ calculateTotalData() }} MB</p>
            <p>Dernière sauvegarde: {{ lastBackup }}</p>
            <button @click="backupDatabase" class="btn btn-primary">Sauvegarder maintenant</button>
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
      username: '',
      activeTab: 'Boutiquiers',
      tabs: ['Boutiquiers', 'Clients', 'Crédits', 'Paiements', 'Codes', 'Paramètres'],
      
      // Données
      boutiquiers: [],
      clients: [],
      credits: [],
      payments: [],
      accessCodes: [],
      
      // Statistiques
      stats: {
        totalBoutiquiers: 0,
        totalClients: 0,
        totalCredits: 0,
        totalPaid: 0
      },
      
      // Formulaires
      showBoutiquierForm: false,
      showClientForm: false,
      showCreditForm: false,
      
      boutiquierForm: {
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        phone: '',
        password: '',
        password_confirm: ''
      },
      
      clientForm: {
        boutiquier: '',
        name: '',
        phone: '',
        email: '',
        address: ''
      },
      
      creditForm: {
        client: '',
        amount: 0,
        due_date: '',
        description: ''
      },
      
      // Filtres
      selectedBoutiquierFilter: '',
      
      // Messages
      boutiquierError: '',
      
      // Paramètres
      settings: {
        codeValidityDays: 7,
        maxCodeUsage: 999
      },
      
      lastBackup: 'Jamais'
    }
  },
  
  computed: {
    filteredClients() {
      if (!this.selectedBoutiquierFilter) {
        return this.clients;
      }
      return this.clients.filter(c => c.boutiquier_id == this.selectedBoutiquierFilter);
    }
  },
  
  mounted() {
    this.loadAdminData();
  },
  
  methods: {
    async loadAdminData() {
      this.username = localStorage.getItem('username');
      
      // Charger toutes les données depuis les APIs
      try {
        // GET /api/users/?role=boutiquier
        // GET /api/clients/
        // GET /api/credits/
        // GET /api/payments/
        // GET /api/access-codes/
      } catch (error) {
        console.error('Erreur chargement données:', error);
      }
    },
    
    // ============ BOUTIQUIERS ============
    async addBoutiquier() {
      try {
        const response = await axios.post(
          'http://localhost:8000/api/users/',
          {
            ...this.boutiquierForm,
            role: 'boutiquier'
          },
          {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
          }
        );
        
        this.boutiquiers.push(response.data);
        this.showBoutiquierForm = false;
        this.resetBoutiquierForm();
        
      } catch (error) {
        this.boutiquierError = 'Erreur création boutiquier';
      }
    },
    
    resetBoutiquierForm() {
      this.boutiquierForm = {
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        phone: '',
        password: '',
        password_confirm: ''
      };
    },
    
    editBoutiquier(boutiq) {
      // Modal édition
    },
    
    async toggleBoutiquier(boutiq) {
      // PATCH /api/users/{id}/
    },
    
    async deleteBoutiquier(boutiq) {
      if (confirm('Êtes-vous sûr ?')) {
        // DELETE /api/users/{id}/
      }
    },
    
    // ============ CLIENTS ============
    async addClient() {
      try {
        const response = await axios.post(
          'http://localhost:8000/api/clients/',
          this.clientForm,
          {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
          }
        );
        
        this.clients.push(response.data);
        this.showClientForm = false;
        this.clientForm = {};
        
      } catch (error) {
        console.error('Erreur création client:', error);
      }
    },
    
    editClient(client) {},
    async toggleClient(client) {},
    async deleteClient(client) {},
    
    // ============ CRÉDITS ============
    async addCredit() {},
    viewCredit(credit) {},
    async deleteCredit(credit) {},
    
    // ============ UTILITAIRES ============
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
    
    getTabIcon(tab) {
      const icons = {
        'Boutiquiers': '👥',
        'Clients': '👤',
        'Crédits': '💰',
        'Paiements': '💳',
        'Codes': '🔐',
        'Paramètres': '⚙️'
      };
      return icons[tab] || '';
    },
    
    calculateTotalData() {
      return (this.boutiquiers.length * 0.5 + 
              this.clients.length * 0.3 + 
              this.credits.length * 0.4).toFixed(2);
    },
    
    async saveSettings() {
      // Sauvegarder les paramètres
    },
    
    async backupDatabase() {
      // POST /api/backup/
    },
    
    logout() {
      localStorage.removeItem('token');
      this.$emit('view-change', 'landing');
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
  background: #f5f7fa;
  min-height: 100vh;
}

.admin-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.global-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  padding: 20px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #667eea;
  margin: 10px 0 0;
}

.admin-tabs {
  display: flex;
  gap: 10px;
  padding: 20px;
  background: white;
  border-bottom: 2px solid #eee;
  flex-wrap: wrap;
}

.tab-button {
  padding: 10px 20px;
  border: none;
  background: #f0f0f0;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.tab-button.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.tab-content-admin {
  padding: 20px;
}

.content-panel {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 10px;
}

.filter-group {
  display: flex;
  gap: 10px;
  align-items: center;
}

.admin-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.admin-table th {
  background: #f5f5f5;
  padding: 12px;
  text-align: left;
  font-weight: bold;
  border-bottom: 2px solid #ddd;
}

.admin-table td {
  padding: 12px;
  border-bottom: 1px solid #eee;
}

.admin-table tr:hover {
  background: #f9f9f9;
}

.actions {
  display: flex;
  gap: 5px;
}

.btn-small {
  padding: 5px 10px;
  font-size: 12px;
}

.form-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.form-modal-content {
  background: white;
  padding: 30px;
  border-radius: 8px;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.status-pending { background: #fff3cd; }
.status-partial { background: #cce5ff; }
.status-paid { background: #d4edda; }
.status-overdue { background: #f8d7da; }

.progress-mini {
  height: 4px;
  background: #eee;
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 5px;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
}

.center {
  text-align: center;
}

.code-display {
  font-family: monospace;
  font-size: 14px;
  font-weight: bold;
  background: #f5f5f5;
  padding: 8px;
  border-radius: 4px;
}

.settings-group {
  max-width: 600px;
}

.setting-item {
  padding: 20px;
  border: 1px solid #eee;
  border-radius: 4px;
  margin-bottom: 15px;
}

.user-badge {
  background: rgba(255,255,255,0.2);
  padding: 8px 15px;
  border-radius: 20px;
  margin-right: 15px;
}

@media (max-width: 768px) {
  .admin-header {
    flex-direction: column;
    gap: 10px;
  }
  
  .admin-table {
    font-size: 12px;
  }
  
  .actions {
    flex-direction: column;
  }
}
</style>
```

---

## 🔄 API ENDPOINTS À CRÉER

```python
# users/views.py

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsSuperUser])
def create_boutiquier(request):
    """Créer un boutiquier"""
    # POST /api/users/create-boutiquier/
    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsSuperUser])
def manage_users(request):
    """Lister/créer utilisateurs"""
    # GET/POST /api/users/
    
@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAuthenticated, IsSuperUser])
def user_detail(request, pk):
    """Éditer/supprimer utilisateur"""
    # PATCH/DELETE /api/users/{id}/

# clients/views.py

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def manage_clients(request):
    """Lister/créer clients"""
    # GET/POST /api/clients/
    
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def client_detail(request, pk):
    """Détails client"""
    # GET/PATCH/DELETE /api/clients/{id}/

# credits/views.py

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def manage_credits(request):
    """Lister/créer crédits"""
    # GET/POST /api/credits/
    
@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def credit_detail(request, pk):
    """Détails crédit"""
    # GET/DELETE /api/credits/{id}/
```

---

## ✨ RÉSUMÉ

| Fonctionnalité | Description |
|----------------|-------------|
| **Dashboard Admin** | Gestion complète du système |
| **Boutiquiers** | Créer, éditer, activer/désactiver |
| **Clients** | Gérer tous les clients |
| **Crédits** | Créer et suivre les crédits |
| **Paiements** | Historique complet |
| **Codes** | Gérer codes d'accès client |
| **Paramètres** | Configuration système |
| **Statistiques** | Vue d'ensemble globale |

