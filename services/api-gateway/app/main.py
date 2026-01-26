"""
API Gateway Service
Routes requests to appropriate backend services and aggregates responses
"""
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from shared.config import config

app = FastAPI(
    title="Cognitive Dev Hub API Gateway",
    description="Unified API gateway for all services",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service URLs
SERVICES = {
    "auth": config.AUTH_SERVICE_URL,
    "project": config.PROJECT_CONTEXT_URL,
    "workflow": config.WORKFLOW_ENGINE_URL,
    "knowledge": config.KNOWLEDGE_HUB_URL,
    "analysis": config.SYSTEM_ANALYSIS_URL,
    "decision": config.DECISION_ENGINE_URL,
    "insight": config.INSIGHT_SERVICE_URL,
}


async def forward_request(service_name: str, path: str, method: str, request: Request):
    """Forward request to backend service"""
    service_url = SERVICES.get(service_name)
    if not service_url:
        raise HTTPException(status_code=404, detail=f"Service {service_name} not found")
    
    url = f"{service_url}{path}"
    
    # Get request body if present
    body = None
    if method in ["POST", "PUT", "PATCH"]:
        try:
            body = await request.body()
        except:
            pass
    
    # Get query parameters
    params = dict(request.query_params)
    
    # Forward headers (especially auth token)
    headers = dict(request.headers)
    headers.pop("host", None)
    headers.pop("content-length", None)
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=method,
                url=url,
                content=body,
                params=params,
                headers=headers,
                timeout=30.0
            )
            return JSONResponse(
                content=response.json() if response.headers.get("content-type", "").startswith("application/json") else {"data": response.text},
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")


# Auth routes
@app.api_route("/api/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def auth_proxy(path: str, request: Request):
    """Proxy requests to auth service"""
    return await forward_request("auth", f"/{path}", request.method, request)


# Project routes
@app.api_route("/api/projects/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def project_proxy(path: str, request: Request):
    """Proxy requests to project context service"""
    return await forward_request("project", f"/{path}", request.method, request)


# Workflow routes
@app.api_route("/api/workflows/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def workflow_proxy(path: str, request: Request):
    """Proxy requests to workflow engine"""
    return await forward_request("workflow", f"/{path}", request.method, request)


# Knowledge routes
@app.api_route("/api/knowledge/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def knowledge_proxy(path: str, request: Request):
    """Proxy requests to knowledge hub"""
    return await forward_request("knowledge", f"/{path}", request.method, request)


# Analysis routes
@app.api_route("/api/analysis/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def analysis_proxy(path: str, request: Request):
    """Proxy requests to system analysis service"""
    return await forward_request("analysis", f"/{path}", request.method, request)


# Decision routes
@app.api_route("/api/decisions/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def decision_proxy(path: str, request: Request):
    """Proxy requests to decision engine"""
    return await forward_request("decision", f"/{path}", request.method, request)


# Insight routes
@app.api_route("/api/insights/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def insight_proxy(path: str, request: Request):
    """Proxy requests to insight service"""
    return await forward_request("insight", f"/{path}", request.method, request)


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "api-gateway"}


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Cognitive Dev Hub API Gateway",
        "version": "1.0.0",
        "services": list(SERVICES.keys())
    }

