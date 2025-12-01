"""
Setup script to initialize Alembic and create initial migration
"""
import os
import sys
import subprocess

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n{'='*60}")
    print(f"🔄 {description}...")
    print('='*60)
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout)
        print(f"✅ {description} - DONE!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False

def check_alembic_structure():
    """Check if Alembic directory structure exists"""
    print("\n🔍 Checking Alembic directory structure...")
    
    required_dirs = ['alembic', 'alembic/versions']
    required_files = ['alembic.ini', 'alembic/env.py']
    
    missing = []
    
    for directory in required_dirs:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Created directory: {directory}")
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing.append(file_path)
    
    if missing:
        print(f"⚠️  Missing files: {', '.join(missing)}")
        print("   Please ensure these files exist before proceeding.")
        return False
    
    print("✅ Alembic structure is correct!")
    return True

def main():
    """Main setup function"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║  Alembic Migration Setup                                 ║
    ║  Database Migration Tool                                 ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Step 1: Check structure
    if not check_alembic_structure():
        print("\n❌ Setup failed: Missing required files")
        return
    
    # Step 2: Check current migration status
    print("\n📊 Checking current migration status...")
    run_command("alembic current", "Check current version")
    
    # Step 3: Check if there are existing migrations
    versions_dir = "alembic/versions"
    existing_migrations = [f for f in os.listdir(versions_dir) if f.endswith('.py') and f != '__init__.py']
    
    if existing_migrations:
        print(f"\n⚠️  Found {len(existing_migrations)} existing migration(s)")
        response = input("Do you want to create a new migration? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return
    
    # Step 4: Create new migration
    migration_message = input("\nEnter migration message (default: 'Auto migration'): ").strip()
    if not migration_message:
        migration_message = "Auto migration"
    
    if not run_command(
        f'alembic revision --autogenerate -m "{migration_message}"',
        "Create new migration"
    ):
        print("\n❌ Failed to create migration")
        return
    
    # Step 5: Ask to apply migration
    print("\n" + "="*60)
    response = input("Do you want to apply this migration now? (y/n): ")
    
    if response.lower() == 'y':
        if run_command("alembic upgrade head", "Apply migration"):
            print("\n✅ Migration applied successfully!")
        else:
            print("\n❌ Failed to apply migration")
    else:
        print("\n⏭️  Skipped migration application")
        print("   Run 'alembic upgrade head' when ready to apply")
    
    # Step 6: Show final status
    print("\n" + "="*60)
    print("📋 Final Migration Status:")
    print("="*60)
    run_command("alembic current", "Current version")
    run_command("alembic history", "Migration history")
    
    print("\n" + "="*60)
    print("✅ Alembic setup complete!")
    print("="*60)
    print("\n📚 Useful Alembic commands:")
    print("  alembic current              - Show current version")
    print("  alembic history              - Show all migrations")
    print("  alembic upgrade head         - Apply all pending migrations")
    print("  alembic downgrade -1         - Rollback one version")
    print("  alembic revision --autogenerate -m 'message' - Create new migration")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        sys.exit(1)