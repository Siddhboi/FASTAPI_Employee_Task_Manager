from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from models import TaskStatus, UserRole

# ============== USER SCHEMAS ==============

class UserBase(BaseModel):
    """Base schema for User"""
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    email: EmailStr = Field(..., description="User email address")
    full_name: Optional[str] = Field(None, max_length=100, description="Full name")

class UserCreate(UserBase):
    """Schema for creating a user (registration)"""
    password: str = Field(..., min_length=6, max_length=100, description="Password")
    role: UserRole = Field(default=UserRole.CLIENT, description="User role")

class UserLogin(BaseModel):
    """Schema for user login"""
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")

class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    role: UserRole
    is_active: bool
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    """JWT Token response"""
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    """Token payload data"""
    username: Optional[str] = None
    role: Optional[str] = None

# ============== EMPLOYEE SCHEMAS ==============

class EmployeeBase(BaseModel):
    """Base schema for Employee"""
    name: str = Field(..., min_length=1, max_length=100, description="Employee name")
    email: EmailStr = Field(..., description="Employee email address")
    role: str = Field(..., min_length=1, max_length=100, description="Employee role")

class EmployeeCreate(EmployeeBase):
    """Schema for creating an employee"""
    pass

class EmployeeUpdate(BaseModel):
    """Schema for updating an employee (all fields optional)"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    role: Optional[str] = Field(None, min_length=1, max_length=100)

class EmployeeResponse(EmployeeBase):
    """Schema for employee response"""
    id: int
    
    class Config:
        from_attributes = True

class EmployeeWithTasks(EmployeeResponse):
    """Schema for employee with their tasks"""
    tasks: List['TaskResponse'] = []
    
    class Config:
        from_attributes = True

# ============== TASK SCHEMAS ==============

class TaskBase(BaseModel):
    """Base schema for Task"""
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: str = Field(..., min_length=1, description="Task description")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Task status")

class TaskCreate(TaskBase):
    """Schema for creating a task"""
    employee_id: Optional[int] = Field(None, description="Assigned employee ID")

class TaskUpdate(BaseModel):
    """Schema for updating a task (all fields optional)"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    status: Optional[TaskStatus] = None
    employee_id: Optional[int] = None

class TaskResponse(TaskBase):
    """Schema for task response"""
    id: int
    employee_id: Optional[int] = None
    
    class Config:
        from_attributes = True

class TaskWithEmployee(TaskResponse):
    """Schema for task with employee details"""
    employee: Optional[EmployeeResponse] = None
    
    class Config:
        from_attributes = True

# Forward reference resolution
EmployeeWithTasks.model_rebuild()