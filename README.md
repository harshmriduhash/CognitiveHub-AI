# Cognitive Dev Hub – AI-Powered Engineering Intelligence Platform

A unified, AI-powered SaaS platform designed to support engineering teams throughout the entire technical decision lifecycle.

## 🎯 Project Overview

Cognitive Dev Hub acts as an "engineering co-pilot" that integrates backend services, AI models, and automation workflows into a single scalable SaaS system. The platform assists with:

- **Technical research** - Knowledge ingestion and semantic search
- **System and architecture analysis** - Automated evaluation and insights
- **Design trade-off evaluation** - Comparative analysis of alternatives
- **Engineering decision support** - AI-assisted recommendations
- **Automated reasoning and summarization** - Intelligent insights generation

## 🏗️ Architecture

The platform follows a microservices architecture with the following core services:

```
┌───────────────┐
│  Web / API UI │
└──────┬────────┘
       │
┌──────▼────────┐
│  API Gateway  │
└──────┬────────┘
       │
┌──────▼──────────────────────────────────────┐
│         Core Services Layer                  │
│  • Auth & Tenant Service                     │
│  • Project Context Service                   │
│  • Workflow Engine                           │
│  • Knowledge Hub (RAG)                       │
│  • System Analysis AI Service                │
│  • Decision Engine AI Service                │
│  • Insight & Reporting Service               │
└──────────────────────────────────────────────┘
```

## 📁 Project Structure

```
cognitive-dev-hub/
├── services/
│   ├── auth-service/          # Authentication & multi-tenant management
│   ├── project-context/       # Project metadata & context management
│   ├── workflow-engine/       # AI task orchestration
│   ├── knowledge-hub/         # RAG & semantic search
│   ├── system-analysis/       # Architecture analysis AI
│   ├── decision-engine/       # Decision support AI
│   ├── insight-service/       # Reporting & insights
│   └── api-gateway/           # Service routing & aggregation
├── frontend/                  # React-based web UI
├── shared/                    # Shared utilities & models
├── docker-compose.yml         # Local development setup
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL (or use Docker)
- Redis (or use Docker)

### Quick Start

```bash
# Start all services with Docker Compose
docker-compose up -d

# Or run services individually (see individual service READMEs)
```

## 🔧 Technology Stack

- **Backend**: Python, FastAPI, SQLAlchemy
- **Frontend**: React, TypeScript, Tailwind CSS
- **AI/ML**: OpenAI API, LangChain, Vector DB (Qdrant/Chroma)
- **Database**: PostgreSQL, Redis
- **Message Queue**: RabbitMQ/Celery
- **Containerization**: Docker

## 📚 Services Documentation

Each service has its own README with detailed documentation:
- [Auth Service](services/auth-service/README.md)
- [Project Context Service](services/project-context/README.md)
- [Workflow Engine](services/workflow-engine/README.md)
- [Knowledge Hub](services/knowledge-hub/README.md)
- [System Analysis Service](services/system-analysis/README.md)
- [Decision Engine](services/decision-engine/README.md)
- [Insight Service](services/insight-service/README.md)

## 🤝 Contributing

This is a portfolio project demonstrating enterprise-level AI platform architecture.

## 📄 License

MIT License

