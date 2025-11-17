"""
Check if the environment is properly set up for the RAG system.
Run this script from the project root: python scripts/check_setup.py
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
os.chdir(project_root)

def check_setup():
    """Check if all requirements are met"""
    print("🔍 Checking RAG System Setup...\n")
    
    all_good = True
    
    # Check 1: .env file exists
    print("1. Checking for .env file...")
    if Path(".env").exists():
        print("   ✅ .env file found")
    else:
        print("   ❌ .env file NOT found")
        print("      → Create .env file with your OPENAI_API_KEY")
        print("      → See config/.env.template for example")
        all_good = False
    
    # Check 2: Load environment variables
    load_dotenv()
    
    # Check 3: OpenAI API key
    print("\n2. Checking OpenAI API key...")
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"   ✅ API key found (starts with: {api_key[:7]}...)")
    else:
        print("   ❌ OPENAI_API_KEY not set in .env file")
        all_good = False
    
    # Check 4: Data directory
    print("\n3. Checking data directory...")
    if Path("data").exists():
        print("   ✅ data/ directory exists")
        txt_files = list(Path("data").glob("*.txt")) + \
                    list(Path("data").glob("*.md")) + \
                    list(Path("data").glob("*.text"))
        print(f"   📄 Found {len(txt_files)} text file(s)")
    else:
        print("   ⚠️  data/ directory not found (will be created automatically)")
    
    # Check 5: Required packages
    print("\n4. Checking required packages...")
    required_packages = [
        "fastapi",
        "uvicorn", 
        "langchain",
        "langchain_community",
        "langchain_text_splitters",
        "openai",
        "langchain_openai",
        "faiss",
        "python_multipart",
        "dotenv"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            if package == "faiss":
                __import__("faiss")
            elif package == "python_multipart":
                __import__("multipart")
            elif package == "dotenv":
                __import__("dotenv")
            elif package == "langchain_community":
                __import__("langchain_community")
            elif package == "langchain_text_splitters":
                __import__("langchain_text_splitters")
            elif package == "langchain_openai":
                __import__("langchain_openai")
            else:
                __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - NOT installed")
            missing_packages.append(package)
            all_good = False
    
    if missing_packages:
        print(f"\n   💡 Install missing packages with:")
        print(f"      pip install -r requirements.txt")
    
    # Check 6: Vector store status
    print("\n5. Checking vector store...")
    if Path("vector_store").exists() and Path("vector_store_metadata.json").exists():
        print("   ✅ Vector store found")
        try:
            import json
            with open("vector_store_metadata.json", "r") as f:
                metadata = json.load(f)
                print(f"   📚 {len(metadata)} document(s) in vector store")
        except:
            print("   ⚠️  Could not read metadata")
    else:
        print("   ℹ️  No vector store yet (will be created on first upload)")
    
    # Summary
    print("\n" + "="*50)
    if all_good:
        print("✅ All checks passed! You're ready to go!")
        print("\nStart the server with:")
        print("   uvicorn main:app --reload")
        print("\nThen open: http://localhost:8000")
    else:
        print("❌ Some issues need to be fixed before running.")
        print("\nPlease fix the issues marked with ❌ above.")
    print("="*50)
    
    return all_good

if __name__ == "__main__":
    success = check_setup()
    sys.exit(0 if success else 1)
