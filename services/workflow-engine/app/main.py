"""
Workflow Engine Service
Orchestrates AI tasks and chains analysis steps automatically
"""
from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from shared.database import get_db, Base, engine
from shared.models import WorkflowStatus
from app import models, schemas, workflow_executor

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Workflow Engine",
    description="AI task orchestration and automation",
    version="1.0.0"
)


@app.post("/workflows", response_model=schemas.WorkflowResponse)
async def create_workflow(
    workflow: schemas.WorkflowCreate,
    tenant_id: str,  # In production, get from auth token
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create and start a new workflow"""
    db_workflow = models.Workflow(
        name=workflow.name,
        workflow_type=workflow.workflow_type,
        input_data=workflow.input_data,
        project_id=workflow.project_id,
        tenant_id=tenant_id,
        status=WorkflowStatus.PENDING
    )
    db.add(db_workflow)
    db.commit()
    db.refresh(db_workflow)
    
    # Start workflow execution in background
    background_tasks.add_task(
        workflow_executor.execute_workflow,
        str(db_workflow.id),
        tenant_id
    )
    
    return schemas.WorkflowResponse.from_orm(db_workflow)


@app.get("/workflows", response_model=List[schemas.WorkflowResponse])
async def list_workflows(
    tenant_id: str,  # In production, get from auth token
    project_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List workflows for a tenant"""
    workflows = models.Workflow.get_by_tenant(db, tenant_id, project_id)
    return [schemas.WorkflowResponse.from_orm(w) for w in workflows]


@app.get("/workflows/{workflow_id}", response_model=schemas.WorkflowResponse)
async def get_workflow(
    workflow_id: str,
    tenant_id: str,  # In production, get from auth token
    db: Session = Depends(get_db)
):
    """Get workflow by ID"""
    workflow = models.Workflow.get_by_id(db, workflow_id)
    if not workflow or str(workflow.tenant_id) != tenant_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found"
        )
    return schemas.WorkflowResponse.from_orm(workflow)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "workflow-engine"}

