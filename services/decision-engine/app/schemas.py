"""
Pydantic schemas for Decision Engine Service
"""
from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class DecisionRequest(BaseModel):
    """Schema for decision evaluation request"""
    alternatives: List[str]
    criteria: List[str]
    constraints: Optional[Dict[str, Any]] = None
    goals: Optional[List[str]] = None
    context: Optional[Dict[str, Any]] = None


class ComparisonRequest(BaseModel):
    """Schema for comparison request"""
    alternatives: List[str]
    criteria: List[str]
    context: Optional[Dict[str, Any]] = None


class AlternativeAnalysis(BaseModel):
    """Schema for alternative analysis"""
    alternative: str
    pros: List[str]
    cons: List[str]
    score: float
    suitability: str  # "high", "medium", "low"


class DecisionResponse(BaseModel):
    """Schema for decision response"""
    decision_id: str
    recommended_alternative: str
    reasoning: str
    trade_offs: Dict[str, Any]
    alternatives_analysis: List[AlternativeAnalysis]
    confidence: float


class ComparisonResponse(BaseModel):
    """Schema for comparison response"""
    alternatives: List[str]
    criteria: List[str]
    comparison_matrix: Dict[str, Dict[str, Any]]
    scores: Dict[str, float]
    recommendations: List[str]

