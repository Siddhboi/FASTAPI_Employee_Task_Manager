from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum, Boolean
from sqlalchemy.orm import relationship
from database import Base
import enum

class TaskStatus(str, enum.Enum):
    """Enum for task status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class UserRole(str, enum.Enum):
    """Enum for user roles"""
    ADMIN = "admin"
    CLIENT = "client"

class User(Base):
    """User model for authentication"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.CLIENT, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

class Employee(Base):
    """Employee SQLAlchemy model"""
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    role = Column(String, nullable=False)
    phone = Column(String, nullable=True)  # ADD THIS
    
    # Relationship with tasks
    tasks = relationship("Task", back_populates="employee", cascade="all, delete-orphan")

class Task(Base):
    """Task SQLAlchemy model"""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    
    # Relationship with employee
    employee = relationship("Employee", back_populates="tasks")