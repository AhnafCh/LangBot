"""
Helper script to switch between Local (FAISS) and Cloud (Supabase) backends
Run this script from the project root: python scripts/switch_backend.py [local|supabase|status]
"""
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
os.chdir(project_root)

def update_env_variable(key: str, value: str):
    """Update or add a variable in .env file"""
    env_path = Path(".env")
    
    if not env_path.exists():
        print("❌ .env file not found!")
        print("💡 Create one from config/.env.template first")
        sys.exit(1)
    
    # Read current .env content
    with open(env_path, 'r') as f:
        lines = f.readlines()
    
    # Update or add the variable
    found = False
    for i, line in enumerate(lines):
        if line.strip().startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            found = True
            break
    
    if not found:
        lines.append(f"\n{key}={value}\n")
    
    # Write back
    with open(env_path, 'w') as f:
        f.writelines(lines)


def switch_to_local():
    """Switch to local FAISS backend"""
    print("🔄 Switching to Local FAISS backend...")
    update_env_variable("USE_SUPABASE", "false")
    print("✅ Switched to Local FAISS!")
    print("📝 Your documents will be stored locally")
    print("🚀 Restart the server for changes to take effect")


def switch_to_supabase():
    """Switch to Supabase cloud backend"""
    print("🔄 Switching to Supabase backend...")
    
    # Check if Supabase credentials are set
    from dotenv import load_dotenv
    load_dotenv()
    
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key or \
       supabase_url == "your_supabase_project_url" or \
       supabase_key == "your_supabase_anon_or_service_key":
        print("❌ Supabase credentials not configured!")
        print("\n📋 Please add to your .env file:")
        print("   SUPABASE_URL=your_project_url")
        print("   SUPABASE_KEY=your_service_role_key")
        print("\n💡 Get these from: https://supabase.com/dashboard")
        print("   Project Settings → API")
        sys.exit(1)
    
    update_env_variable("USE_SUPABASE", "true")
    print("✅ Switched to Supabase!")
    print("☁️  Your documents will be stored in the cloud")
    print("🚀 Restart the server for changes to take effect")


def show_status():
    """Show current backend status"""
    from dotenv import load_dotenv
    load_dotenv()
    
    use_supabase = os.getenv("USE_SUPABASE", "false").lower() == "true"
    
    print("\n📊 Current Backend Status")
    print("=" * 50)
    
    if use_supabase:
        print("✅ Backend: Supabase (Cloud)")
        print(f"   URL: {os.getenv('SUPABASE_URL', 'Not set')}")
        print(f"   Key: {'✅ Configured' if os.getenv('SUPABASE_KEY') else '❌ Not set'}")
    else:
        print("✅ Backend: Local FAISS")
        print("   Storage: ./vector_store/")
        print("   Metadata: ./vector_store_metadata.json")
    
    print(f"\nOpenAI: {'✅ Configured' if os.getenv('OPENAI_API_KEY') else '❌ Not set'}")
    print("=" * 50)


def main():
    if len(sys.argv) < 2:
        print("🔧 Backend Switcher")
        print("\nUsage:")
        print("  python switch_backend.py local     - Switch to local FAISS")
        print("  python switch_backend.py supabase  - Switch to Supabase")
        print("  python switch_backend.py status    - Show current backend")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "local":
        switch_to_local()
    elif command == "supabase" or command == "cloud":
        switch_to_supabase()
    elif command == "status":
        show_status()
    else:
        print(f"❌ Unknown command: {command}")
        print("Use: local, supabase, or status")
        sys.exit(1)


if __name__ == "__main__":
    main()
