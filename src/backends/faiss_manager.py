import os
import json
import hashlib
from pathlib import Path
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Load environment variables
load_dotenv()


class VectorStoreManager:
    """Manages persistent vector store and document tracking"""
    
    def __init__(self, vector_store_path: str = "vector_store", metadata_path: str = "vector_store_metadata.json"):
        self.vector_store_path = vector_store_path
        self.metadata_path = metadata_path
        self.embeddings = OpenAIEmbeddings()
        self.vector_store: Optional[FAISS] = None
        self.metadata: Dict[str, Dict] = {}
        
        # Create vector store directory if it doesn't exist
        Path(vector_store_path).mkdir(parents=True, exist_ok=True)
        
        # Load existing metadata
        self._load_metadata()
        
        # Load existing vector store if available
        self._load_vector_store()
    
    def _load_metadata(self):
        """Load document metadata from JSON file"""
        if os.path.exists(self.metadata_path):
            with open(self.metadata_path, 'r') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {}
    
    def _save_metadata(self):
        """Save document metadata to JSON file"""
        with open(self.metadata_path, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def _load_vector_store(self):
        """Load existing FAISS vector store"""
        if os.path.exists(os.path.join(self.vector_store_path, "index.faiss")):
            try:
                self.vector_store = FAISS.load_local(
                    self.vector_store_path, 
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                print(f"Loaded existing vector store with {len(self.metadata)} documents")
            except Exception as e:
                print(f"Error loading vector store: {e}")
                self.vector_store = None
    
    def _save_vector_store(self):
        """Save FAISS vector store to disk"""
        if self.vector_store:
            self.vector_store.save_local(self.vector_store_path)
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA256 hash of a file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def document_exists(self, file_path: str) -> tuple[bool, Optional[str]]:
        """
        Check if document already exists in the vector store
        Returns: (exists: bool, document_id: Optional[str])
        """
        file_hash = self._calculate_file_hash(file_path)
        
        for doc_id, doc_info in self.metadata.items():
            if doc_info.get('file_hash') == file_hash:
                return True, doc_id
        
        return False, None
    
    def add_document(self, file_path: str, original_filename: str) -> Dict[str, Any]:
        """
        Add a new document to the vector store
        Returns: Dictionary with status and document info
        """
        # Check if document already exists
        exists, existing_id = self.document_exists(file_path)
        if exists:
            return {
                "status": "duplicate",
                "message": f"Document already exists with ID: {existing_id}",
                "document_id": existing_id
            }
        
        try:
            # Load the document
            loader = TextLoader(file_path, encoding='utf-8')
            documents = loader.load()
            
            # Split the document into chunks
            splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
            document_chunks = splitter.split_documents(documents)
            
            # Calculate file hash for duplicate detection
            file_hash = self._calculate_file_hash(file_path)
            
            # Generate unique document ID
            doc_id = f"doc_{file_hash[:16]}"
            
            # Add metadata to each chunk
            for chunk in document_chunks:
                chunk.metadata['document_id'] = doc_id
                chunk.metadata['source_file'] = original_filename
            
            # Add to vector store or create new one
            if self.vector_store is None:
                self.vector_store = FAISS.from_documents(document_chunks, self.embeddings)
            else:
                # Add new documents to existing vector store
                new_vector_store = FAISS.from_documents(document_chunks, self.embeddings)
                self.vector_store.merge_from(new_vector_store)
            
            # Save vector store
            self._save_vector_store()
            
            # Update metadata
            self.metadata[doc_id] = {
                'document_id': doc_id,
                'original_filename': original_filename,
                'file_hash': file_hash,
                'file_path': file_path,
                'chunk_count': len(document_chunks),
                'added_at': str(Path(file_path).stat().st_mtime)
            }
            self._save_metadata()
            
            return {
                "status": "success",
                "message": f"Document added successfully with {len(document_chunks)} chunks",
                "document_id": doc_id,
                "chunk_count": len(document_chunks)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error processing document: {str(e)}",
                "document_id": None
            }
    
    def get_retriever(self, k: int = 2):
        """Get a retriever from the vector store"""
        if self.vector_store is None:
            raise ValueError("No vector store available. Please add documents first.")
        
        return self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k}
        )
    
    def get_all_documents(self) -> List[Dict]:
        """Get list of all documents in the vector store"""
        return list(self.metadata.values())
    
    def remove_document(self, doc_id: str) -> Dict[str, Any]:
        """Remove a document from metadata (Note: FAISS doesn't support deletion easily)"""
        if doc_id in self.metadata:
            del self.metadata[doc_id]
            self._save_metadata()
            return {
                "status": "success",
                "message": f"Document {doc_id} removed from metadata. Rebuild vector store to fully remove."
            }
        return {
            "status": "error",
            "message": f"Document {doc_id} not found"
        }


# Global instance
vector_store_manager = VectorStoreManager()
