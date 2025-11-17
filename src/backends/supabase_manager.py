"""
Supabase Vector Store Manager with pgvector
Optimized for scalable document storage and retrieval
"""
import os
import hashlib
from typing import Optional, List, Dict, Any
from datetime import datetime
from dotenv import load_dotenv

from supabase import create_client, Client
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.documents import Document

# Load environment variables
load_dotenv()


class SupabaseVectorStore:
    """Manages document storage and vector search using Supabase + pgvector"""
    
    def __init__(self):
        # Initialize Supabase client
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError(
                "SUPABASE_URL and SUPABASE_KEY must be set in .env file. "
                "Get these from your Supabase project settings."
            )
        
        self.client: Client = create_client(supabase_url, supabase_key)
        self.embeddings = OpenAIEmbeddings()
        self.bucket_name = "documents"
        
        # Ensure storage bucket exists
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        """Create storage bucket if it doesn't exist"""
        try:
            buckets = self.client.storage.list_buckets()
            if not any(b.name == self.bucket_name for b in buckets):
                self.client.storage.create_bucket(self.bucket_name, {"public": False})
        except Exception as e:
            print(f"Note: Storage bucket check: {e}")
    
    def _calculate_file_hash(self, content: bytes) -> str:
        """Calculate SHA256 hash of file content"""
        return hashlib.sha256(content).hexdigest()
    
    async def document_exists(self, file_hash: str) -> tuple[bool, Optional[str]]:
        """
        Check if document already exists
        Returns: (exists: bool, document_id: Optional[str])
        """
        try:
            result = self.client.table("documents").select("id, document_id").eq("file_hash", file_hash).execute()
            
            if result.data and len(result.data) > 0:
                return True, result.data[0]["document_id"]
            return False, None
        except Exception as e:
            print(f"Error checking document: {e}")
            return False, None
    
    async def add_document(
        self, 
        file_content: bytes, 
        filename: str,
        chunk_size: int = 200,
        chunk_overlap: int = 20
    ) -> Dict[str, Any]:
        """
        Add a document to Supabase storage and vector database
        """
        try:
            # Calculate file hash for duplicate detection
            file_hash = self._calculate_file_hash(file_content)
            
            # Check for duplicates
            exists, existing_id = await self.document_exists(file_hash)
            if exists:
                return {
                    "status": "duplicate",
                    "message": f"Document already exists with ID: {existing_id}",
                    "document_id": existing_id
                }
            
            # Generate unique document ID
            doc_id = f"doc_{file_hash[:16]}"
            
            # Upload file to Supabase Storage
            file_path = f"{doc_id}/{filename}"
            storage_result = self.client.storage.from_(self.bucket_name).upload(
                file_path, 
                file_content,
                {"content-type": "text/plain"}
            )
            
            # Decode content for processing
            text_content = file_content.decode('utf-8')
            
            # Split text into chunks
            from langchain_text_splitters import RecursiveCharacterTextSplitter
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size, 
                chunk_overlap=chunk_overlap
            )
            chunks = splitter.split_text(text_content)
            
            # Generate embeddings for all chunks
            embeddings_list = self.embeddings.embed_documents(chunks)
            
            # Insert document metadata
            doc_metadata = {
                "document_id": doc_id,
                "filename": filename,
                "file_hash": file_hash,
                "file_path": file_path,
                "chunk_count": len(chunks),
                "created_at": datetime.utcnow().isoformat()
            }
            
            self.client.table("documents").insert(doc_metadata).execute()
            
            # Insert chunks with embeddings into vector table
            chunk_records = []
            for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings_list)):
                chunk_records.append({
                    "document_id": doc_id,
                    "chunk_index": idx,
                    "content": chunk,
                    "embedding": embedding,
                    "metadata": {"filename": filename, "chunk": idx}
                })
            
            # Batch insert chunks
            self.client.table("document_chunks").insert(chunk_records).execute()
            
            return {
                "status": "success",
                "message": f"Document added successfully with {len(chunks)} chunks",
                "document_id": doc_id,
                "chunk_count": len(chunks),
                "file_path": file_path
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error adding document: {str(e)}",
                "document_id": None
            }
    
    async def similarity_search(self, query: str, k: int = 2) -> List[Document]:
        """
        Perform similarity search using pgvector
        """
        try:
            # Generate query embedding
            query_embedding = self.embeddings.embed_query(query)
            
            # Use Supabase RPC for vector similarity search
            # This requires a custom PostgreSQL function (see setup_supabase.sql)
            result = self.client.rpc(
                "match_documents",
                {
                    "query_embedding": query_embedding,
                    "match_count": k
                }
            ).execute()
            
            # Convert results to LangChain Document objects
            documents = []
            for row in result.data:
                doc = Document(
                    page_content=row["content"],
                    metadata={
                        "document_id": row["document_id"],
                        "chunk_index": row["chunk_index"],
                        "similarity": row["similarity"],
                        **row.get("metadata", {})
                    }
                )
                documents.append(doc)
            
            return documents
            
        except Exception as e:
            print(f"Error in similarity search: {e}")
            return []
    
    async def get_all_documents(self) -> List[Dict[str, Any]]:
        """Get list of all documents"""
        try:
            result = self.client.table("documents").select("*").order("created_at", desc=True).execute()
            return result.data
        except Exception as e:
            print(f"Error fetching documents: {e}")
            return []
    
    async def delete_document(self, doc_id: str) -> Dict[str, Any]:
        """Delete a document and its chunks"""
        try:
            # Delete from storage
            doc_result = self.client.table("documents").select("file_path").eq("document_id", doc_id).execute()
            
            if doc_result.data and len(doc_result.data) > 0:
                file_path = doc_result.data[0]["file_path"]
                try:
                    self.client.storage.from_(self.bucket_name).remove([file_path])
                except:
                    pass  # File might not exist
            
            # Delete chunks (cascades if foreign key is set up)
            self.client.table("document_chunks").delete().eq("document_id", doc_id).execute()
            
            # Delete document metadata
            self.client.table("documents").delete().eq("document_id", doc_id).execute()
            
            return {
                "status": "success",
                "message": f"Document {doc_id} deleted successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error deleting document: {str(e)}"
            }
    
    async def get_document_content(self, doc_id: str) -> Optional[str]:
        """Retrieve original document content from storage"""
        try:
            doc_result = self.client.table("documents").select("file_path").eq("document_id", doc_id).execute()
            
            if doc_result.data and len(doc_result.data) > 0:
                file_path = doc_result.data[0]["file_path"]
                content = self.client.storage.from_(self.bucket_name).download(file_path)
                return content.decode('utf-8')
            return None
        except Exception as e:
            print(f"Error retrieving document: {e}")
            return None


# Global instance (will be created when imported)
supabase_vector_store = None

def get_supabase_store() -> SupabaseVectorStore:
    """Get or create Supabase vector store instance"""
    global supabase_vector_store
    if supabase_vector_store is None:
        supabase_vector_store = SupabaseVectorStore()
    return supabase_vector_store
