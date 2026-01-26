"""
Pydantic schemas for Insight Service
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any, List


class InsightRequest(BaseModel):
    """Schema for insight generation request"""
    source_type: str  # "analysis", "decision", "workflow"
    source_data: Dict[str, Any]
    context: Optional[Dict[str, Any]] = None
    project_id: Optional[str] = None


class InsightResponse(BaseModel):
    """Schema for insight response"""
    id: str
    type: str
    title: str
    content: str
    confidence: float
    metadata: Optional[Dict[str, Any]]
    project_id: Optional[str]
    created_at: datetime
    
    @classmethod
    def from_orm(cls, insight):
        """Create from ORM model"""
        return cls(
            id=str(insight.id),
            type=insight.type,
            title=insight.title,
            content=insight.content,
            confidence=insight.confidence,
            metadata=insight.metadata,
            project_id=str(insight.project_id) if insight.project_id else None,
            created_at=insight.created_at
        )
    
    class Config:
        from_attributes = True


class ReportCreate(BaseModel):
    """Schema for report creation"""
    report_type: str
    project_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class ReportResponse(BaseModel):
    """Schema for report response"""
    id: str
    title: str
    content: str
    report_type: str
    project_id: Optional[str]
    created_at: datetime
    
    @classmethod
    def from_orm(cls, report):
        """Create from ORM model"""
        return cls(
            id=str(report.id),
            title=report.title,
            content=report.content,
            report_type=report.report_type,
            project_id=str(report.project_id) if report.project_id else None,
            created_at=report.created_at
        )
    
    class Config:
        from_attributes = True

