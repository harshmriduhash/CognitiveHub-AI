# Knowledge Hub Service

RAG (Retrieval-Augmented Generation) and semantic search for engineering knowledge.

## Features

- Document ingestion (text, files)
- Semantic search using embeddings
- Vector storage with Qdrant
- Multi-tenant knowledge isolation
- Project-specific document organization

## API Endpoints

- `POST /documents` - Ingest a file document
- `POST /documents/text` - Ingest text content
- `POST /search` - Perform semantic search
- `GET /documents` - List documents for tenant
- `DELETE /documents/{document_id}` - Delete document
- `GET /health` - Health check

## Environment Variables

- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `QDRANT_URL` - Qdrant vector database URL
- `OPENAI_API_KEY` - OpenAI API key for embeddings

## Technology

- OpenAI embeddings (text-embedding-3-small)
- Qdrant vector database
- LangChain for text processing

