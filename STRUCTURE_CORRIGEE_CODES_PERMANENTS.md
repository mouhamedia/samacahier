# 🎯 STRUCTURE CORRIGÉE - VUE.JS AVEC CODES PERMANENTS

## 📊 FLUX FINAL CORRECT

```
┌─────────────────────────────────┐
│     LANDING PAGE / ACCUEIL      │
└─────────────────────────────────┘
           ↓
    ┌──────────────────────┐
    │  Choix utilisateur   │
    ├──────────────────────┤
    │ [Admin]              │
    │ [Boutiquier]         │
    │ [Client (Code)]      │
    └──────────────────────┘
       ↓       ↓          ↓
    ┌────┐ ┌────────┐ ┌──────────┐
    │ADM │ │BOUTIQ  │ │ CLIENTE  │
    │LOG │ │LOGIN   │ │ CODE     │
    └────┘ └────────┘ └──────────┘
       ↓       ↓          ↓
    ┌─────────────────────────────┐
    │   DASHBOARDS                │
    ├─────────────────────────────┤
    │ • Admin: Gère boutiquiers   │
    │ • Boutiquier: Crée clients  │
    │ • Client: Voit ses crédits  │
    └─────────────────────────────┘
```

---

## 🔐 SYSTÈME DE CODE CLIENT

### **CHAQUE CLIENT = UN CODE UNIQUE & PERMANENT**

```
Client: Mamadou Traoré
├── Code: MAM-TR-001 ✅ FIXE (ne change jamais)
├── Crédits associés
└── Accès via ce code toute sa vie

Client: Fatima Diallo
├── Code: FAT-DI-002 ✅ FIXE (ne change jamais)
├── Crédits associés
└── Accès via ce code toute sa vie
```

### **Modèle Django (Client)**

```python
class Client(models.Model):
    boutiquier = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    
    # CODE UNIQUE & PERMANENT
    access_code = models.CharField(
        max_length=20, 
        unique=True,
        editable=False  # ❌ L'admin ne peut pas le modifier !
    )
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.access_code:
            # Générer le code UNE SEULE FOIS à la création
            self.access_code = self.generate_unique_code()
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_unique_code():
        """Générer code unique: ABC-DE-001"""
        import uuid
        code = str(uuid.uuid4())[:8].upper()
        return f"{code}"
    
    def __str__(self):
        return f"{self.name} ({self.access_code})"
```

---

## 📁 FICHIERS VUE.JS À CRÉER

```
frontend/
├── index.html                           ← Application complète
├── components/
│   ├── Landing.vue
│   ├── AdminLogin.vue
│   ├── BoutiquierLogin.vue
│   ├── ClientAccessByCode.vue          ← Code permanent
│   ├── AdminDashboard.vue
│   ├── BoutiquierDashboard.vue
│   └── ClientDashboard.vue
└── css/
    └── style.css
```

---

## 🎨 COMPOSANT: CLIENT ACCÈS PAR CODE

```vue
<template>
  <div class="client-access-container">
    <div class="access-card">
      <h2>📱 Accès Client</h2>
      <p class="subtitle">Entrez votre code personnel</p>
      
      <form @submit.prevent="accessAsClient">
        <div class="form-group">
          <label>Votre code client</label>
          <input 
            v-model="form.code" 
            type="text" 
            placeholder="Ex: ABC-DE-001"
            maxlength="20"
            class="code-input"
            @keyup.enter="accessAsClient"
          >
          <small class="hint">Code fourni à la création du compte</small>
        </div>
        
        <div class="form-group">
          <label>Votre nom (confirmation)</label>
          <input 
            v-model="form.name" 
            type="text" 
            placeholder="Votre nom complet"
            @keyup.enter="accessAsClient"
          >
        </div>
        
        <button type="submit" class="btn btn-primary" :disabled="loading">
          {{ loading ? 'Vérification...' : 'Accéder à mes crédits' }}
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
        code: '',
        name: ''
      },
      loading: false,
      error: '',
      success: ''
    }
  },
  methods: {
    async accessAsClient() {
      if (!this.form.code || !this.form.name) {
        this.error = 'Veuillez remplir tous les champs';
        return;
      }
      
      this.loading = true;
      this.error = '';
      
      try {
        // Appel API pour vérifier le code
        const response = await axios.post(
          'http://localhost:8000/api/clients/verify-code/',
          {
            code: this.form.code,
            name: this.form.name
          }
        );
        
        // Code valide et correspond au nom
        localStorage.setItem('client_code', this.form.code);
        localStorage.setItem('client_id', response.data.client_id);
        localStorage.setItem('client_name', response.data.client_name);
        localStorage.setItem('boutiquier_id', response.data.boutiquier_id);
        
        this.success = 'Bienvenue ! 🎉';
        this.$emit('view-change', 'client-dashboard');
        
      } catch (error) {
        if (error.response?.status === 404) {
          this.error = 'Code invalide ou client inexistant';
        } else if (error.response?.status === 400) {
          this.error = 'Le nom ne correspond pas';
        } else {
          this.error = 'Erreur d\'accès';
        }
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.client-access-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.access-card {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.2);
  max-width: 400px;
  width: 90%;
}

.access-card h2 {
  text-align: center;
  margin-bottom: 10px;
  color: #333;
}

.subtitle {
  text-align: center;
  color: #666;
  margin-bottom: 30px;
  font-size: 14px;
}

.code-input {
  font-size: 16px;
  letter-spacing: 2px;
  text-transform: uppercase;
  text-align: center;
  font-weight: bold;
}

.hint {
  display: block;
  margin-top: 8px;
  color: #999;
  font-size: 12px;
  text-align: center;
}
</style>
```

---

## 🛠️ DASHBOARD BOUTIQUIER (CORRIGÉ)

```vue
<template>
  <div class="boutiquier-dashboard">
    <!-- HEADER -->
    <header class="dashboard-header">
      <div class="header-left">
        <h1>👤 Mes Clients & Crédits</h1>
        <p>Bienvenue {{ username }}</p>
      </div>
      <div class="header-right">
        <button @click="logout" class="btn btn-danger">Déconnexion</button>
      </div>
    </header>
    
    <!-- STATISTIQUES -->
    <section class="stats">
      <div class="stat-card">
        <h3>👥 Mes Clients</h3>
        <p class="stat-value">{{ clients.length }}</p>
      </div>
      <div class="stat-card">
        <h3>💰 Crédits Total</h3>
        <p class="stat-value">{{ formatCurrency(totalCredits) }}</p>
      </div>
      <div class="stat-card">
        <h3>✅ Payé</h3>
        <p class="stat-value">{{ formatCurrency(totalPaid) }}</p>
      </div>
      <div class="stat-card">
        <h3>⏳ Restant</h3>
        <p class="stat-value">{{ formatCurrency(remaining) }}</p>
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
    
    <!-- CONTENU -->
    <section class="content">
      
      <!-- 1. MES CLIENTS -->
      <div v-if="activeTab === 'Clients'" class="tab-content">
        <div class="add-button">
          <button @click="showClientForm = true" class="btn btn-primary">
            ➕ Ajouter un Client
          </button>
        </div>
        
        <!-- FORMULAIRE AJOUT CLIENT -->
        <div v-if="showClientForm" class="form-modal">
          <div class="form-modal-content">
            <h3>Créer un Client</h3>
            <form @submit.prevent="addClient">
              <div class="form-group">
                <label>Nom complet *</label>
                <input v-model="clientForm.name" type="text" required>
              </div>
              <div class="form-group">
                <label>Téléphone *</label>
                <input v-model="clientForm.phone" type="tel" required>
              </div>
              <div class="form-group">
                <label>Email</label>
                <input v-model="clientForm.email" type="email">
              </div>
              <div class="form-group">
                <label>Adresse</label>
                <textarea v-model="clientForm.address" rows="3"></textarea>
              </div>
              
              <div class="form-actions">
                <button type="submit" class="btn btn-primary">Créer</button>
                <button type="button" @click="showClientForm = false" class="btn btn-secondary">Annuler</button>
              </div>
            </form>
            
            <div v-if="clientError" class="alert alert-error">{{ clientError }}</div>
            <div v-if="clientSuccess" class="alert alert-success">
              ✅ Client créé avec succès !
              <br>
              <strong>Code: {{ newClientCode }}</strong>
              <br>
              <small>Donnez ce code au client pour accéder à ses crédits</small>
            </div>
          </div>
        </div>
        
        <!-- LISTE CLIENTS -->
        <div class="clients-grid">
          <div v-for="client in clients" :key="client.id" class="client-card">
            <div class="client-header">
              <h3>{{ client.name }}</h3>
              <span :class="{ active: client.is_active }" class="status-badge">
                {{ client.is_active ? 'Actif' : 'Inactif' }}
              </span>
            </div>
            
            <div class="client-info">
              <p><strong>📞 Téléphone:</strong> {{ client.phone }}</p>
              <p><strong>✉️ Email:</strong> {{ client.email || '-' }}</p>
              <p><strong>📍 Adresse:</strong> {{ client.address || '-' }}</p>
            </div>
            
            <!-- CODE PERMANENT -->
            <div class="code-section">
              <label>Code permanent (à partager):</label>
              <div class="code-display">
                <span class="code">{{ client.access_code }}</span>
                <button 
                  type="button"
                  @click="copyCode(client.access_code)"
                  class="btn btn-small btn-copy"
                  title="Copier"
                >
                  📋
                </button>
              </div>
            </div>
            
            <!-- CRÉDITS CLIENT -->
            <div class="client-credits">
              <p><strong>Crédits:</strong> {{ client.credits_count }}</p>
              <p><strong>Total dû:</strong> {{ formatCurrency(client.total_credits) }}</p>
              <p><strong>Payé:</strong> {{ formatCurrency(client.total_paid) }}</p>
            </div>
            
            <!-- ACTIONS -->
            <div class="client-actions">
              <button @click="editClient(client)" class="btn btn-small btn-info">✏️ Éditer</button>
              <button @click="toggleClient(client)" class="btn btn-small btn-warning">
                {{ client.is_active ? '🔒 Désactiver' : '🔓 Activer' }}
              </button>
              <button @click="deleteClient(client)" class="btn btn-small btn-danger">🗑️ Supprimer</button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 2. MES CRÉDITS -->
      <div v-if="activeTab === 'Crédits'" class="tab-content">
        <div class="add-button">
          <button @click="showCreditForm = true" class="btn btn-primary">
            ➕ Ajouter un Crédit
          </button>
        </div>
        
        <!-- FORMULAIRE CRÉDIT -->
        <div v-if="showCreditForm" class="form-modal">
          <div class="form-modal-content">
            <h3>Créer un Crédit</h3>
            <form @submit.prevent="addCredit">
              <div class="form-group">
                <label>Client *</label>
                <select v-model="creditForm.client" required>
                  <option value="">-- Sélectionner --</option>
                  <option v-for="c in clients" :key="c.id" :value="c.id">
                    {{ c.name }}
                  </option>
                </select>
              </div>
              <div class="form-group">
                <label>Montant *</label>
                <input v-model.number="creditForm.amount" type="number" step="0.01" required>
              </div>
              <div class="form-group">
                <label>Date d'échéance</label>
                <input v-model="creditForm.due_date" type="date">
              </div>
              <div class="form-group">
                <label>Description</label>
                <textarea v-model="creditForm.description" rows="3"></textarea>
              </div>
              
              <div class="form-actions">
                <button type="submit" class="btn btn-primary">Créer</button>
                <button type="button" @click="showCreditForm = false" class="btn btn-secondary">Annuler</button>
              </div>
            </form>
          </div>
        </div>
        
        <!-- LISTE CRÉDITS -->
        <div class="credits-list">
          <div v-for="credit in allCredits" :key="credit.id" class="credit-card">
            <div class="credit-header">
              <h3>{{ credit.client_name }}</h3>
              <span :class="'status-' + credit.status" class="status">
                {{ credit.status }}
              </span>
            </div>
            
            <div class="credit-details">
              <div class="detail-item">
                <span>Montant:</span>
                <strong>{{ formatCurrency(credit.amount) }}</strong>
              </div>
              <div class="detail-item">
                <span>Payé:</span>
                <strong class="paid">{{ formatCurrency(credit.paid_amount) }}</strong>
              </div>
              <div class="detail-item">
                <span>Restant:</span>
                <strong class="due">{{ formatCurrency(credit.amount - credit.paid_amount) }}</strong>
              </div>
            </div>
            
            <div class="progress-bar">
              <div class="progress" :style="{ width: getProgress(credit) + '%' }"></div>
            </div>
            <small>{{ getProgress(credit) }}% payé</small>
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
      activeTab: 'Clients',
      tabs: ['Clients', 'Crédits'],
      
      clients: [],
      allCredits: [],
      
      showClientForm: false,
      showCreditForm: false,
      
      clientForm: {
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
      
      clientError: '',
      clientSuccess: '',
      newClientCode: ''
    }
  },
  
  computed: {
    totalCredits() {
      return this.allCredits.reduce((sum, c) => sum + c.amount, 0);
    },
    totalPaid() {
      return this.allCredits.reduce((sum, c) => sum + c.paid_amount, 0);
    },
    remaining() {
      return this.totalCredits - this.totalPaid;
    }
  },
  
  mounted() {
    this.loadBoutiquierData();
  },
  
  methods: {
    async loadBoutiquierData() {
      this.username = localStorage.getItem('username');
      
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };
      
      try {
        // Charger les clients
        const clientsRes = await axios.get(
          'http://localhost:8000/api/clients/',
          { headers }
        );
        this.clients = clientsRes.data;
        
        // Charger les crédits
        const creditsRes = await axios.get(
          'http://localhost:8000/api/credits/',
          { headers }
        );
        this.allCredits = creditsRes.data;
        
      } catch (error) {
        console.error('Erreur chargement données:', error);
      }
    },
    
    async addClient() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.post(
          'http://localhost:8000/api/clients/',
          this.clientForm,
          {
            headers: { Authorization: `Bearer ${token}` }
          }
        );
        
        this.clients.push(response.data);
        this.newClientCode = response.data.access_code;
        this.clientSuccess = true;
        
        // Réinitialiser formulaire après 3 secondes
        setTimeout(() => {
          this.showClientForm = false;
          this.clientForm = { name: '', phone: '', email: '', address: '' };
          this.clientSuccess = false;
        }, 3000);
        
      } catch (error) {
        this.clientError = 'Erreur création client';
      }
    },
    
    async addCredit() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.post(
          'http://localhost:8000/api/credits/',
          this.creditForm,
          {
            headers: { Authorization: `Bearer ${token}` }
          }
        );
        
        this.allCredits.push(response.data);
        this.showCreditForm = false;
        this.creditForm = { client: '', amount: 0, due_date: '', description: '' };
        
      } catch (error) {
        console.error('Erreur création crédit:', error);
      }
    },
    
    editClient(client) {},
    toggleClient(client) {},
    deleteClient(client) {},
    
    copyCode(code) {
      navigator.clipboard.writeText(code);
      alert('Code copié ! 📋');
    },
    
    formatCurrency(value) {
      return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'XOF'
      }).format(value || 0);
    },
    
    getProgress(credit) {
      if (credit.amount === 0) return 0;
      return Math.round((credit.paid_amount / credit.amount) * 100);
    },
    
    logout() {
      localStorage.removeItem('token');
      this.$emit('view-change', 'landing');
    }
  }
}
</script>

<style scoped>
.boutiquier-dashboard {
  background: #f5f7fa;
  min-height: 100vh;
}

.dashboard-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stats {
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
  margin-top: 10px;
}

.clients-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
  padding: 20px;
}

.client-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.client-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  border-bottom: 2px solid #eee;
  padding-bottom: 10px;
}

.status-badge {
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 12px;
  background: #f0f0f0;
}

.status-badge.active {
  background: #d4edda;
  color: #155724;
}

.code-section {
  background: #f9f9f9;
  padding: 15px;
  border-radius: 6px;
  margin: 15px 0;
}

.code-display {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 10px;
}

.code {
  font-family: monospace;
  font-size: 16px;
  font-weight: bold;
  background: white;
  padding: 8px 12px;
  border-radius: 4px;
  border: 2px solid #667eea;
  flex: 1;
}

.btn-copy {
  padding: 8px 12px;
}

.client-actions {
  display: flex;
  gap: 8px;
  margin-top: 15px;
  flex-wrap: wrap;
}

.btn-small {
  padding: 6px 12px;
  font-size: 12px;
}

.credits-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  padding: 20px;
}

.credit-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
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

.tabs {
  display: flex;
  gap: 10px;
  padding: 20px;
  background: white;
  border-bottom: 2px solid #eee;
}

.tab {
  padding: 10px 20px;
  border: none;
  background: #f0f0f0;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.tab.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.tab-content {
  padding: 20px;
}

.add-button {
  margin-bottom: 20px;
}

.progress-bar {
  height: 8px;
  background: #eee;
  border-radius: 4px;
  overflow: hidden;
  margin: 10px 0;
}

.progress {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
}

@media (max-width: 768px) {
  .clients-grid {
    grid-template-columns: 1fr;
  }
  
  .dashboard-header {
    flex-direction: column;
    gap: 10px;
  }
}
</style>
```

---

## 🔌 API ENDPOINTS (Backend)

### **Créer Client avec Code Auto**

```python
# clients/models.py
from django.db import models
import uuid

class Client(models.Model):
    boutiquier = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    
    # CODE UNIQUE & PERMANENT
    access_code = models.CharField(max_length=20, unique=True, editable=False)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.access_code:
            self.access_code = self.generate_unique_code()
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_unique_code():
        """Générer un code unique: ABC-DE-001"""
        code = str(uuid.uuid4())[:8].upper()
        return f"{code}"
```

### **API Vérifier Code Client**

```python
# clients/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def verify_client_code(request):
    """
    Vérifier le code d'accès client
    POST /api/clients/verify-code/
    {
        "code": "ABC-DE-001",
        "name": "Mamadou Traoré"
    }
    """
    code = request.data.get('code')
    name = request.data.get('name')
    
    try:
        client = Client.objects.get(
            access_code=code,
            is_active=True
        )
        
        # Vérifier que le nom correspond (minimum)
        # ou utiliser une regex pour fuzzy match
        if name.lower() not in client.name.lower():
            return Response(
                {'error': 'Le nom ne correspond pas'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({
            'client_id': client.id,
            'client_name': client.name,
            'boutiquier_id': client.boutiquier.id
        })
    
    except Client.DoesNotExist:
        return Response(
            {'error': 'Code invalide'},
            status=status.HTTP_404_NOT_FOUND
        )
```

---

## ✨ RÉSUMÉ FINAL

| Élément | Description |
|---------|------------|
| **Admin** | Crée les Boutiquiers |
| **Boutiquier** | Crée ses Clients + Crédits |
| **Client** | Utilise son Code Permanent |
| **Code Client** | Unique + Fixe + Jamais changé |
| **Génération** | Automatique à la création |
| **Accès** | Code + Nom (vérification) |
| **Visibilité** | Boutiquier voit le code du client |

---

## 🚀 FLUX COMPLET

```
1️⃣ Admin crée Boutiquier (Django admin ou Vue.js admin)
2️⃣ Boutiquier se connecte (username + password)
3️⃣ Boutiquier crée Client (code généré auto)
4️⃣ Boutiquier partage le code au Client
5️⃣ Client entre son code + nom
6️⃣ Client voit ses crédits
7️⃣ Code reste TOUJOURS le même ✅
```

