# Cognitive Dev Hub - Setup Guide

## Prerequisites

- Docker and Docker Compose installed
- OpenAI API key (for AI features)
- Git (for cloning the repository)

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd cognitive-dev-hub
```

### 2. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and set your OpenAI API key:

```bash
OPENAI_API_KEY=your-openai-api-key-here
```

### 3. Start All Services

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database
- Redis cache
- Qdrant vector database
- RabbitMQ message queue
- All backend services (ports 8001-8007)
- API Gateway (port 8000)
- Frontend (port 3000)

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **API Gateway**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### 5. Create Your First Account

1. Navigate to http://localhost:3000
2. Click "Sign up"
3. Enter your details:
   - Full Name
   - Organization Name (creates a new tenant)
   - Email
   - Password
4. You'll be automatically logged in

## Service URLs

When running with Docker Compose, services are accessible at:

- Auth Service: http://localhost:8001
- Project Context: http://localhost:8002
- Workflow Engine: http://localhost:8003
- Knowledge Hub: http://localhost:8004
- System Analysis: http://localhost:8005
- Decision Engine: http://localhost:8006
- Insight Service: http://localhost:8007
- API Gateway: http://localhost:8000

## Development Setup

### Backend Services

Each service can be run independently for development:

```bash
cd services/auth-service
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at http://localhost:3000 with hot-reload enabled.

## Database Setup

PostgreSQL is automatically initialized by Docker Compose. To manually set up:

```bash
docker exec -it cognitive-dev-hub-postgres-1 psql -U cognitivehub -d cognitivehub
```

## Troubleshooting

### Services Not Starting

1. Check Docker logs:
   ```bash
   docker-compose logs <service-name>
   ```

2. Verify environment variables are set correctly

3. Ensure ports are not already in use

### Database Connection Issues

1. Verify PostgreSQL is running:
   ```bash
   docker-compose ps postgres
   ```

2. Check database connection string in `.env`

### OpenAI API Issues

1. Verify your API key is correct
2. Check API quota/limits
3. Services will use mock data if API key is not set

## Stopping Services

```bash
docker-compose down
```

To remove volumes (deletes all data):

```bash
docker-compose down -v
```

## Production Deployment

For production deployment:

1. Update `.env` with production values
2. Use strong JWT secret keys
3. Configure proper CORS origins
4. Set up SSL/TLS certificates
5. Use managed databases (RDS, etc.)
6. Configure monitoring and logging
7. Set up CI/CD pipelines

## Next Steps

- Read [ARCHITECTURE.md](ARCHITECTURE.md) for system design details
- Check individual service READMEs for specific documentation
- Explore the API documentation at http://localhost:8000/docs

