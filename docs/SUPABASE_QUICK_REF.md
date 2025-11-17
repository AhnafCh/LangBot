# 🎯 Quick Reference: Supabase + Railway Setup

## ⚡ Super Quick Start

### 1. Setup Supabase (5 minutes)
```bash
1. Go to supabase.com → New Project
2. SQL Editor → Paste setup_supabase.sql → Run
3. Storage → Create bucket "documents"
4. Settings → API → Copy URL and service_role key
```

### 2. Update .env
```env
USE_SUPABASE=true
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_service_role_key
```

### 3. Deploy to Railway (3 minutes)
```bash
1. Push code to GitHub
2. railway.app → New Project → Deploy from GitHub
3. Add environment variables (same as .env)
4. Generate domain
```

## 🔄 Switch Between Backends

```bash
# Switch to local (development)
python switch_backend.py local

# Switch to Supabase (production)
python switch_backend.py supabase

# Check current backend
python switch_backend.py status
```

## 📦 Install New Dependencies

```bash
# Activate venv first
.\venv\Scripts\Activate.ps1

# Install
pip install supabase psycopg2-binary pgvector gunicorn
```

## 🚀 Test Locally with Supabase

```bash
# 1. Switch to Supabase
python switch_backend.py supabase

# 2. Use unified main file
uvicorn main_unified:app --reload

# 3. Upload a document and test
```

## 📁 File Structure After Setup

```
LangBot/
├── main.py                    # Original (FAISS only)
├── main_unified.py           # New (Both FAISS & Supabase) ⭐
├── endpoints.py              # Original (FAISS only)
├── endpoints_unified.py      # New (Both backends) ⭐
├── rag.py                    # Original (FAISS only)
├── rag_unified.py           # New (Both backends) ⭐
├── vector_store_manager.py  # Local FAISS manager
├── supabase_manager.py      # Supabase manager ⭐
├── setup_supabase.sql       # Database schema ⭐
├── switch_backend.py        # Backend switcher ⭐
├── Procfile                  # Railway config ⭐
├── railway.json             # Railway config ⭐
└── SUPABASE_RAILWAY_GUIDE.md # Full guide ⭐
```

## 🎨 Backend Comparison

| Feature | Command |
|---------|---------|
| **Local FAISS** | `python switch_backend.py local` |
| **Supabase Cloud** | `python switch_backend.py supabase` |
| **Check Status** | `python switch_backend.py status` |

## ⚙️ Environment Variables

```env
# Always Required
OPENAI_API_KEY=sk-...

# Backend Selection
USE_SUPABASE=false              # or true

# Supabase (only if USE_SUPABASE=true)
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJ...
```

## 🧪 Testing Checklist

- [ ] Supabase database created
- [ ] setup_supabase.sql executed
- [ ] Storage bucket "documents" created
- [ ] .env updated with Supabase credentials
- [ ] Dependencies installed
- [ ] Switch to Supabase: `python switch_backend.py supabase`
- [ ] Start server: `uvicorn main_unified:app --reload`
- [ ] Upload test document
- [ ] Query works
- [ ] Documents list shows
- [ ] Check Supabase dashboard for data

## 🚨 Common Issues

**ImportError: No module named 'supabase'**
```bash
pip install supabase
```

**"SUPABASE_URL not set"**
```bash
python switch_backend.py status  # Check config
```

**Supabase connection fails**
- Check if URL/Key are correct in .env
- Verify network connection
- Check Supabase project is active

## 🎯 Deployment Steps

1. **Test locally with Supabase** ✓
2. **Commit to GitHub** ✓
3. **Deploy to Railway** ✓
4. **Set env variables on Railway** ✓
5. **Generate domain** ✓
6. **Test production URL** ✓

## 📊 Cost Reference

- **Local**: $0 (just your machine)
- **Supabase Free**: $0/month (500MB DB, 1GB storage)
- **Railway Free**: $5 credits/month (~500 hours)
- **Total Free Tier**: Perfect for testing and small projects

## 🎓 Learn More

- Full guide: `SUPABASE_RAILWAY_GUIDE.md`
- Setup help: `README.md`
- Quick start: `QUICK_START.md`

---

**Ready to deploy?** Follow `SUPABASE_RAILWAY_GUIDE.md` for step-by-step instructions!
