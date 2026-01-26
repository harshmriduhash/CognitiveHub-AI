"""
Pydantic schemas for System Analysis Service
"""
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from shared.models import AnalysisType


class AnalysisRequest(BaseModel):
    """Schema for analysis request"""
    system_description: Dict[str, Any]
    analysis_types: Optional[List[AnalysisType]] = None
    context: Optional[Dict[str, Any]] = None
    knowledge: Optional[List[Dict[str, Any]]] = None


class BatchAnalysisRequest(BaseModel):
    """Schema for batch analysis request"""
    systems: List[Dict[str, Any]]
    analysis_types: Optional[List[AnalysisType]] = None
    context: Optional[Dict[str, Any]] = None
    knowledge: Optional[List[Dict[str, Any]]] = None


class AnalysisResult(BaseModel):
    """Schema for analysis result"""
    strengths: List[str]
    weaknesses: List[str]
    risks: List[str]
    recommendations: List[str]
    metrics: Dict[str, Any]
    confidence: float


class AnalysisResponse(BaseModel):
    """Schema for analysis response"""
    system_name: str
    analysis_types: List[AnalysisType]
    results: Dict[str, Any]
    confidence: float

