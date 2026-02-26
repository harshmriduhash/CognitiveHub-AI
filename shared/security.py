"""
Shared security utilities
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Optional
from shared.config import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token", auto_error=False)

def verify_token(token: str = Depends(oauth2_scheme)) -> dict:
    """Verify JWT token and return payload"""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(
            token, 
            config.JWT_SECRET_KEY, 
            algorithms=[config.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_tenant_id(payload: dict = Depends(verify_token)) -> str:
    """Extract tenant_id from token payload"""
    tenant_id = payload.get("tenant_id")
    if not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tenant ID missing from token"
        )
    return tenant_id
