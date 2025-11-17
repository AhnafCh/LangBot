"""
Main FastAPI application with support for both local and cloud backends
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Import the unified endpoints
from src.api import router

app = FastAPI(
    title="RAG System API",
    description="Document-based Q&A system with local (FAISS) and cloud (Supabase) support",
    version="2.0"
)

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(router)

# Serve static files (HTML client)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    import os
    
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
