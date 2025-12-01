from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from typing import Optional
from config import settings

# API Key configuration
API_KEY_NAME = "X-API-Key"
API_KEY = settings.API_KEY

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key: Optional[str] = Security(api_key_header)) -> Optional[str]:
    """
    Validate API Key from request header
    
    Args:
        api_key: API key from X-API-Key header
        
    Returns:
        The validated API key if valid, raises exception if provided but invalid
        
    Raises:
        HTTPException: If API key is provided but invalid
    """
    if api_key is None:
        return None
    
    if api_key == API_KEY:
        return api_key
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key",
        headers={"WWW-Authenticate": "ApiKey"},
    )