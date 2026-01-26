"""
Pydantic schemas for Project Context Service
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any


class ProjectCreate(BaseModel):
    """Schema for creating a project"""
    name: str
    description: Optional[str] = None
    tech_stack: Optional[List[str]] = None
    architecture_type: Optional[str] = None
    constraints: Optional[Dict[str, Any]] = None
    requirements: Optional[Dict[str, Any]] = None


class ProjectUpdate(BaseModel):
    """Schema for updating a project"""
    name: Optional[str] = None
    description: Optional[str] = None
    tech_stack: Optional[List[str]] = None
    architecture_type: Optional[str] = None
    constraints: Optional[Dict[str, Any]] = None
    requirements: Optional[Dict[str, Any]] = None


class ProjectResponse(BaseModel):
    """Schema for project response"""
    id: str
    name: str
    description: Optional[str]
    tech_stack: Optional[List[str]]
    architecture_type: Optional[str]
    constraints: Optional[Dict[str, Any]]
    requirements: Optional[Dict[str, Any]]
    tenant_id: str
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_orm(cls, project):
        """Create from ORM model"""
        return cls(
            id=str(project.id),
            name=project.name,
            description=project.description,
            tech_stack=project.tech_stack,
            architecture_type=project.architecture_type,
            constraints=project.constraints,
            requirements=project.requirements,
            tenant_id=str(project.tenant_id),
            created_at=project.created_at,
            updated_at=project.updated_at
        )
    
    class Config:
        from_attributes = True

