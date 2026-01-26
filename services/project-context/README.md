# Project Context Service

Manages engineering project metadata and system context that feeds into AI reasoning.

## Features

- Project creation and management
- Tech stack tracking
- Architecture type specification
- Constraints and requirements storage
- Multi-tenant project isolation

## API Endpoints

- `POST /projects` - Create new project
- `GET /projects` - List all projects for tenant
- `GET /projects/{project_id}` - Get project details
- `PUT /projects/{project_id}` - Update project
- `DELETE /projects/{project_id}` - Delete project
- `GET /health` - Health check

## Environment Variables

- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string

