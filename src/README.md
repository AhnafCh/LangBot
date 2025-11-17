# Source Code (`src/`)

This directory contains all the application source code organized by functionality.

## Structure

```
src/
├── __init__.py           # Package initialization
├── main.py               # Main unified app (supports both backends)
├── main_local.py         # Original local-only app (legacy)
├── api/                  # API endpoints and routes
│   ├── __init__.py
│   ├── endpoints.py      # Unified endpoints (FAISS + Supabase)
│   └── endpoints_local.py# Original local-only endpoints (legacy)
├── core/                 # Core RAG system logic
│   ├── __init__.py
│   ├── rag.py           # Unified RAG system (FAISS + Supabase)
│   └── rag_local.py     # Original local-only RAG (legacy)
└── backends/            # Vector store backends
    ├── __init__.py
    ├── faiss_manager.py     # Local FAISS vector store
    └── supabase_manager.py  # Supabase cloud vector store
```

## Modules

### `api/`
Contains all FastAPI endpoints and route handlers.

- **endpoints.py**: Unified API supporting both FAISS and Supabase backends
- **endpoints_local.py**: Legacy local-only version

### `core/`
Core RAG (Retrieval-Augmented Generation) system logic.

- **rag.py**: Main RAG implementation with backend switching
- **rag_local.py**: Legacy local-only implementation

### `backends/`
Vector store management implementations.

- **faiss_manager.py**: Local FAISS vector database manager
- **supabase_manager.py**: Supabase PostgreSQL + pgvector manager

## Usage

Import from src package:

```python
# From root directory
from src.api import router
from src.core import get_rag_response
from src.backends import vector_store_manager, get_supabase_store
```

## Legacy Files

Files with `_local` suffix are the original implementations before adding Supabase support. They are kept for reference and backwards compatibility.
