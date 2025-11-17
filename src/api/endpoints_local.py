from fastapi import APIRouter, HTTPException, UploadFile, File
from rag import get_rag_response
from vector_store_manager import vector_store_manager
import os
import shutil
from pathlib import Path

router = APIRouter()

# Ensure data directory exists
DATA_DIR = "data"
Path(DATA_DIR).mkdir(parents=True, exist_ok=True)

@router.get("/query/")
async def query_rag_system(query: str):
    try:
        # Pass the query string to your RAG system and return the response
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
        
        # Validate file type (only text files)
        if not file.filename.endswith(('.txt', '.md', '.text')):
            raise HTTPException(
                status_code=400, 
                detail="Only text files (.txt, .md, .text) are supported"
            )
        
        # Save the uploaded file
        file_path = os.path.join(DATA_DIR, file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Add document to vector store
        result = vector_store_manager.add_document(file_path, file.filename)
        
        return {
            "filename": file.filename,
            "status": result["status"],
            "message": result["message"],
            "document_id": result.get("document_id"),
            "chunk_count": result.get("chunk_count")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading document: {str(e)}")

@router.get("/documents/")
async def list_documents():
    """Get list of all documents in the vector store"""
    try:
        documents = vector_store_manager.get_all_documents()
        return {
            "count": len(documents),
            "documents": documents
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    """Remove a document from the metadata"""
    try:
        result = vector_store_manager.remove_document(doc_id)
        if result["status"] == "error":
            raise HTTPException(status_code=404, detail=result["message"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))