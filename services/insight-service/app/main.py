"""
Insight & Reporting Service
Converts AI output into structured insights and maintains historical decision records
"""
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import sys
import os

from shared.database import get_db, Base, engine
from shared.security import get_tenant_id
from app import models, schemas, insight_generator

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Insight & Reporting Service",
    description="Insight generation and historical decision tracking",
    version="1.0.0"
)


@app.post("/generate", response_model=schemas.InsightResponse)
async def generate_insight(
    request: schemas.InsightRequest,
    tenant_id: str = Depends(get_tenant_id),
    db: Session = Depends(get_db)
):
    """Generate insights from AI analysis or decision results"""
    insight = insight_generator.generate(
        source_type=request.source_type,
        source_data=request.source_data,
        context=request.context or {}
    )
    
    # Store insight
    db_insight = models.Insight(
        type=insight["type"],
        title=insight["title"],
        content=insight["content"],
        confidence=insight.get("confidence", 0.8),
        metadata=insight.get("metadata", {}),
        tenant_id=tenant_id,
        project_id=request.project_id
    )
    db.add(db_insight)
    db.commit()
    db.refresh(db_insight)
    
    return schemas.InsightResponse.from_orm(db_insight)


@app.get("/insights", response_model=List[schemas.InsightResponse])
async def list_insights(
    project_id: Optional[str] = None,
    insight_type: Optional[str] = None,
    limit: int = 50,
    tenant_id: str = Depends(get_tenant_id),
    db: Session = Depends(get_db)
):
    """List insights for a tenant"""
    insights = models.Insight.get_by_tenant(
        db, tenant_id, project_id, insight_type, limit
    )
    return [schemas.InsightResponse.from_orm(i) for i in insights]


@app.get("/insights/{insight_id}", response_model=schemas.InsightResponse)
async def get_insight(
    insight_id: str,
    tenant_id: str = Depends(get_tenant_id),
    db: Session = Depends(get_db)
):
    """Get insight by ID"""
    insight = models.Insight.get_by_id(db, insight_id)
    if not insight or str(insight.tenant_id) != tenant_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Insight not found"
        )
    return schemas.InsightResponse.from_orm(insight)


@app.post("/reports", response_model=schemas.ReportResponse)
async def create_report(
    request: schemas.ReportCreate,
    tenant_id: str = Depends(get_tenant_id),
    db: Session = Depends(get_db)
):
    """Create a comprehensive report from multiple insights"""
    # Get insights
    insights = models.Insight.get_by_tenant(
        db, tenant_id, request.project_id, limit=100
    )
    
    # Generate report
    report = insight_generator.generate_report(
        insights=[schemas.InsightResponse.from_orm(i).dict() for i in insights],
        report_type=request.report_type,
        context=request.context or {}
    )
    
    # Store report
    db_report = models.Report(
        title=report["title"],
        content=report["content"],
        report_type=request.report_type,
        tenant_id=tenant_id,
        project_id=request.project_id
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    
    return schemas.ReportResponse.from_orm(db_report)


@app.get("/reports", response_model=List[schemas.ReportResponse])
async def list_reports(
    project_id: Optional[str] = None,
    tenant_id: str = Depends(get_tenant_id),
    db: Session = Depends(get_db)
):
    """List reports for a tenant"""
    reports = models.Report.get_by_tenant(db, tenant_id, project_id)
    return [schemas.ReportResponse.from_orm(r) for r in reports]


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "insight-service"}

