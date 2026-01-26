"""
Shared configuration utilities
"""
import os
from typing import Optional


class Config:
    """Base configuration"""
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://cognitivehub:cognitivehub_dev@localhost:5432/cognitivehub"
    )
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "dev-secret-key")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_HOURS: int = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))
    
    # AI Services
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # Vector DB
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_COLLECTION: str = os.getenv("QDRANT_COLLECTION", "knowledge_base")
    
    # Message Queue
    RABBITMQ_URL: str = os.getenv(
        "RABBITMQ_URL",
        "amqp://cognitivehub:cognitivehub_dev@localhost:5672/"
    )
    
    # Service URLs (for API Gateway)
    AUTH_SERVICE_URL: str = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")
    PROJECT_CONTEXT_URL: str = os.getenv("PROJECT_CONTEXT_URL", "http://localhost:8002")
    WORKFLOW_ENGINE_URL: str = os.getenv("WORKFLOW_ENGINE_URL", "http://localhost:8003")
    KNOWLEDGE_HUB_URL: str = os.getenv("KNOWLEDGE_HUB_URL", "http://localhost:8004")
    SYSTEM_ANALYSIS_URL: str = os.getenv("SYSTEM_ANALYSIS_URL", "http://localhost:8005")
    DECISION_ENGINE_URL: str = os.getenv("DECISION_ENGINE_URL", "http://localhost:8006")
    INSIGHT_SERVICE_URL: str = os.getenv("INSIGHT_SERVICE_URL", "http://localhost:8007")


config = Config()

