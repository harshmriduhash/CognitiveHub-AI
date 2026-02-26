"""
System Analysis AI Service
Evaluates architectures and identifies bottlenecks, scalability, reliability, cost
"""
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import sys
import os

from shared.database import get_db, Base, engine
from shared.security import get_tenant_id
from shared.models import AnalysisType
from app import schemas, analysis_engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="System Analysis AI Service",
    description="AI-powered architecture and system analysis",
    version="1.0.0"
)


@app.post("/analyze", response_model=schemas.AnalysisResponse)
async def analyze_system(
    request: schemas.AnalysisRequest,
    tenant_id: str = Depends(get_tenant_id),
    db: Session = Depends(get_db)
):
    """Analyze a system architecture"""
    analysis_result = await analysis_engine.analyze(
        system_description=request.system_description,
        analysis_types=request.analysis_types or [AnalysisType.ARCHITECTURE],
        context=request.context or {},
        knowledge=request.knowledge or []
    )
    
    return schemas.AnalysisResponse(
        system_name=request.system_description.get("name", "Unknown"),
        analysis_types=request.analysis_types or [AnalysisType.ARCHITECTURE],
        results=analysis_result,
        confidence=analysis_result.get("confidence", 0.8)
    )


@app.post("/analyze/batch", response_model=List[schemas.AnalysisResponse])
async def analyze_systems_batch(
    request: schemas.BatchAnalysisRequest,
    tenant_id: str = Depends(get_tenant_id),
    db: Session = Depends(get_db)
):
    """Analyze multiple systems"""
    results = []
    for system_desc in request.systems:
        analysis_result = await analysis_engine.analyze(
            system_description=system_desc,
            analysis_types=request.analysis_types or [AnalysisType.ARCHITECTURE],
            context=request.context or {},
            knowledge=request.knowledge or []
        )
        results.append(schemas.AnalysisResponse(
            system_name=system_desc.get("name", "Unknown"),
            analysis_types=request.analysis_types or [AnalysisType.ARCHITECTURE],
            results=analysis_result,
            confidence=analysis_result.get("confidence", 0.8)
        ))
    
    return results


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "system-analysis"}

