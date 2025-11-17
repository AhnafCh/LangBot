"""
RAG System with Supabase backend
Supports both FAISS (local) and Supabase (cloud) vector stores
"""
from dotenv import load_dotenv
import os

from langchain_openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize the LLM (using OpenAI)
llm = OpenAI()

# Determine which vector store to use
USE_SUPABASE = os.getenv("USE_SUPABASE", "false").lower() == "true"


async def get_rag_response(query: str):
    """
    Get RAG response using either Supabase or FAISS backend
    """
    try:
        if USE_SUPABASE:
            # Use Supabase pgvector for production
            from src.backends import get_supabase_store
            
            store = get_supabase_store()
            retrieved_docs = await store.similarity_search(query, k=2)
            
            if not retrieved_docs:
                return "I don't have enough information to answer that question. Please upload relevant documents first."
        else:
            # Use FAISS for local development
            from src.backends import vector_store_manager
            
            retriever = vector_store_manager.get_retriever(k=2)
            retrieved_docs = retriever.invoke(query)
        
        # Prepare the input for the LLM
        context = "\n".join([doc.page_content for doc in retrieved_docs])
        
        # Create prompt with context
        prompt = [f"Use the following information to answer the question:\n\n{context}\n\nQuestion: {query}"]
        
        # Generate the final response using the language model
        generated_response = llm.generate(prompt)
        
        # Extract the text from the response
        return generated_response.generations[0][0].text
        
    except ValueError as e:
        return f"Error: {str(e)}. Please upload at least one document first."
    except Exception as e:
        return f"An error occurred: {str(e)}"
