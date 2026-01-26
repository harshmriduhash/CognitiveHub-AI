# Cognitive Dev Hub - Architecture Documentation

## System Architecture Overview

Cognitive Dev Hub is built as a microservices-based SaaS platform with the following architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (React)                        │
│                  Port: 3000 (Nginx)                          │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                    API Gateway                              │
│                  Port: 8000                                 │
│         Routes requests to backend services                  │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼──────┐ ┌─────▼──────┐ ┌──────▼──────┐
│ Auth Service │ │  Project   │ │  Workflow   │
│   Port: 8001 │ │  Context   │ │   Engine    │
│              │ │ Port: 8002 │ │ Port: 8003  │
└──────────────┘ └────────────┘ └─────────────┘
        │               │               │
        └───────────────┼───────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼──────┐ ┌─────▼──────┐ ┌──────▼──────┐
│  Knowledge   │ │   System    │ │  Decision   │
│     Hub      │ │  Analysis   │ │   Engine    │
│ Port: 8004   │ │ Port: 8005  │ │ Port: 8006  │
└──────────────┘ └────────────┘ └─────────────┘
        │               │               │
        └───────────────┼───────────────┘
                        │
                ┌───────▼──────┐
                │   Insight    │
                │   Service    │
                │ Port: 8007   │
                └──────────────┘
```

## Core Services

### 1. Auth & Tenant Service (Port 8001)
- **Purpose**: Authentication, authorization, and multi-tenant isolation
- **Technologies**: FastAPI, JWT, PostgreSQL
- **Key Features**:
  - User registration and authentication
  - JWT token generation and validation
  - Tenant/organization management
  - Role-based access control

### 2. Project Context Service (Port 8002)
- **Purpose**: Manages engineering project metadata and system context
- **Technologies**: FastAPI, PostgreSQL
- **Key Features**:
  - Project creation and management
  - Tech stack tracking
  - Architecture type specification
  - Constraints and requirements storage

### 3. Workflow Engine (Port 8003)
- **Purpose**: Orchestrates AI tasks and chains analysis steps
- **Technologies**: FastAPI, PostgreSQL, Background Tasks
- **Key Features**:
  - Workflow creation and execution
  - AI service orchestration
  - Background task processing
  - Workflow status tracking

### 4. Knowledge Hub (Port 8004)
- **Purpose**: RAG and semantic search for engineering knowledge
- **Technologies**: FastAPI, PostgreSQL, Qdrant, OpenAI Embeddings
- **Key Features**:
  - Document ingestion
  - Vector embeddings generation
  - Semantic search
  - Multi-tenant knowledge isolation

### 5. System Analysis AI Service (Port 8005)
- **Purpose**: AI-powered architecture and system analysis
- **Technologies**: FastAPI, OpenAI GPT-4
- **Key Features**:
  - Architecture evaluation
  - Scalability analysis
  - Reliability assessment
  - Risk identification
  - Recommendation generation

### 6. Decision Engine AI Service (Port 8006)
- **Purpose**: AI-powered decision support and trade-off analysis
- **Technologies**: FastAPI, OpenAI GPT-4
- **Key Features**:
  - Alternative evaluation
  - Trade-off analysis
  - Decision recommendations
  - Side-by-side comparison

### 7. Insight & Reporting Service (Port 8007)
- **Purpose**: Converts AI output into structured insights
- **Technologies**: FastAPI, PostgreSQL
- **Key Features**:
  - Insight generation
  - Historical decision tracking
  - Report generation
  - Multi-tenant insight isolation

### 8. API Gateway (Port 8000)
- **Purpose**: Unified entry point for all backend services
- **Technologies**: FastAPI, HTTPX
- **Key Features**:
  - Request routing
  - CORS handling
  - Service aggregation
  - Health check aggregation

## Data Flow

### Architecture Analysis Workflow
1. User submits system description via frontend
2. API Gateway routes to Workflow Engine
3. Workflow Engine:
   - Retrieves project context from Project Context Service
   - Searches knowledge base via Knowledge Hub
   - Calls System Analysis AI Service
   - Generates insights via Insight Service
4. Results returned to user

### Decision Support Workflow
1. User provides alternatives and criteria
2. API Gateway routes to Workflow Engine
3. Workflow Engine:
   - Calls Decision Engine AI Service
   - Generates insights via Insight Service
4. Recommendations returned to user

## Technology Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **Cache**: Redis
- **Vector DB**: Qdrant
- **Message Queue**: RabbitMQ
- **AI/ML**: OpenAI API (GPT-4, Embeddings)

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Routing**: React Router

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Web Server**: Nginx (for frontend)

## Database Schema

### Core Tables
- `tenants` - Organizations/tenants
- `users` - User accounts
- `projects` - Engineering projects
- `workflows` - Workflow executions
- `documents` - Knowledge base documents
- `insights` - Generated insights
- `reports` - Generated reports

## Security

- JWT-based authentication
- Multi-tenant data isolation
- Role-based access control
- CORS configuration
- Environment variable management

## Scalability Considerations

- Stateless services for horizontal scaling
- Independent service scaling
- Async workflow processing
- Database connection pooling
- Redis caching layer
- Vector database for efficient semantic search

## Deployment

All services are containerized and can be deployed using Docker Compose. Each service:
- Has its own Dockerfile
- Exposes a specific port
- Connects to shared databases (PostgreSQL, Redis, Qdrant)
- Can be scaled independently

## Future Enhancements

- Kubernetes deployment configuration
- Service mesh integration
- Advanced caching strategies
- Real-time updates via WebSockets
- Enhanced monitoring and observability
- CI/CD pipeline configuration

