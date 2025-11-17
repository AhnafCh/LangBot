from dotenv import load_dotenv
import os

from langchain_openai import OpenAI
from vector_store_manager import vector_store_manager

# Load environment variables
load_dotenv()

# Initialize the LLM (using OpenAI)
llm = OpenAI()

# Function to get the response from the RAG system
async def get_rag_response(query: str):
    try:
        # Get retriever from the persistent vector store
        retriever = vector_store_manager.get_retriever(k=2)
        
        # Retrieve the relevant documents using 'invoke' method
        retrieved_docs = retriever.invoke(query)
        
        # Prepare the input for the LLM: Combine the query and the retrieved documents into a single string
        context = "\n".join([doc.page_content for doc in retrieved_docs])
        
        # LLM expects a list of strings (prompts), so we create one by combining the query with the retrieved context
        prompt = [f"Use the following information to answer the question:\n\n{context}\n\nQuestion: {query}"]
        
        # Generate the final response using the language model (LLM)
        generated_response = llm.generate(prompt)
        
        # Extract the text from the response
        return generated_response.generations[0][0].text
    except ValueError as e:
        return f"Error: {str(e)}. Please upload at least one document first."