from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Task, Employee, TaskStatus, User
from schemas import TaskCreate, TaskUpdate, TaskResponse, TaskWithEmployee
from auth_dependencies import require_authentication, require_admin

router = APIRouter(
    prefix="/tasks",
    tags=["📋 Tasks"]
)

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_authentication)
):
    """
    Create a new task (Authentication required - JWT or API Key)
    
    **Authentication Options:**
    - **Option 1:** JWT Bearer Token - `Authorization: Bearer <token>`
    - **Option 2:** API Key - `X-API-Key: your-secret-api-key-12345`
    
    **Requires:** Valid authentication (JWT token OR API Key)
    
    - **title**: Task title
    - **description**: Task description
    - **status**: Task status (pending, in_progress, completed)
    - **employee_id**: ID of assigned employee (optional)
    """
    # Validate employee exists if provided
    if task.employee_id:
        employee = db.query(Employee).filter(Employee.id == task.employee_id).first()
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID {task.employee_id} not found"
            )
    
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/", response_model=dict)
def get_all_tasks(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum records to return"),
    status_filter: Optional[TaskStatus] = Query(None, alias="status", description="Filter by task status"),
    employee_id: Optional[int] = Query(None, description="Filter by employee ID"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all tasks with advanced filtering, search, and pagination
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100, max: 1000)
    - **status**: Filter by task status (pending, in_progress, completed)
    - **employee_id**: Filter by assigned employee
    - **search**: Search term for title and description
    
    Returns paginated results with metadata
    """
    query = db.query(Task)
    
    # Apply status filter
    if status_filter:
        query = query.filter(Task.status == status_filter)
    
    # Apply employee filter
    if employee_id is not None:
        query = query.filter(Task.employee_id == employee_id)
    
    # Apply search filter
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Task.title.ilike(search_term)) | (Task.description.ilike(search_term))
        )
    
    # Get total count before pagination
    total = query.count()
    
    # Apply pagination
    tasks = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": [TaskWithEmployee.model_validate(task) for task in tasks]
    }

@router.get("/{task_id}", response_model=TaskWithEmployee)
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific task by ID with employee details
    
    - **task_id**: The ID of the task to retrieve
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int, 
    task_update: TaskUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_authentication)
):
    """
    Update an existing task (Authentication required - JWT or API Key)
    
    **Authentication Options:**
    - **Option 1:** JWT Bearer Token - `Authorization: Bearer <token>`
    - **Option 2:** API Key - `X-API-Key: your-secret-api-key-12345`
    
    **Requires:** Valid authentication (JWT token OR API Key)
    
    - **task_id**: The ID of the task to update
    - **title**: New title (optional)
    - **description**: New description (optional)
    - **status**: New status (optional)
    - **employee_id**: New assigned employee ID (optional)
    """
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    
    # Validate employee exists if being updated
    if task_update.employee_id is not None:
        if task_update.employee_id > 0:
            employee = db.query(Employee).filter(Employee.id == task_update.employee_id).first()
            if not employee:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Employee with ID {task_update.employee_id} not found"
                )
    
    # Update only provided fields
    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int, 
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """
    Delete a task (Admin only - JWT or API Key)
    
    **Authentication Options:**
    - **Option 1:** JWT Bearer Token (Admin role) - `Authorization: Bearer <admin_token>`
    - **Option 2:** API Key (Admin access) - `X-API-Key: your-secret-api-key-12345`
    
    **Requires:** Admin role
    
    - **task_id**: The ID of the task to delete
    """
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    
    db.delete(db_task)
    db.commit()
    return None

@router.post("/{task_id}/assign/{employee_id}", response_model=TaskResponse)
def assign_task_to_employee(
    task_id: int, 
    employee_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_authentication)
):
    """
    Assign a task to an employee (Authentication required - JWT or API Key)
    
    **Authentication Options:**
    - **Option 1:** JWT Bearer Token - `Authorization: Bearer <token>`
    - **Option 2:** API Key - `X-API-Key: your-secret-api-key-12345`
    
    **Requires:** Valid authentication (JWT token OR API Key)
    
    - **task_id**: The ID of the task to assign
    - **employee_id**: The ID of the employee to assign the task to
    """
    # Check if task exists
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    
    # Check if employee exists
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {employee_id} not found"
        )
    
    # Assign task
    db_task.employee_id = employee_id
    db.commit()
    db.refresh(db_task)
    return db_task