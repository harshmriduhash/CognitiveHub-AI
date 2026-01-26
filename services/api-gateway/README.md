# API Gateway Service

Unified API gateway that routes requests to appropriate backend services and aggregates responses.

## Features

- Request routing to backend services
- CORS handling
- Request/response forwarding
- Service aggregation
- Health check aggregation

## Routes

- `/api/auth/*` - Auth service routes
- `/api/projects/*` - Project context service routes
- `/api/workflows/*` - Workflow engine routes
- `/api/knowledge/*` - Knowledge hub routes
- `/api/analysis/*` - System analysis service routes
- `/api/decisions/*` - Decision engine routes
- `/api/insights/*` - Insight service routes

## Environment Variables

- `AUTH_SERVICE_URL` - Auth service URL
- `PROJECT_CONTEXT_URL` - Project context service URL
- `WORKFLOW_ENGINE_URL` - Workflow engine URL
- `KNOWLEDGE_HUB_URL` - Knowledge hub URL
- `SYSTEM_ANALYSIS_URL` - System analysis service URL
- `DECISION_ENGINE_URL` - Decision engine URL
- `INSIGHT_SERVICE_URL` - Insight service URL

