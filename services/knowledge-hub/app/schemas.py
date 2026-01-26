"""
Pydantic schemas for Knowledge Hub
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class DocumentCreate(BaseModel):
    """Schema for creating a document"""
    name: str
    content: str
    project_id: Optional[str] = None


class DocumentResponse(BaseModel):
    """Schema for document response"""
    id: str
    name: str
    tenant_id: str
    project_id: Optional[str]
    created_at: datetime
    
    @classmethod
    def from_orm(cls, document):
        """Create from ORM model"""
        return cls(
            id=str(document.id),
            name=document.name,
            tenant_id=str(document.tenant_id),
            project_id=str(document.project_id) if document.project_id else None,
            created_at=document.created_at
        )
    
    class Config:
        from_attributes = True


class SearchQuery(BaseModel):
    """Schema for search query"""
    query: str
    project_id: Optional[str] = None
    limit: Optional[int] = 10


class SearchResult(BaseModel):
    """Schema for search result"""
    document_id: str
    document_name: str
    content: str
    score: float


class SearchResponse(BaseModel):
    """Schema for search response"""
    query: str
    results: List[SearchResult]
    count: int

