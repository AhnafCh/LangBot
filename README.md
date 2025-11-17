# LangBot - RAG System with Document Upload

A FastAPI-based Retrieval-Augmented Generation (RAG) system with document upload functionality and persistent vector storage.

## Features

- 📄 **Document Upload**: Upload text documents (.txt, .md, .text) through the web interface
- 🔍 **Automatic Vectorization**: Documents are automatically processed and vectorized upon upload
- 💾 **Persistent Storage**: Vector store is saved to disk and reused across sessions
- 🔒 **Duplicate Prevention**: Each document gets a unique ID based on content hash to prevent duplicates
- 🤖 **Question Answering**: Query the RAG system to get answers based on uploaded documents
- 📚 **Document Management**: View all uploaded documents and their metadata

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your OpenAI API key:
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_api_key_here
```

3. Initialize the vector store with existing documents (optional):
```bash
python init_vector_store.py
```

## Usage

1. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

3. Upload documents:
   - Click "Choose File" to select a text document
   - Click "Upload & Vectorize" to process and add it to the vector store
   - The system will notify you if the document is a duplicate

4. Ask questions:
   - Type your question in the query box
   - Click "Submit Query" to get an answer based on the uploaded documents

## API Endpoints

### POST /upload/
Upload a new document and automatically vectorize it.
- **Input**: Multipart form data with file
- **Returns**: Document ID, status, and chunk count

### GET /query/
Query the RAG system with a question.
- **Parameters**: `query` (string)
- **Returns**: Query response based on relevant documents

### GET /documents/
Get a list of all uploaded documents.
- **Returns**: Count and list of documents with metadata

### DELETE /documents/{doc_id}
Remove a document from metadata.
- **Parameters**: `doc_id` (string)
- **Returns**: Success/error status

## File Structure

```
LangBot/
├── main.py                      # FastAPI application entry point
├── endpoints.py                 # API endpoints
├── rag.py                       # RAG system logic
├── vector_store_manager.py      # Vector store management and persistence
├── init_vector_store.py         # Script to initialize vector store
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (create this)
├── data/                        # Document storage directory
│   └── my_document.txt         # Example document
├── static/
│   └── index.html              # Web interface
├── vector_store/               # FAISS vector store (auto-generated)
└── vector_store_metadata.json  # Document metadata (auto-generated)
```

## How It Works

1. **Document Upload**: When you upload a document:
   - File is saved to the `data/` directory
   - Content hash (SHA256) is calculated for duplicate detection
   - Document is split into chunks using RecursiveCharacterTextSplitter
   - Chunks are embedded using OpenAI embeddings
   - Embeddings are stored in a FAISS vector store
   - Metadata is saved to `vector_store_metadata.json`

2. **Duplicate Prevention**: 
   - Each document is assigned a unique ID based on its content hash
   - Before adding a document, the system checks if a document with the same hash exists
   - If found, the upload is rejected with a notification

3. **Persistent Storage**:
   - Vector store is saved to disk in the `vector_store/` directory
   - On startup, the system loads the existing vector store
   - All documents are reused across sessions

4. **Query Processing**:
   - User query is embedded using the same embedding model
   - Similar document chunks are retrieved from the vector store
   - Retrieved context is combined with the query
   - OpenAI LLM generates a response based on the context

## Technologies Used

- **FastAPI**: Web framework
- **LangChain**: RAG framework
- **OpenAI**: Embeddings and LLM
- **FAISS**: Vector similarity search
- **Python-multipart**: File upload handling

## Notes

- Only text-based files (.txt, .md, .text) are supported
- The system requires an active OpenAI API key
- Vector store is automatically saved after each document upload
- Document chunks are set to 200 characters with 20 character overlap (configurable in `vector_store_manager.py`)

## Troubleshooting

**Error: "No vector store available"**
- Upload at least one document first, or run `python init_vector_store.py` to process existing documents

**Error: "OpenAI API key not found"**
- Make sure you have created a `.env` file with your OpenAI API key

**Upload fails with "Only text files are supported"**
- Ensure your file has a .txt, .md, or .text extension
