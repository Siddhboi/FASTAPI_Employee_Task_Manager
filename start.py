"""
Complete setup and start script
Handles database creation, default users, and sample data
"""
import sys
import subprocess

def run_command(description, func):
    """Run a function and handle errors"""
    print(f"\n{'='*60}")
    print(f"🔄 {description}...")
    print('='*60)
    try:
        func()
        print(f"✅ {description} - DONE!")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    return True

def create_database():
    """Create database tables"""
    from database import engine, Base
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")

def create_users():
    """Create default users"""
    from create_default_users import create_default_users
    create_default_users()

def create_sample_data():
    """Create sample employees and tasks"""
    response = input("\n📊 Do you want to create sample employees and tasks? (y/n): ")
    if response.lower() == 'y':
        from sample_data import create_sample_data
        create_sample_data()
    else:
        print("⏭️  Skipped sample data creation")

def show_instructions():
    """Show usage instructions"""
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE!")
    print("="*60)
    print("\n📋 Next Steps:")
    print("\n1️⃣  Start the server:")
    print("   uvicorn main:app --reload")
    print("\n2️⃣  Open your browser:")
    print("   http://localhost:8000/")
    print("\n3️⃣  Login with:")
    print("   Username: admin")
    print("   Password: admin123")
    print("\n4️⃣  Click 'Authorize' button 🔓")
    print("   Enter: Bearer <your_access_token>")
    print("\n📚 For detailed instructions, see:")
    print("   AUTHENTICATION_GUIDE.md")
    print("\n" + "="*60)

def main():
    """Main setup function"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║  Employee Task Manager API - Complete Setup             ║
    ║  JWT Authentication System                               ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Step 1: Create database
    if not run_command("Creating database tables", create_database):
        return
    
    # Step 2: Create default users
    if not run_command("Creating default users", create_users):
        return
    
    # Step 3: Create sample data (optional)
    try:
        create_sample_data()
    except KeyboardInterrupt:
        print("\n⏭️  Skipped sample data creation")
    
    # Step 4: Show instructions
    show_instructions()
    
    # Ask if user wants to start server
    print("\n" + "="*60)
    response = input("🚀 Do you want to start the server now? (y/n): ")
    if response.lower() == 'y':
        print("\n🔄 Starting server...")
        print("Press CTRL+C to stop the server\n")
        try:
            subprocess.run(["uvicorn", "main:app", "--reload"])
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped. Goodbye!")
    else:
        print("\n👋 Setup complete! Run 'uvicorn main:app --reload' when ready.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        sys.exit(1)