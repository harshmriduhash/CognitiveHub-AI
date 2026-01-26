# Insight & Reporting Service

Converts AI output into structured insights and maintains historical decision records.

## Features

- Insight generation from AI analysis
- Historical decision tracking
- Report generation
- Multi-tenant insight isolation
- Project-specific insights

## Insight Types

- `analysis` - Architecture and system analysis insights
- `decision` - Decision recommendation insights
- `workflow` - Workflow execution insights
- `generic` - Generic insights

## API Endpoints

- `POST /generate` - Generate insight from AI output
- `GET /insights` - List insights for tenant
- `GET /insights/{insight_id}` - Get insight details
- `POST /reports` - Create comprehensive report
- `GET /reports` - List reports for tenant
- `GET /health` - Health check

## Environment Variables

- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string

