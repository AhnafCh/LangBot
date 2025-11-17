# Deployment Configuration

Deployment configuration files for Railway and other platforms.

## Files

### `Procfile`
Railway/Heroku process file.

**Content:**
```
web: gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

Tells Railway how to start the application in production.

---

### `railway.json`
Railway-specific configuration.

**Specifies:**
- Build system (NIXPACKS)
- Start command
- Restart policy
- Auto-scaling settings

---

### `runtime.txt`
Python version specification for deployment platforms.

**Content:**
```
python-3.11.*
```

Ensures Railway uses Python 3.11.

---

## Deployment

### Railway Deployment:

1. **Connect GitHub:**
   - Push your code to GitHub
   - Go to [railway.app](https://railway.app)
   - Create new project from GitHub repo

2. **Environment Variables:**
   Add in Railway dashboard:
   ```
   OPENAI_API_KEY=your_key
   USE_SUPABASE=true
   SUPABASE_URL=your_url
   SUPABASE_KEY=your_key
   ```

3. **Deploy:**
   - Railway automatically detects Python
   - Uses these config files
   - Deploys on git push

4. **Domain:**
   - Railway generates a public URL
   - Or add custom domain in settings

---

## Notes

- Files in this directory are used by deployment platforms
- `Procfile` must be in project root for Railway (copy there during deployment)
- Don't modify unless you understand deployment configuration
