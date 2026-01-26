"""
Shared data models across all services
"""
from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from enum import Enum


class TenantRole(str, Enum):
    """User roles within a tenant"""
    ADMIN = "admin"
    ENGINEER = "engineer"
    VIEWER = "viewer"


class WorkflowStatus(str, Enum):
    """Workflow execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AnalysisType(str, Enum):
    """Types of system analysis"""
    ARCHITECTURE = "architecture"
    SCALABILITY = "scalability"
    RELIABILITY = "reliability"
    COST = "cost"
    SECURITY = "security"
    PERFORMANCE = "performance"


class DecisionContext(BaseModel):
    """Context for decision-making"""
    alternatives: List[str]
    criteria: List[str]
    constraints: Optional[Dict[str, Any]] = None
    goals: Optional[List[str]] = None


class SystemDescription(BaseModel):
    """System description for analysis"""
    name: str
    description: str
    tech_stack: List[str]
    architecture_type: Optional[str] = None
    constraints: Optional[Dict[str, Any]] = None
    requirements: Optional[Dict[str, Any]] = None


class Insight(BaseModel):
    """Generated insight"""
    id: str
    type: str
    title: str
    content: str
    confidence: float = Field(ge=0.0, le=1.0)
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime


class Recommendation(BaseModel):
    """AI-generated recommendation"""
    id: str
    decision_id: str
    recommended_alternative: str
    reasoning: str
    trade_offs: Dict[str, Any]
    confidence: float = Field(ge=0.0, le=1.0)
    created_at: datetime

