"""
Auth & Tenant Service
Handles authentication, authorization, and multi-tenant isolation
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
import sys
import os

# Add parent directories to path for shared imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from shared.database import get_db, Base, engine
from shared.config import config
from app import models, schemas, auth_utils

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Auth & Tenant Service",
    description="Authentication and multi-tenant management",
    version="1.0.0"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/register", response_model=schemas.UserResponse)
async def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user and create/join tenant"""
    # Check if user exists
    db_user = models.User.get_by_email(db, user_data.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create or get tenant
    tenant = models.Tenant.get_or_create(db, user_data.tenant_name)
    
    # Create user
    hashed_password = auth_utils.hash_password(user_data.password)
    db_user = models.User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        tenant_id=tenant.id,
        role=schemas.TenantRole.ADMIN if tenant.created_by_user_id is None else schemas.TenantRole.ENGINEER
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Update tenant creator if first user
    if tenant.created_by_user_id is None:
        tenant.created_by_user_id = db_user.id
        db.commit()
    
    return schemas.UserResponse.from_orm(db_user)


@app.post("/token", response_model=schemas.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Authenticate user and return JWT token"""
    user = models.User.get_by_email(db, form_data.username)
    if not user or not auth_utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth_utils.create_access_token(
        data={"sub": user.email, "tenant_id": str(user.tenant_id), "user_id": str(user.id)}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me", response_model=schemas.UserResponse)
async def get_current_user(
    current_user: models.User = Depends(auth_utils.get_current_user)
):
    """Get current authenticated user"""
    return schemas.UserResponse.from_orm(current_user)


@app.get("/tenant/{tenant_id}", response_model=schemas.TenantResponse)
async def get_tenant(
    tenant_id: str,
    current_user: models.User = Depends(auth_utils.get_current_user),
    db: Session = Depends(get_db)
):
    """Get tenant information (only for users in that tenant)"""
    if str(current_user.tenant_id) != tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this tenant"
        )
    
    tenant = models.Tenant.get_by_id(db, tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )
    
    return schemas.TenantResponse.from_orm(tenant)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "auth-service"}

