"""
Database models for Auth Service
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from shared.database import Base
from shared.models import TenantRole


class Tenant(Base):
    """Tenant/Organization model for multi-tenancy"""
    __tablename__ = "tenants"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    users = relationship("User", back_populates="tenant")
    
    @classmethod
    def get_or_create(cls, db, name: str):
        """Get existing tenant or create new one"""
        tenant = db.query(cls).filter(cls.name == name).first()
        if not tenant:
            tenant = cls(name=name)
            db.add(tenant)
            db.commit()
            db.refresh(tenant)
        return tenant
    
    @classmethod
    def get_by_id(cls, db, tenant_id: str):
        """Get tenant by ID"""
        return db.query(cls).filter(cls.id == tenant_id).first()


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    role = Column(SQLEnum(TenantRole), default=TenantRole.ENGINEER)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(String, default="true")
    
    tenant = relationship("Tenant", back_populates="users")
    
    @classmethod
    def get_by_email(cls, db, email: str):
        """Get user by email"""
        return db.query(cls).filter(cls.email == email).first()
    
    @classmethod
    def get_by_id(cls, db, user_id: str):
        """Get user by ID"""
        return db.query(cls).filter(cls.id == user_id).first()

