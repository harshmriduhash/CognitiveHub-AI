"""
Database models for Workflow Engine
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from shared.database import Base
from shared.models import WorkflowStatus


class Workflow(Base):
    """Workflow execution model"""
    __tablename__ = "workflows"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    workflow_type = Column(String, nullable=False)  # e.g., "architecture_analysis", "decision_support"
    input_data = Column(JSON, nullable=False)
    output_data = Column(JSON, nullable=True)
    project_id = Column(UUID(as_uuid=True), nullable=True)
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    status = Column(SQLEnum(WorkflowStatus), default=WorkflowStatus.PENDING)
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    @classmethod
    def get_by_id(cls, db, workflow_id: str):
        """Get workflow by ID"""
        return db.query(cls).filter(cls.id == workflow_id).first()
    
    @classmethod
    def get_by_tenant(cls, db, tenant_id: str, project_id: Optional[str] = None):
        """Get workflows for a tenant"""
        query = db.query(cls).filter(cls.tenant_id == tenant_id)
        if project_id:
            query = query.filter(cls.project_id == project_id)
        return query.order_by(cls.created_at.desc()).all()

