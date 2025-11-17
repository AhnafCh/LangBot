# Configuration Directory

Configuration files and templates for the RAG system.

## Files

### `.env.template`
Template for environment variables.

**Copy this to create your `.env` file in the project root:**

```bash
# In project root (D:\LangBot/)
cp config/.env.template .env
# Then edit .env with your actual values
```

**Required variables:**
- `OPENAI_API_KEY` - Your OpenAI API key
- `USE_SUPABASE` - Set to "true" for cloud, "false" for local
- `SUPABASE_URL` - Your Supabase project URL (if using Supabase)
- `SUPABASE_KEY` - Your Supabase service role key (if using Supabase)

---

### `setup_supabase.sql`
PostgreSQL schema for Supabase database.

**Usage:**
1. Go to your Supabase dashboard
2. Open SQL Editor
3. Copy entire contents of this file
4. Paste and run in SQL Editor

**What it creates:**
- `pgvector` extension
- `documents` table for metadata
- `document_chunks` table with vector embeddings
- Indexes for fast similarity search
- RPC function for vector search
- Row Level Security policies

---

## Notes

- The actual `.env` file should be in the **project root**, not in this directory
- Never commit `.env` file with real API keys to git
- `.env.template` is safe to commit (no real secrets)
