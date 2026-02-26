"""
Decision Engine AI Service
Compares alternatives, evaluates trade-offs, and recommends decisions
"""
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import sys
import os

from shared.database import get_db, Base, engine
from shared.security import get_tenant_id
from app import schemas, decision_engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Decision Engine AI Service",
    description="AI-powered decision support and trade-off analysis",
    version="1.0.0"
)


@app.post("/evaluate", response_model=schemas.DecisionResponse)
async def evaluate_decision(
    request: schemas.DecisionRequest,
    tenant_id: str = Depends(get_tenant_id),
    db: Session = Depends(get_db)
):
    """Evaluate alternatives and provide decision recommendation"""
    decision_result = await decision_engine.evaluate(
        alternatives=request.alternatives,
        criteria=request.criteria,
        constraints=request.constraints or {},
        goals=request.goals or [],
        context=request.context or {}
    )
    
    return schemas.DecisionResponse(
        decision_id=decision_result.get("decision_id", ""),
        recommended_alternative=decision_result.get("recommended_alternative", ""),
        reasoning=decision_result.get("reasoning", ""),
        trade_offs=decision_result.get("trade_offs", {}),
        alternatives_analysis=decision_result.get("alternatives_analysis", []),
        confidence=decision_result.get("confidence", 0.8)
    )


@app.post("/compare", response_model=schemas.ComparisonResponse)
async def compare_alternatives(
    request: schemas.ComparisonRequest,
    tenant_id: str = Depends(get_tenant_id),
    db: Session = Depends(get_db)
):
    """Compare multiple alternatives side-by-side"""
    comparison_result = await decision_engine.compare(
        alternatives=request.alternatives,
        criteria=request.criteria,
        context=request.context or {}
    )
    
    return schemas.ComparisonResponse(
        alternatives=request.alternatives,
        criteria=request.criteria,
        comparison_matrix=comparison_result.get("comparison_matrix", {}),
        scores=comparison_result.get("scores", {}),
        recommendations=comparison_result.get("recommendations", [])
    )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "decision-engine"}

