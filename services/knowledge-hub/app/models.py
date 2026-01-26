"""
Database models for Knowledge Hub
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from shared.database import Base


class Document(Base):
    """Document model for knowledge base"""
    __tablename__ = "documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    project_id = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    @classmethod
    def get_by_id(cls, db, document_id: str):
        """Get document by ID"""
        return db.query(cls).filter(cls.id == document_id).first()
    
    @classmethod
    def get_by_tenant(cls, db, tenant_id: str, project_id: Optional[str] = None):
        """Get documents for a tenant"""
        query = db.query(cls).filter(cls.tenant_id == tenant_id)
        if project_id:
            query = query.filter(cls.project_id == project_id)
        return query.order_by(cls.created_at.desc()).all()

