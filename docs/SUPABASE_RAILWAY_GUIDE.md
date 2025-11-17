# 🚀 Supabase + Railway Deployment Guide

## Overview
This guide will help you deploy your RAG system using:
- **Supabase**: Cloud PostgreSQL with pgvector for scalable vector storage
- **Railway**: Easy deployment platform for your FastAPI backend

## 🎯 Benefits of This Setup

### Supabase (vs Local FAISS):
✅ **Persistent Storage** - Data survives restarts  
✅ **Scalable** - Handle thousands of documents  
✅ **Fast Queries** - Optimized pgvector indexes  
✅ **File Storage** - Built-in storage for documents  
✅ **Real-time** - WebSocket support for live updates  
✅ **Backup** - Automatic backups included  

### Railway (vs Local Server):
✅ **Auto-Deploy** - Push to git, auto-deploys  
✅ **HTTPS** - Free SSL certificates  
✅ **Custom Domain** - Use your own domain  
✅ **Scale** - Handle more users  
✅ **Monitoring** - Built-in logs and metrics  
✅ **Zero DevOps** - No server management  

---

## Part 1: Setting Up Supabase

### Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Sign up / Sign in
3. Click **"New Project"**
4. Fill in:
   - **Name**: LangBot (or your choice)
   - **Database Password**: Create a strong password (save it!)
   - **Region**: Choose closest to your users
5. Click **"Create new project"** (takes ~2 minutes)

### Step 2: Set Up Database Schema

1. In your Supabase dashboard, click **"SQL Editor"** (left sidebar)
2. Click **"New query"**
3. Copy the entire contents of `setup_supabase.sql`
4. Paste into the SQL editor
5. Click **"Run"** (or press Ctrl+Enter)
6. You should see success messages

### Step 3: Create Storage Bucket

1. Click **"Storage"** in left sidebar
2. Click **"Create a new bucket"**
3. **Name**: `documents`
4. **Public bucket**: Leave unchecked (private)
5. Click **"Create bucket"**

### Step 4: Get API Credentials

1. Click **"Project Settings"** (gear icon, bottom left)
2. Click **"API"** in settings menu
3. Copy these values:
   - **Project URL** (looks like: `https://xxxxx.supabase.co`)
   - **anon public key** OR **service_role key** (service_role recommended for backend)

### Step 5: Update Your .env File

Add to your `.env` file:
```env
USE_SUPABASE=true
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_service_role_key_here
```

---

## Part 2: Deploying to Railway

### Step 1: Prepare Your Repository

1. **Create a GitHub repository** (if you haven't):
   ```bash
   git init
   git add .
   git commit -m "Initial commit with Supabase integration"
   git branch -M main
   git remote add origin https://github.com/yourusername/LangBot.git
   git push -u origin main
   ```

### Step 2: Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Click **"Start a New Project"**
3. Click **"Deploy from GitHub repo"**
4. Authorize Railway to access your GitHub
5. Select your **LangBot** repository
6. Railway will automatically detect it's a Python app

### Step 3: Configure Environment Variables

1. In Railway dashboard, click on your project
2. Click **"Variables"** tab
3. Add these environment variables:

```
OPENAI_API_KEY=your_openai_key
USE_SUPABASE=true
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_service_role_key
```

4. Click **"Save"**

### Step 4: Deploy

1. Railway will automatically build and deploy
2. Wait for deployment to complete (~2-5 minutes)
3. You'll see a **"Deployment successful"** message
4. Click **"Settings"** → **"Generate Domain"** to get a public URL

### Step 5: Test Your Deployment

1. Visit: `https://your-app.railway.app/health`
2. You should see: `{"status": "healthy", "backend": "Supabase"}`
3. Visit: `https://your-app.railway.app/` to access the web interface

---

## Part 3: Migration from Local to Supabase

### Option A: Keep Both (Recommended)

The system supports both backends simultaneously:

**Local Development** (`.env`):
```env
USE_SUPABASE=false
```

**Production** (Railway):
```env
USE_SUPABASE=true
```

### Option B: Migrate Existing Documents

If you have documents in local FAISS, upload them through the web interface:

1. Go to `http://localhost:8000` (or your Railway URL)
2. Upload each document using the upload button
3. System will automatically vectorize and store in Supabase

---

## Part 4: Using the Unified System

### Switching Between Backends

**In your `.env` file:**

```env
# Use Local FAISS (development)
USE_SUPABASE=false

# Use Supabase (production)
USE_SUPABASE=true
```

### API Endpoints (Same for Both Backends)

- `POST /upload/` - Upload documents
- `GET /query/?query=your_question` - Query RAG system
- `GET /documents/` - List all documents
- `DELETE /documents/{doc_id}` - Delete document
- `GET /health` - Health check
- `GET /config` - Check current configuration

---

## 📊 Comparison: Local vs Supabase

| Feature | Local FAISS | Supabase |
|---------|-------------|----------|
| Setup Complexity | Low | Medium |
| Scalability | Limited | High |
| Data Persistence | File-based | Database |
| Concurrent Users | 1-10 | Unlimited |
| Backup | Manual | Automatic |
| Cost | Free | Free tier + paid |
| Vector Search | CPU-based | GPU-accelerated |
| File Storage | Local disk | Cloud storage |

---

## 🔧 Troubleshooting

### Supabase Issues

**"Extension vector does not exist"**
→ Make sure you ran `setup_supabase.sql` completely

**"Bucket not found"**
→ Create `documents` bucket in Supabase Storage

**"Permission denied"**
→ Check RLS policies in Supabase dashboard

### Railway Issues

**"Build failed"**
→ Check build logs, ensure all dependencies in `requirements.txt`

**"Application not responding"**
→ Check if PORT environment variable is set (Railway sets it automatically)

**"Import errors"**
→ Make sure `gunicorn` is in `requirements.txt`

### Connection Issues

**"Cannot connect to Supabase"**
→ Verify SUPABASE_URL and SUPABASE_KEY in environment variables

**"CORS errors"**
→ Add your Railway domain to allowed origins in `main.py`

---

## 🎉 You're Done!

Your RAG system is now:
- ✅ Deployed to the cloud (Railway)
- ✅ Using scalable vector database (Supabase)
- ✅ Accessible from anywhere via HTTPS
- ✅ Ready for production use

### Next Steps:

1. **Custom Domain**: Add your own domain in Railway settings
2. **Authentication**: Add user login using Supabase Auth
3. **Rate Limiting**: Implement rate limiting for API endpoints
4. **Monitoring**: Set up error tracking with Sentry
5. **Analytics**: Track usage with PostHog or similar

---

## 📚 Additional Resources

- [Supabase Documentation](https://supabase.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

---

## 💰 Cost Estimates

### Supabase Free Tier:
- 500 MB database
- 1 GB file storage
- 2 GB bandwidth
- **Enough for: ~10,000 document chunks**

### Railway Free Tier:
- $5 free credits/month
- ~500 hours of runtime
- **Enough for: Small to medium traffic**

### When to Upgrade:
- **Supabase Pro** ($25/mo): 8 GB database, 100 GB storage
- **Railway Usage-based**: Pay for what you use (~$20-50/mo for moderate traffic)

---

## 🆘 Need Help?

- Check Railway logs: Railway dashboard → Deployments → View logs
- Check Supabase logs: Supabase dashboard → Logs
- Test locally first: Set `USE_SUPABASE=false` to test with FAISS

Good luck with your deployment! 🚀
