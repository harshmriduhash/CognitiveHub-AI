# Auth & Tenant Service

Handles authentication, authorization, and multi-tenant isolation for Cognitive Dev Hub.

## Features

- User registration and authentication
- JWT-based authentication
- Multi-tenant support with organization isolation
- Role-based access control (Admin, Engineer, Viewer)
- Tenant management

## API Endpoints

- `POST /register` - Register new user
- `POST /token` - Login and get JWT token
- `GET /me` - Get current user info
- `GET /tenant/{tenant_id}` - Get tenant information
- `GET /health` - Health check

## Environment Variables

- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `JWT_SECRET_KEY` - Secret key for JWT signing
- `JWT_ALGORITHM` - JWT algorithm (default: HS256)
- `JWT_EXPIRATION_HOURS` - Token expiration time (default: 24)

