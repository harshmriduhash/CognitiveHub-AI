"""
Pydantic schemas for Workflow Engine
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any
from shared.models import WorkflowStatus


class WorkflowCreate(BaseModel):
    """Schema for creating a workflow"""
    name: str
    workflow_type: str
    input_data: Dict[str, Any]
    project_id: Optional[str] = None


class WorkflowResponse(BaseModel):
    """Schema for workflow response"""
    id: str
    name: str
    workflow_type: str
    input_data: Dict[str, Any]
    output_data: Optional[Dict[str, Any]]
    project_id: Optional[str]
    tenant_id: str
    status: WorkflowStatus
    error_message: Optional[str]
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]
    
    @classmethod
    def from_orm(cls, workflow):
        """Create from ORM model"""
        return cls(
            id=str(workflow.id),
            name=workflow.name,
            workflow_type=workflow.workflow_type,
            input_data=workflow.input_data,
            output_data=workflow.output_data,
            project_id=str(workflow.project_id) if workflow.project_id else None,
            tenant_id=str(workflow.tenant_id),
            status=workflow.status,
            error_message=workflow.error_message,
            created_at=workflow.created_at,
            updated_at=workflow.updated_at,
            completed_at=workflow.completed_at
        )
    
    class Config:
        from_attributes = True

