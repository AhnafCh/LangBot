# Quick Start Guide

## Before Running the Server

You need to set up your OpenAI API key first.

### Step 1: Get Your OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (it starts with "sk-...")

### Step 2: Create .env File
Create a file named `.env` in the project root directory (D:\LangBot\) with this content:

```
OPENAI_API_KEY=sk-your-actual-key-here
```

Replace `sk-your-actual-key-here` with your actual OpenAI API key.

### Step 3: Initialize Vector Store (Optional)
If you want to add the existing document (my_document.txt) to the vector store:

```bash
python init_vector_store.py
```

### Step 4: Start the Server
```bash
uvicorn main:app --reload
```

### Step 5: Open the Web Interface
Open your browser and go to:
```
http://localhost:8000
```

## That's It!

You can now:
- Upload new documents
- Ask questions about your documents
- View all uploaded documents

Enjoy your RAG system! 🚀
