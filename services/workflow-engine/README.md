# Workflow Engine Service

Orchestrates AI tasks and chains analysis steps automatically to create repeatable engineering processes.

## Features

- Workflow creation and management
- Automated AI task orchestration
- Workflow execution tracking
- Integration with all AI services
- Background task processing

## Workflow Types

- `architecture_analysis` - Full architecture evaluation workflow
- `decision_support` - Decision-making assistance workflow
- `full_analysis` - Combined research + analysis + decision workflow

## API Endpoints

- `POST /workflows` - Create and start a new workflow
- `GET /workflows` - List workflows for tenant
- `GET /workflows/{workflow_id}` - Get workflow status and results
- `GET /health` - Health check

## Environment Variables

- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `RABBITMQ_URL` - RabbitMQ connection string

