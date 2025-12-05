# 📊 RENDER DEPLOYMENT - FLOWCHART

```
┌─────────────────────────────────────────────────────────┐
│  VOTRE MACHINE LOCALE                                   │
│  ✅ Code complet sur GitHub: mouhamedia/samacahier      │
│  ✅ Fichiers prêts: Procfile, requirements.txt          │
│  ✅ PostgreSQL local: localhost:5432                    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  GITHUB REPOSITORY                                      │
│  📦 https://github.com/mouhamedia/samacahier            │
│  📌 Branch: main (latest commit: f464a1f)               │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  RENDER.COM SETUP                                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1️⃣  WEB SERVICE (Django API)                          │
│      📍 URL: https://samacahier-api.onrender.com        │
│      ⚙️ Runtime: Python 3                              │
│      🔄 Auto-deploys on push to GitHub                 │
│                                                         │
│  2️⃣  PostgreSQL DATABASE (Managed)                     │
│      📍 URL: postgresql://user:pass@host:5432/db       │
│      💾 Auto-backups included                          │
│      ✅ 90 days free, then $15/month                   │
│                                                         │
│  3️⃣  ENVIRONMENT VARIABLES                             │
│      🔐 DEBUG=False                                    │
│      🔐 SECRET_KEY=<secure_key>                        │
│      🔐 DATABASE_URL=<rendered_pg_url>                 │
│      🔐 ALLOWED_HOSTS=samacahier-api.onrender.com      │
│                                                         │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  DEPLOYMENT PROCESS                                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Step 1: Build                                          │
│    ↳ Clone repo from GitHub                            │
│    ↳ Install requirements: gunicorn, psycopg2, etc      │
│    ↳ Duration: ~1-2 minutes                            │
│                                                         │
│  Step 2: Migrations                                     │
│    ↳ python manage.py migrate                          │
│    ↳ Apply database schema                             │
│    ↳ Duration: ~30 seconds                             │
│                                                         │
│  Step 3: Static Files                                  │
│    ↳ python manage.py collectstatic                    │
│    ↳ Prepare CSS, JS assets                            │
│    ↳ Duration: ~20 seconds                             │
│                                                         │
│  Step 4: Start Service                                 │
│    ↳ gunicorn samacahier.wsgi                          │
│    ↳ Server listening on port 8000                     │
│    ↳ Duration: ~10 seconds                             │
│                                                         │
│  🎉 TOTAL TIME: ~3-4 minutes                            │
│                                                         │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  YOUR LIVE API 🌐                                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  🔗 Base URL: https://samacahier-api.onrender.com      │
│                                                         │
│  📍 Endpoints Available:                                │
│     POST   /api/users/token/          (Login)          │
│     GET    /api/clients/access/       (Client access)  │
│     POST   /api/admin/boutiquiers/    (Create user)    │
│     GET    /api/credits/              (List credits)   │
│     GET    /api/dashboard/            (Dashboard)      │
│                                                         │
│  ✅ HTTPS enabled by default                           │
│  ✅ PostgreSQL connected                               │
│  ✅ JWT authentication working                         │
│  ✅ CORS configured                                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 🔄 AUTO-DEPLOYMENT WORKFLOW

```
┌─────────────────────┐
│  Modify code        │
│  Commit to GitHub   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Push to main       │
│  git push           │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Render detects     │
│  new commit         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Automatic redeploy │
│  (3-4 min)          │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  ✅ Live update!    │
│  No downtime!       │
└─────────────────────┘
```

## 💰 PRICING

| Service | Free | Paid |
|---------|------|------|
| **Web Service (Django)** | ✅ Included | - |
| **PostgreSQL (90 days)** | ✅ $0 | $15/month after |
| **Custom Domain** | ❌ subdomain.onrender.com | ✅ $12/month |
| **Uptime** | 99.9% | 99.95% |
| **CPU/Memory** | Shared | Dedicated |

## ⚡ PERFORMANCE

- **Cold Start**: ~5-10 seconds (first request after idle)
- **Response Time**: ~50-200ms (after warm)
- **Database Queries**: ~10-50ms
- **Region**: US, EU, Asia (choose closest)

## 🛠️ MAINTENANCE

### View Logs
```
Render Dashboard → Web Service → Logs
Real-time monitoring of errors and requests
```

### Manual Redeploy
```
Render Dashboard → Web Service → Deploys → Deploy latest commit
```

### Scale Up (Optional)
```
Render Dashboard → Web Service → Instance Type
Free → Pro ($7/month) for better performance
```

## ✅ POST-DEPLOYMENT CHECKLIST

- [ ] API is running on https://samacahier-api.onrender.com
- [ ] Database connection working (check Logs)
- [ ] Migrations applied successfully
- [ ] Test endpoint: POST /api/users/token/
- [ ] Login works with admin credentials
- [ ] Boutiquiers can connect
- [ ] Clients can access via code
- [ ] CORS working for frontend
- [ ] No 500 errors in logs
- [ ] Email notifications working (optional)

## 🚨 TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| **App won't start** | Check Logs for errors, verify DATABASE_URL |
| **Database error** | Ensure PostgreSQL URL is correct, DB is "Available" |
| **ALLOWED_HOSTS error** | Add domain to environment variables |
| **Slow response** | Upgrade from Free to Pro, or optimize queries |
| **Static files missing** | Run `collectstatic` via Shell |

---

**Total Setup Time**: ~25 minutes ⏱️
**Your API Lives**: https://samacahier-api.onrender.com 🎉
