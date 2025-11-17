# Scripts Directory

Utility scripts for managing the RAG system.

## Scripts

### `check_setup.py`
Validates your environment configuration.

**Usage:**
```bash
python scripts/check_setup.py
```

**Checks:**
- .env file exists
- OpenAI API key is set
- Required packages installed
- Vector store status
- Supabase configuration (if enabled)

---

### `init_vector_store.py`
Initializes the local FAISS vector store with existing documents.

**Usage:**
```bash
python scripts/init_vector_store.py
```

**What it does:**
- Scans `./data/` directory
- Processes all `.txt`, `.md`, `.text` files
- Creates embeddings
- Stores in local FAISS vector database

---

### `switch_backend.py`
Switches between Local FAISS and Supabase backends.

**Usage:**
```bash
# Check current backend
python scripts/switch_backend.py status

# Switch to local FAISS
python scripts/switch_backend.py local

# Switch to Supabase cloud
python scripts/switch_backend.py supabase
```

**Note:** Restart the server after switching backends.

---

## Running Scripts

All scripts should be run from the **project root** directory:

```bash
# From D:\LangBot\
python scripts/check_setup.py
python scripts/init_vector_store.py
python scripts/switch_backend.py status
```

## Requirements

Scripts automatically add the project root to Python path, so imports work correctly.
