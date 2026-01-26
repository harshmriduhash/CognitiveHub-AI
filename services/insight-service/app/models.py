"""
Database models for Insight Service
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from shared.database import Base


class Insight(Base):
    """Insight model"""
    __tablename__ = "insights"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String, nullable=False, index=True)  # e.g., "analysis", "decision", "recommendation"
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    confidence = Column(Float, default=0.8)
    metadata = Column(JSON, nullable=True)
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    project_id = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    @classmethod
    def get_by_id(cls, db, insight_id: str):
        """Get insight by ID"""
        return db.query(cls).filter(cls.id == insight_id).first()
    
    @classmethod
    def get_by_tenant(
        cls, db, tenant_id: str, project_id: str = None,
        insight_type: str = None, limit: int = 50
    ):
        """Get insights for a tenant"""
        query = db.query(cls).filter(cls.tenant_id == tenant_id)
        if project_id:
            query = query.filter(cls.project_id == project_id)
        if insight_type:
            query = query.filter(cls.type == insight_type)
        return query.order_by(cls.created_at.desc()).limit(limit).all()


class Report(Base):
    """Report model"""
    __tablename__ = "reports"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    report_type = Column(String, nullable=False)  # e.g., "architecture_review", "decision_summary"
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    project_id = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    @classmethod
    def get_by_id(cls, db, report_id: str):
        """Get report by ID"""
        return db.query(cls).filter(cls.id == report_id).first()
    
    @classmethod
    def get_by_tenant(cls, db, tenant_id: str, project_id: str = None):
        """Get reports for a tenant"""
        query = db.query(cls).filter(cls.tenant_id == tenant_id)
        if project_id:
            query = query.filter(cls.project_id == project_id)
        return query.order_by(cls.created_at.desc()).all()

