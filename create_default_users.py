"""
Script to create default admin and client users
Run this after creating the database
"""
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import User, UserRole
from jwt_auth import hash_password

def create_default_users():
    """Create default admin and client users"""
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Check if users already exist
        existing_users = db.query(User).count()
        if existing_users > 0:
            print("⚠️  Users already exist in database. Skipping creation.")
            print(f"   Total users: {existing_users}")
            return
        
        print("Creating default users...")
        print("=" * 50)
        
        # Create Admin User
        admin_user = User(
            username="admin",
            email="admin@example.com",
            full_name="Admin User",
            hashed_password=hash_password("admin123"),
            role=UserRole.ADMIN,
            is_active=True
        )
        db.add(admin_user)
        
        # Create Client User
        client_user = User(
            username="client",
            email="client@example.com",
            full_name="Client User",
            hashed_password=hash_password("client123"),
            role=UserRole.CLIENT,
            is_active=True
        )
        db.add(client_user)
        
        # Create Demo Admin
        demo_admin = User(
            username="demoadmin",
            email="demoadmin@example.com",
            full_name="Demo Admin",
            hashed_password=hash_password("demo123"),
            role=UserRole.ADMIN,
            is_active=True
        )
        db.add(demo_admin)
        
        db.commit()
        
        print("✅ Default users created successfully!")
        print("=" * 50)
        print("\n📋 Login Credentials:\n")
        print("👨‍💼 ADMIN USERS:")
        print("   Username: admin    | Password: admin123")
        print("   Username: demoadmin | Password: demo123")
        print("\n👤 CLIENT USER:")
        print("   Username: client   | Password: client123")
        print("\n" + "=" * 50)
        print("\n🔐 Authentication Instructions:")
        print("1. Go to http://localhost:8000/")
        print("2. Click on 'POST /auth/login'")
        print("3. Try it out with above credentials")
        print("4. Copy the 'access_token' from response")
        print("5. Click 'Authorize' button at top")
        print("6. Paste token in format: Bearer <your_token>")
        print("7. Now you can access protected endpoints!")
        print("\n" + "=" * 50)
        
    except Exception as e:
        print(f"❌ Error creating users: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_default_users()