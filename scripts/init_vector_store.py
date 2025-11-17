"""
Initialize the vector store with existing documents in the data directory.
Run this script from the project root: python scripts/init_vector_store.py
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables first
load_dotenv()

def initialize_vector_store():
    """Initialize vector store with all documents in data directory"""
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY environment variable is not set!")
        print("Please create a .env file with your OpenAI API key.")
        print("See config/.env.template for an example.")
        sys.exit(1)
    
    # Import here after checking environment
    from src.backends.faiss_manager import vector_store_manager
    
    data_dir = "data"
    
    if not os.path.exists(data_dir):
        print(f"Data directory '{data_dir}' does not exist.")
        return
    
    # Get all text files in data directory
    text_files = list(Path(data_dir).glob("*.txt")) + \
                 list(Path(data_dir).glob("*.md")) + \
                 list(Path(data_dir).glob("*.text"))
    
    if not text_files:
        print("No text files found in data directory.")
        return
    
    print(f"Found {len(text_files)} document(s) to process...")
    
    for file_path in text_files:
        print(f"\nProcessing: {file_path.name}")
        result = vector_store_manager.add_document(
            str(file_path), 
            file_path.name
        )
        
        print(f"  Status: {result['status']}")
        print(f"  Message: {result['message']}")
        
        if result['status'] == 'success':
            print(f"  Document ID: {result['document_id']}")
            print(f"  Chunks created: {result['chunk_count']}")
    
    print("\n" + "="*50)
    print("Vector store initialization complete!")
    print(f"Total documents in vector store: {len(vector_store_manager.get_all_documents())}")

if __name__ == "__main__":
    initialize_vector_store()
