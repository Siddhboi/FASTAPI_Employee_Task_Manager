"""
Script to populate the database with sample employees and tasks
Run this script after starting the API server
"""
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Employee, Task, TaskStatus

def create_sample_data():
    """Create sample employees and tasks"""
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Clear existing data (optional - remove if you want to keep existing data)
        print("Clearing existing data...")
        db.query(Task).delete()
        db.query(Employee).delete()
        db.commit()
        
        # Sample Employees
        print("Creating sample employees...")
        employees_data = [
            {"name": "John Doe", "email": "john.doe@company.com", "role": "Software Engineer"},
            {"name": "Jane Smith", "email": "jane.smith@company.com", "role": "Project Manager"},
            {"name": "Mike Johnson", "email": "mike.johnson@company.com", "role": "UI/UX Designer"},
            {"name": "Emily Brown", "email": "emily.brown@company.com", "role": "QA Engineer"},
            {"name": "David Wilson", "email": "david.wilson@company.com", "role": "DevOps Engineer"},
            {"name": "Sarah Davis", "email": "sarah.davis@company.com", "role": "Business Analyst"},
            {"name": "Robert Taylor", "email": "robert.taylor@company.com", "role": "Full Stack Developer"},
            {"name": "Lisa Anderson", "email": "lisa.anderson@company.com", "role": "Data Scientist"},
            {"name": "James Martinez", "email": "james.martinez@company.com", "role": "Backend Developer"},
            {"name": "Maria Garcia", "email": "maria.garcia@company.com", "role": "Frontend Developer"},
        ]
        
        employees = []
        for emp_data in employees_data:
            employee = Employee(**emp_data)
            db.add(employee)
            employees.append(employee)
        
        db.commit()
        print(f"✅ Created {len(employees)} employees")
        
        # Refresh to get IDs
        for emp in employees:
            db.refresh(emp)
        
        # Sample Tasks
        print("Creating sample tasks...")
        tasks_data = [
            {
                "title": "Implement User Authentication",
                "description": "Add JWT-based authentication to the API",
                "status": TaskStatus.IN_PROGRESS,
                "employee_id": employees[0].id
            },
            {
                "title": "Design Dashboard UI",
                "description": "Create wireframes and mockups for the admin dashboard",
                "status": TaskStatus.COMPLETED,
                "employee_id": employees[2].id
            },
            {
                "title": "Write API Documentation",
                "description": "Document all API endpoints with examples",
                "status": TaskStatus.PENDING,
                "employee_id": employees[1].id
            },
            {
                "title": "Set Up CI/CD Pipeline",
                "description": "Configure GitHub Actions for automated testing and deployment",
                "status": TaskStatus.IN_PROGRESS,
                "employee_id": employees[4].id
            },
            {
                "title": "Database Migration",
                "description": "Migrate from SQLite to PostgreSQL",
                "status": TaskStatus.PENDING,
                "employee_id": employees[4].id
            },
            {
                "title": "Conduct User Testing",
                "description": "Perform UAT for the new features",
                "status": TaskStatus.PENDING,
                "employee_id": employees[3].id
            },
            {
                "title": "Optimize Database Queries",
                "description": "Improve performance of slow queries",
                "status": TaskStatus.COMPLETED,
                "employee_id": employees[8].id
            },
            {
                "title": "Implement Real-time Notifications",
                "description": "Add WebSocket support for live updates",
                "status": TaskStatus.PENDING,
                "employee_id": employees[6].id
            },
            {
                "title": "Create Data Analytics Dashboard",
                "description": "Build visualization for business metrics",
                "status": TaskStatus.IN_PROGRESS,
                "employee_id": employees[7].id
            },
            {
                "title": "Mobile App Prototype",
                "description": "Develop a React Native prototype for mobile",
                "status": TaskStatus.PENDING,
                "employee_id": employees[9].id
            },
            {
                "title": "Security Audit",
                "description": "Perform comprehensive security testing",
                "status": TaskStatus.PENDING,
                "employee_id": None  # Unassigned task
            },
            {
                "title": "Refactor Legacy Code",
                "description": "Clean up and modernize old codebase",
                "status": TaskStatus.PENDING,
                "employee_id": None  # Unassigned task
            },
        ]
        
        tasks = []
        for task_data in tasks_data:
            task = Task(**task_data)
            db.add(task)
            tasks.append(task)
        
        db.commit()
        print(f"✅ Created {len(tasks)} tasks")
        
        print("\n" + "="*50)
        print("🎉 Sample data created successfully!")
        print("="*50)
        print("\nSummary:")
        print(f"  • Employees: {len(employees)}")
        print(f"  • Tasks: {len(tasks)}")
        print(f"  • Assigned Tasks: {len([t for t in tasks if t.employee_id])}")
        print(f"  • Unassigned Tasks: {len([t for t in tasks if not t.employee_id])}")
        print("\nTask Status Distribution:")
        print(f"  • Pending: {len([t for t in tasks if t.status == TaskStatus.PENDING])}")
        print(f"  • In Progress: {len([t for t in tasks if t.status == TaskStatus.IN_PROGRESS])}")
        print(f"  • Completed: {len([t for t in tasks if t.status == TaskStatus.COMPLETED])}")
        print("\n✨ You can now test the API at http://localhost:8000")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()