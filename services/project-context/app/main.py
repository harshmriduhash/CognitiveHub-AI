"""
Project Context Service
Manages engineering project metadata and system context
"""
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from shared.database import get_db, Base, engine
from app import models, schemas

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Project Context Service",
    description="Project metadata and system context management",
    version="1.0.0"
)


@app.post("/projects", response_model=schemas.ProjectResponse)
async def create_project(
    project: schemas.ProjectCreate,
    tenant_id: str,  # In production, get from auth token
    db: Session = Depends(get_db)
):
    """Create a new project"""
    db_project = models.Project(
        name=project.name,
        description=project.description,
        tech_stack=project.tech_stack,
        architecture_type=project.architecture_type,
        constraints=project.constraints,
        requirements=project.requirements,
        tenant_id=tenant_id
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return schemas.ProjectResponse.from_orm(db_project)


@app.get("/projects", response_model=List[schemas.ProjectResponse])
async def list_projects(
    tenant_id: str,  # In production, get from auth token
    db: Session = Depends(get_db)
):
    """List all projects for a tenant"""
    projects = models.Project.get_by_tenant(db, tenant_id)
    return [schemas.ProjectResponse.from_orm(p) for p in projects]


@app.get("/projects/{project_id}", response_model=schemas.ProjectResponse)
async def get_project(
    project_id: str,
    tenant_id: str,  # In production, get from auth token
    db: Session = Depends(get_db)
):
    """Get project by ID"""
    project = models.Project.get_by_id(db, project_id)
    if not project or str(project.tenant_id) != tenant_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return schemas.ProjectResponse.from_orm(project)


@app.put("/projects/{project_id}", response_model=schemas.ProjectResponse)
async def update_project(
    project_id: str,
    project_update: schemas.ProjectUpdate,
    tenant_id: str,  # In production, get from auth token
    db: Session = Depends(get_db)
):
    """Update project"""
    project = models.Project.get_by_id(db, project_id)
    if not project or str(project.tenant_id) != tenant_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Update fields
    update_data = project_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    return schemas.ProjectResponse.from_orm(project)


@app.delete("/projects/{project_id}")
async def delete_project(
    project_id: str,
    tenant_id: str,  # In production, get from auth token
    db: Session = Depends(get_db)
):
    """Delete project"""
    project = models.Project.get_by_id(db, project_id)
    if not project or str(project.tenant_id) != tenant_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    db.delete(project)
    db.commit()
    return {"message": "Project deleted"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "project-context"}

