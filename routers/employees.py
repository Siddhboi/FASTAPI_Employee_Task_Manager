from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Employee, User
from schemas import EmployeeCreate, EmployeeUpdate, EmployeeResponse, EmployeeWithTasks
from auth_dependencies import require_authentication, require_admin

router = APIRouter(
    prefix="/employees",
    tags=["👥 Employees"]
)

@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(
    employee: EmployeeCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_authentication)
):
    """
    Create a new employee (Authentication required - JWT or API Key)
    
    **Authentication Options:**
    - **Option 1:** JWT Bearer Token - `Authorization: Bearer <token>`
    - **Option 2:** API Key - `X-API-Key: your-secret-api-key-12345`
    
    **Requires:** Valid authentication (JWT token OR API Key)
    
    - **name**: Employee's full name
    - **email**: Employee's email address (must be unique)
    - **role**: Employee's job role
    """
    # Check if email already exists
    existing_employee = db.query(Employee).filter(Employee.email == employee.email).first()
    if existing_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Employee with email '{employee.email}' already exists"
        )
    
    db_employee = Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.get("/", response_model=dict)
def get_all_employees(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum records to return"),
    role: Optional[str] = Query(None, description="Filter by role"),
    search: Optional[str] = Query(None, description="Search in name and email"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all employees with advanced filtering, search, and pagination
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100, max: 1000)
    - **role**: Filter by employee role
    - **search**: Search term for name and email
    
    Returns paginated results with metadata
    """
    query = db.query(Employee)
    
    # Apply role filter
    if role:
        query = query.filter(Employee.role.ilike(f"%{role}%"))
    
    # Apply search filter
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Employee.name.ilike(search_term)) | (Employee.email.ilike(search_term))
        )
    
    # Get total count before pagination
    total = query.count()
    
    # Apply pagination
    employees = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": [EmployeeResponse.model_validate(emp) for emp in employees]
    }

@router.get("/{employee_id}", response_model=EmployeeWithTasks)
def get_employee_by_id(employee_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific employee by ID with their assigned tasks
    
    - **employee_id**: The ID of the employee to retrieve
    """
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {employee_id} not found"
        )
    return employee

@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int, 
    employee_update: EmployeeUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_authentication)
):
    """
    Update an existing employee (Authentication required - JWT or API Key)
    
    **Authentication Options:**
    - **Option 1:** JWT Bearer Token - `Authorization: Bearer <token>`
    - **Option 2:** API Key - `X-API-Key: your-secret-api-key-12345`
    
    **Requires:** Valid authentication (JWT token OR API Key)
    
    - **employee_id**: The ID of the employee to update
    - **name**: New name (optional)
    - **email**: New email (optional, must be unique)
    - **role**: New role (optional)
    """
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {employee_id} not found"
        )
    
    # Check if email is being updated and if it's already taken
    if employee_update.email and employee_update.email != db_employee.email:
        existing = db.query(Employee).filter(Employee.email == employee_update.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Employee with email '{employee_update.email}' already exists"
            )
    
    # Update only provided fields
    update_data = employee_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_employee, key, value)
    
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: int, 
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """
    Delete an employee (Admin only - JWT or API Key)
    
    **Authentication Options:**
    - **Option 1:** JWT Bearer Token (Admin role) - `Authorization: Bearer <admin_token>`
    - **Option 2:** API Key (Admin access) - `X-API-Key: your-secret-api-key-12345`
    
    **Requires:** Admin role
    
    - **employee_id**: The ID of the employee to delete
    
    Note: This will also remove all tasks assigned to this employee
    """
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {employee_id} not found"
        )
    
    db.delete(db_employee)
    db.commit()
    return None