"""
Database models for Project Context Service
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from datetime import datetime
import uuid
from shared.database import Base


class Project(Base):
    """Project/System context model"""
    __tablename__ = "projects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    tech_stack = Column(ARRAY(String), nullable=True)
    architecture_type = Column(String, nullable=True)  # e.g., "microservices", "monolith"
    constraints = Column(JSON, nullable=True)  # e.g., {"budget": 10000, "latency": "100ms"}
    requirements = Column(JSON, nullable=True)  # Functional and non-functional requirements
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @classmethod
    def get_by_id(cls, db, project_id: str):
        """Get project by ID"""
        return db.query(cls).filter(cls.id == project_id).first()
    
    @classmethod
    def get_by_tenant(cls, db, tenant_id: str):
        """Get all projects for a tenant"""
        return db.query(cls).filter(cls.tenant_id == tenant_id).all()

