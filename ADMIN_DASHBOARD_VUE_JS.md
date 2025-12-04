# 🛠️ ADMIN DASHBOARD COMPLET - CRÉATION BOUTIQUIERS

## 📋 AJOUTER AU FICHIER index.html (dans le template)

Cherchez cette section :

```html
<!-- ADMIN DASHBOARD (Simple) -->
<div v-if="currentView === 'admin-dashboard'" class="fade-in">
    <div class="dashboard-header">
        <div class="header-left">
            <h1>🔧 Admin</h1>
            <p>Bienvenue {{ username }}</p>
        </div>
        <div class="header-right">
            <button @click="logout" class="btn btn-danger">Déconnexion</button>
        </div>
    </div>

    <div class="content">
        <div class="alert alert-success">
            ✅ Créer les boutiquiers via Django Admin: 
            <br>
            <strong>http://localhost:8000/admin/</strong>
            <br>
            Les boutiquiers créent leurs clients directement dans l'application.
        </div>
    </div>
</div>
```

**Remplacez par :**

```html
<!-- ADMIN DASHBOARD (COMPLET) -->
<div v-if="currentView === 'admin-dashboard'" class="fade-in">
    <div class="dashboard-header">
        <div class="header-left">
            <h1>🔧 Panneau Administrateur</h1>
            <p>Gestion complète du système</p>
        </div>
        <div class="header-right">
            <button @click="logout" class="btn btn-danger">Déconnexion</button>
        </div>
    </div>

    <!-- ONGLETS ADMIN -->
    <div class="tabs">
        <button @click="adminTab = 'boutiquiers'" :class="{ active: adminTab === 'boutiquiers' }" class="tab">
            👥 Boutiquiers
        </button>
        <button @click="adminTab = 'clients'" :class="{ active: adminTab === 'clients' }" class="tab">
            👤 Clients
        </button>
        <button @click="adminTab = 'credits'" :class="{ active: adminTab === 'credits' }" class="tab">
            💰 Crédits
        </button>
    </div>

    <div class="content">
        <!-- TAB 1: BOUTIQUIERS -->
        <div v-if="adminTab === 'boutiquiers'">
            <h2>👥 Gestion des Boutiquiers</h2>
            
            <button @click="showBoutiquierForm = true" class="btn btn-primary" style="margin-bottom: 20px;">
                ➕ Créer un Boutiquier
            </button>

            <!-- FORMULAIRE CRÉER BOUTIQUIER -->
            <div v-if="showBoutiquierForm" class="modal">
                <div class="modal-content">
                    <h3>Créer un Boutiquier</h3>
                    <form @submit.prevent="createBoutiquier">
                        <div class="form-group">
                            <label>Identifiant (username) *</label>
                            <input v-model="boutiquierForm.username" type="text" placeholder="ex: ali" required>
                        </div>
                        <div class="form-group">
                            <label>Email *</label>
                            <input v-model="boutiquierForm.email" type="email" placeholder="ex: ali@boutique.com" required>
                        </div>
                        <div class="form-group">
                            <label>Prénom *</label>
                            <input v-model="boutiquierForm.first_name" type="text" placeholder="Ali" required>
                        </div>
                        <div class="form-group">
                            <label>Nom *</label>
                            <input v-model="boutiquierForm.last_name" type="text" placeholder="Diallo" required>
                        </div>
                        <div class="form-group">
                            <label>Téléphone *</label>
                            <input v-model="boutiquierForm.phone" type="tel" placeholder="77 123 45 67" required>
                        </div>
                        <div class="form-group">
                            <label>Mot de passe *</label>
                            <input v-model="boutiquierForm.password" type="password" placeholder="••••••••" required>
                        </div>
                        <div class="form-group">
                            <label>Confirmer mot de passe *</label>
                            <input v-model="boutiquierForm.password_confirm" type="password" placeholder="••••••••" required>
                        </div>
                        
                        <div v-if="boutiquierError" class="alert alert-error">{{ boutiquierError }}</div>
                        
                        <div class="form-actions">
                            <button type="submit" class="btn btn-primary" :disabled="loadingBoutiquier">
                                {{ loadingBoutiquier ? 'Création...' : 'Créer' }}
                            </button>
                            <button type="button" @click="showBoutiquierForm = false" class="btn btn-secondary">
                                Annuler
                            </button>
                        </div>
                    </form>
                </div>
            </div>

            <!-- TABLEAU BOUTIQUIERS -->
            <div v-if="allBoutiquiers.length > 0" class="table-responsive" style="margin-top: 20px;">
                <table>
                    <thead>
                        <tr>
                            <th>Prénom Nom</th>
                            <th>Identifiant</th>
                            <th>Email</th>
                            <th>Téléphone</th>
                            <th>Clients</th>
                            <th>Crédits Total</th>
                            <th>Statut</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="bout in allBoutiquiers" :key="bout.id">
                            <td>{{ bout.first_name }} {{ bout.last_name }}</td>
                            <td><strong>{{ bout.username }}</strong></td>
                            <td>{{ bout.email }}</td>
                            <td>{{ bout.phone }}</td>
                            <td>{{ bout.clients_count }}</td>
                            <td>{{ formatCurrency(bout.total_owed) }}</td>
                            <td>
                                <span :class="'status-' + bout.status" class="credit-status">
                                    {{ bout.status }}
                                </span>
                            </td>
                            <td>
                                <button @click="viewBoutiquierDetails(bout)" class="btn btn-small btn-info">Voir</button>
                                <button @click="toggleBoutiquierActive(bout)" class="btn btn-small" 
                                    :class="bout.is_active ? 'btn-warning' : 'btn-success'">
                                    {{ bout.is_active ? '🔒 Désactiver' : '🔓 Activer' }}
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div v-else class="alert alert-error" style="margin-top: 20px;">
                Aucun boutiquier créé
            </div>
        </div>

        <!-- TAB 2: CLIENTS -->
        <div v-if="adminTab === 'clients'">
            <h2>👤 Tous les Clients</h2>
            
            <div class="table-responsive" style="margin-top: 20px;">
                <table>
                    <thead>
                        <tr>
                            <th>Nom</th>
                            <th>Boutiquier</th>
                            <th>Téléphone</th>
                            <th>Code</th>
                            <th>Statut</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="client in allClients" :key="client.id">
                            <td>{{ client.name }}</td>
                            <td>{{ client.boutiquier_name }}</td>
                            <td>{{ client.phone }}</td>
                            <td><strong>{{ client.access_code }}</strong></td>
                            <td>
                                <span :class="'status-' + client.status" class="credit-status">
                                    {{ client.status }}
                                </span>
                            </td>
                            <td>
                                <button @click="toggleClientActive(client)" class="btn btn-small" 
                                    :class="client.is_active ? 'btn-warning' : 'btn-success'">
                                    {{ client.is_active ? '🔒' : '🔓' }}
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- TAB 3: CRÉDITS -->
        <div v-if="adminTab === 'credits'">
            <h2>💰 Tous les Crédits</h2>
            
            <div class="table-responsive" style="margin-top: 20px;">
                <table>
                    <thead>
                        <tr>
                            <th>Client</th>
                            <th>Montant</th>
                            <th>Payé</th>
                            <th>Restant</th>
                            <th>Produit</th>
                            <th>Statut</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="credit in allCredits" :key="credit.id">
                            <td>{{ credit.client_name }}</td>
                            <td>{{ formatCurrency(credit.amount) }}</td>
                            <td>{{ formatCurrency(credit.paid_amount) }}</td>
                            <td>{{ formatCurrency(credit.amount - credit.paid_amount) }}</td>
                            <td>{{ credit.product }}</td>
                            <td>
                                <span :class="'status-' + credit.status" class="credit-status">
                                    {{ credit.status }}
                                </span>
                            </td>
                            <td>
                                <button @click="toggleCreditActive(credit)" class="btn btn-small" 
                                    :class="credit.is_active ? 'btn-warning' : 'btn-success'">
                                    {{ credit.is_active ? '🔒' : '🔓' }}
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
```

---

## 🔧 **AJOUTER CES DATA & METHODS AU SCRIPT**

### **Dans data():**

```javascript
// Admin
adminTab: 'boutiquiers',
showBoutiquierForm: false,
allBoutiquiers: [],
allClients: [],
allCredits: [],

boutiquierForm: {
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    phone: '',
    password: '',
    password_confirm: ''
},

boutiquierError: '',
loadingBoutiquier: false,
```

### **Dans methods():**

```javascript
// ============ ADMIN: CHARGER TOUS LES DONNÉES ============

async loadAdminDashboard() {
    const token = localStorage.getItem('token');
    const headers = { Authorization: `Bearer ${token}` };
    
    try {
        // Charger boutiquiers
        const boutRes = await axios.get(
            'http://localhost:8000/api/admin/boutiquiers/',
            { headers }
        );
        this.allBoutiquiers = boutRes.data;
        
        // Charger clients (tous)
        const clientRes = await axios.get(
            'http://localhost:8000/api/clients/',
            { headers }
        );
        this.allClients = clientRes.data;
        
        // Charger crédits (tous)
        const creditRes = await axios.get(
            'http://localhost:8000/api/credits/',
            { headers }
        );
        this.allCredits = creditRes.data;
        
    } catch (error) {
        console.error('Erreur chargement admin:', error);
    }
},

// ============ CRÉER BOUTIQUIER ============

async createBoutiquier() {
    // Vérifier les mots de passe
    if (this.boutiquierForm.password !== this.boutiquierForm.password_confirm) {
        this.boutiquierError = 'Les mots de passe ne correspondent pas';
        return;
    }
    
    if (this.boutiquierForm.password.length < 8) {
        this.boutiquierError = 'Le mot de passe doit avoir au moins 8 caractères';
        return;
    }
    
    this.loadingBoutiquier = true;
    this.boutiquierError = '';
    
    try {
        const token = localStorage.getItem('token');
        const response = await axios.post(
            'http://localhost:8000/api/users/',
            {
                ...this.boutiquierForm,
                role: 'boutiquier'
            },
            {
                headers: { Authorization: `Bearer ${token}` }
            }
        );
        
        this.allBoutiquiers.push(response.data);
        this.showBoutiquierForm = false;
        this.boutiquierForm = {
            username: '',
            email: '',
            first_name: '',
            last_name: '',
            phone: '',
            password: '',
            password_confirm: ''
        };
        
    } catch (error) {
        if (error.response?.data?.username) {
            this.boutiquierError = 'Cet identifiant existe déjà';
        } else if (error.response?.data?.email) {
            this.boutiquierError = 'Cet email existe déjà';
        } else {
            this.boutiquierError = 'Erreur lors de la création';
        }
    } finally {
        this.loadingBoutiquier = false;
    }
},

// ============ DESACTIVER/ACTIVER BOUTIQUIER ============

async toggleBoutiquierActive(boutiquier) {
    if (!confirm('Êtes-vous sûr ?')) return;
    
    try {
        const token = localStorage.getItem('token');
        const newStatus = boutiquier.is_active ? 'inactive' : 'active';
        
        await axios.patch(
            `http://localhost:8000/api/admin/boutiquiers/${boutiquier.id}/toggle-status/`,
            { status: newStatus },
            { headers: { Authorization: `Bearer ${token}` } }
        );
        
        boutiquier.is_active = !boutiquier.is_active;
        boutiquier.status = newStatus;
        
    } catch (error) {
        alert('Erreur: ' + error.message);
    }
},

// ============ DESACTIVER/ACTIVER CLIENT ============

async toggleClientActive(client) {
    if (!confirm('Êtes-vous sûr ?')) return;
    
    try {
        const token = localStorage.getItem('token');
        const newStatus = client.is_active ? 'inactive' : 'active';
        
        await axios.patch(
            `http://localhost:8000/api/admin/clients/${client.id}/toggle-status/`,
            { status: newStatus },
            { headers: { Authorization: `Bearer ${token}` } }
        );
        
        client.is_active = !client.is_active;
        client.status = newStatus;
        
    } catch (error) {
        alert('Erreur: ' + error.message);
    }
},

// ============ DESACTIVER/ACTIVER CRÉDIT ============

async toggleCreditActive(credit) {
    if (!confirm('Êtes-vous sûr ?')) return;
    
    try {
        const token = localStorage.getItem('token');
        
        await axios.patch(
            `http://localhost:8000/api/admin/credits/${credit.id}/toggle-status/`,
            { is_active: !credit.is_active },
            { headers: { Authorization: `Bearer ${token}` } }
        );
        
        credit.is_active = !credit.is_active;
        
    } catch (error) {
        alert('Erreur: ' + error.message);
    }
},

// ============ VOIR DÉTAILS BOUTIQUIER ============

viewBoutiquierDetails(boutiquier) {
    alert(`Boutiquier: ${boutiquier.first_name} ${boutiquier.last_name}
Total dû: ${this.formatCurrency(boutiquier.total_owed)}
Payé: ${this.formatCurrency(boutiquier.paid_amount)}
Restant: ${this.formatCurrency(boutiquier.total_owed - boutiquier.paid_amount)}
Clients: ${boutiquier.clients_count}`);
},
```

### **Mettre à jour loginAdmin():**

```javascript
async loginAdmin() {
    this.loading = true;
    this.loginError = '';

    try {
        const response = await axios.post(
            'http://localhost:8000/api/users/token/',
            this.loginForm
        );

        if (!response.data.is_superuser) {
            this.loginError = 'Accès administrateur requis';
            return;
        }

        localStorage.setItem('token', response.data.access);
        localStorage.setItem('user_role', 'admin');
        localStorage.setItem('username', response.data.username);

        this.isAuthenticated = true;
        this.userRole = 'admin';
        this.username = response.data.username;

        // ← CHARGER LES DONNÉES ADMIN
        await this.loadAdminDashboard();
        
        this.currentView = 'admin-dashboard';

    } catch (error) {
        this.loginError = 'Identifiants incorrects';
    } finally {
        this.loading = false;
    }
}
```

---

## 📡 **API ENDPOINT À VÉRIFIER**

L'endpoint pour créer un utilisateur doit accepter `role`:

```python
# users/serializers.py

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'phone', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(
            password=password,
            **validated_data
        )
        return user
```

---

## ✨ **RÉSULTAT APRÈS HÉBERGEMENT**

Après hébergement, vous pouvez:

1. ✅ Accéder à l'app Vue.js
2. ✅ Login comme Admin
3. ✅ Créer les boutiquiers directement dans l'app
4. ✅ Gérer tous les clients et crédits
5. ✅ Désactiver/Activer sans suppression
6. ✅ **PAS BESOIN DE DJANGO ADMIN** 🎉

