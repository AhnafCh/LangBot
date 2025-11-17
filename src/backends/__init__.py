"""
Backend managers for vector storage
"""
from .faiss_manager import vector_store_manager

# Lazy import for Supabase to avoid requiring supabase package when not used
def get_supabase_store():
    """Lazy load Supabase store only when needed"""
    from .supabase_manager import get_supabase_store as _get_store
    return _get_store()

__all__ = ["vector_store_manager", "get_supabase_store"]
