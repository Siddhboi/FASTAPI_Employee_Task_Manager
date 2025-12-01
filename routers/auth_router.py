"""
Authentication Router
Handles user registration, login, and token management
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserCreate, UserLogin, UserResponse, Token
from models import User
from jwt_auth import (
    create_access_token,
    authenticate_user,
    get_current_active_user,
    get_current_admin_user,
    hash_password,
    get_user_by_username,
    get_user_by_email,
    create_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(
    prefix="/auth",
    tags=["🔐 Authentication"]
)

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user (CLIENT role by default)
    
    - **username**: Unique username (3-50 characters)
    - **email**: Valid email address (must be unique)
    - **password**: Password (min 6 characters)
    - **full_name**: Full name (optional)
    - **role**: User role (admin or client, default: client)
    
    **Note:** Only the first user can be created as admin. Subsequent admin users must be created by existing admins.
    """
    # Check if username already exists
    if get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    if get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if this is the first user (can be admin)
    user_count = db.query(User).count()
    
    # If this is not the first user and trying to register as admin, deny
    if user_count > 0 and user_data.role.value == "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot self-register as admin. Please contact an existing admin."
        )
    
    # Create user
    db_user = create_user(
        db=db,
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
        full_name=user_data.full_name,
        role=user_data.role
    )
    
    # Generate access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username, "role": db_user.role.value},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": db_user
    }

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Login with username and password
    
    - **username**: Your username
    - **password**: Your password
    
    Returns an access token that must be included in subsequent requests.
    
    **Usage:**
    1. Send POST request to this endpoint with username and password
    2. Copy the `access_token` from response
    3. Add header to protected endpoints: `Authorization: Bearer <access_token>`
    """
    # Authenticate user
    user = authenticate_user(db, user_data.username, user_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role.value},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """
    Get current logged-in user information
    
    **Requires:** Bearer token in Authorization header
    """
    return current_user

@router.get("/verify-token")
async def verify_token(current_user: User = Depends(get_current_active_user)):
    """
    Verify if the provided token is valid
    
    **Requires:** Bearer token in Authorization header
    """
    return {
        "valid": True,
        "username": current_user.username,
        "role": current_user.role.value,
        "message": "Token is valid"
    }

@router.post("/create-admin", response_model=UserResponse)
async def create_admin_user(
    user_data: UserCreate,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Create a new admin user (Admin only)
    
    **Requires:** Admin role
    
    - **username**: Unique username
    - **email**: Valid email address
    - **password**: Password
    - **full_name**: Full name (optional)
    """
    # Check if username already exists
    if get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    if get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Force admin role
    from models import UserRole
    db_user = create_user(
        db=db,
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
        full_name=user_data.full_name,
        role=UserRole.ADMIN
    )
    
    return db_user

@router.get("/users", response_model=list[UserResponse])
async def list_all_users(
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    List all users (Admin only)
    
    **Requires:** Admin role
    """
    users = db.query(User).all()
    return users