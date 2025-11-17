"""
Unified endpoints supporting both FAISS (local) and Supabase (cloud) backends
"""
from fastapi import APIRouter, HTTPException, UploadFile, File
from src.core import get_rag_response
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# Determine which backend to use
USE_SUPABASE = os.getenv("USE_SUPABASE", "false").lower() == "true"

# Ensure data directory exists for local storage
DATA_DIR = "data"
Path(DATA_DIR).mkdir(parents=True, exist_ok=True)


@router.get("/query/")
async def query_rag_system(query: str):
    """Query the RAG system"""
    try:
        response = await get_rag_response(query)
        return {"query": query, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    """Upload a new document and automatically vectorize it"""
    try:
        # Validate filename exists
        if not file.filename:
            raise HTTPException(status_code=400, detail="Filename is required")
        
        # Validate file type
        if not file.filename.endswith(('.txt', '.md', '.text')):
            raise HTTPException(
                status_code=400, 
                detail="Only text files (.txt, .md, .text) are supported"
            )
        
        # Read file content
        file_content = await file.read()
        
        if USE_SUPABASE:
            # Use Supabase for storage and vectorization
            from src.backends import get_supabase_store
            
            store = get_supabase_store()
            result = await store.add_document(file_content, file.filename)
        else:
            # Use local FAISS storage
            from src.backends import vector_store_manager
            import shutil
            
            # Save file locally
            file_path = os.path.join(DATA_DIR, file.filename)
            with open(file_path, "wb") as buffer:
                buffer.write(file_content)
            
            # Add to vector store
            result = vector_store_manager.add_document(file_path, file.filename)
        
        return {
            "filename": file.filename,
            "status": result["status"],
            "message": result["message"],
            "document_id": result.get("document_id"),
            "chunk_count": result.get("chunk_count"),
            "backend": "Supabase" if USE_SUPABASE else "Local FAISS"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading document: {str(e)}")


@router.get("/documents/")
async def list_documents():
    """Get list of all documents in the vector store"""
    try:
        if USE_SUPABASE:
            from src.backends import get_supabase_store
            store = get_supabase_store()
            documents = await store.get_all_documents()
        else:
            from src.backends import vector_store_manager
            documents = vector_store_manager.get_all_documents()
        
        return {
            "count": len(documents),
            "documents": documents,
            "backend": "Supabase" if USE_SUPABASE else "Local FAISS"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    """Remove a document"""
    try:
        if USE_SUPABASE:
            from src.backends import get_supabase_store
            store = get_supabase_store()
            result = await store.delete_document(doc_id)
        else:
            from src.backends import vector_store_manager
            result = vector_store_manager.remove_document(doc_id)
        
        if result["status"] == "error":
            raise HTTPException(status_code=404, detail=result["message"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint for Railway"""
    return {
        "status": "healthy",
        "backend": "Supabase" if USE_SUPABASE else "Local FAISS",
        "version": "2.0"
    }


@router.get("/config")
async def get_config():
    """Get current configuration"""
    return {
        "backend": "Supabase" if USE_SUPABASE else "Local FAISS",
        "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
        "supabase_configured": bool(os.getenv("SUPABASE_URL")) and bool(os.getenv("SUPABASE_KEY"))
    }
