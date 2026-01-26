"""
Pydantic schemas for Auth Service
"""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from shared.models import TenantRole


class UserCreate(BaseModel):
    """Schema for user registration"""
    email: EmailStr
    password: str
    full_name: str
    tenant_name: str


class UserResponse(BaseModel):
    """Schema for user response"""
    id: str
    email: str
    full_name: Optional[str]
    tenant_id: str
    role: TenantRole
    created_at: datetime
    
    @classmethod
    def from_orm(cls, user):
        """Create from ORM model"""
        return cls(
            id=str(user.id),
            email=user.email,
            full_name=user.full_name,
            tenant_id=str(user.tenant_id),
            role=user.role,
            created_at=user.created_at
        )
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str


class TenantResponse(BaseModel):
    """Schema for tenant response"""
    id: str
    name: str
    created_at: datetime
    
    @classmethod
    def from_orm(cls, tenant):
        """Create from ORM model"""
        return cls(
            id=str(tenant.id),
            name=tenant.name,
            created_at=tenant.created_at
        )
    
    class Config:
        from_attributes = True

