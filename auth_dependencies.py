"""
Combined Authentication Dependencies
Supports both JWT and API Key authentication
"""
from typing import Optional, Union
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database import get_db
from models import User, UserRole
from auth import get_api_key
from jwt_auth import get_current_user as jwt_get_current_user

# HTTPBearer for JWT
security = HTTPBearer(auto_error=False)

async def get_current_user_dual(
    bearer_credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    api_key: Optional[str] = Depends(get_api_key),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Get current user using EITHER JWT token OR API Key
    
    Priority:
    1. JWT Bearer Token (if provided)
    2. API Key (if provided)
    3. None (if neither provided)
    
    Args:
        bearer_credentials: JWT token from Authorization: Bearer header
        api_key: API key from X-API-Key header
        db: Database session
        
    Returns:
        User object if authenticated, None otherwise
    """
    # Try JWT first
    if bearer_credentials:
        try:
            user = await jwt_get_current_user(bearer_credentials, db)
            return user
        except HTTPException:
            pass  # Try API key next
    
    # Try API key
    if api_key:
        # API key is valid (validated by get_api_key)
        # For API key, we return a virtual admin user
        # You can customize this behavior
        virtual_admin = User(
            id=0,
            username="api_key_user",
            email="api@system.com",
            full_name="API Key User",
            hashed_password="",
            role=UserRole.ADMIN,  # API key gets admin privileges
            is_active=True
        )
        return virtual_admin
    
    return None

async def require_authentication(
    user: Optional[User] = Depends(get_current_user_dual)
) -> User:
    """
    Require authentication via JWT OR API Key
    Raises 401 if neither is provided or valid
    """
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Provide either JWT token (Authorization: Bearer) or API Key (X-API-Key)",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def require_admin(
    user: User = Depends(require_authentication)
) -> User:
    """
    Require admin role (works with both JWT and API Key)
    """
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return user