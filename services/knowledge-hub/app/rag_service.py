"""
RAG (Retrieval-Augmented Generation) service
Handles document indexing and semantic search
"""
import os
import sys
from typing import List, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from openai import OpenAI
import uuid

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from shared.config import config

# Initialize clients
qdrant_client = QdrantClient(url=config.QDRANT_URL)
openai_client = OpenAI(api_key=config.OPENAI_API_KEY) if config.OPENAI_API_KEY else None

# Embedding model
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIM = 1536  # Dimension for text-embedding-3-small


def get_collection_name(tenant_id: str) -> str:
    """Get collection name for tenant"""
    return f"{config.QDRANT_COLLECTION}_{tenant_id}"


async def ensure_collection(tenant_id: str):
    """Ensure collection exists for tenant"""
    collection_name = get_collection_name(tenant_id)
    try:
        qdrant_client.get_collection(collection_name)
    except Exception:
        # Create collection if it doesn't exist
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=EMBEDDING_DIM,
                distance=Distance.COSINE
            )
        )


async def get_embedding(text: str) -> List[float]:
    """Get embedding for text using OpenAI"""
    if not openai_client:
        # Fallback: return zero vector (in production, use a local model)
        return [0.0] * EMBEDDING_DIM
    
    response = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding


async def index_document(document_id: str, content: str, tenant_id: str):
    """Index a document in the vector store"""
    await ensure_collection(tenant_id)
    collection_name = get_collection_name(tenant_id)
    
    # Split content into chunks (simple chunking - in production, use proper text splitting)
    chunk_size = 1000
    chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
    
    points = []
    for i, chunk in enumerate(chunks):
        embedding = await get_embedding(chunk)
        point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{document_id}_{i}"))
        points.append(
            PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "document_id": document_id,
                    "chunk_index": i,
                    "content": chunk,
                    "tenant_id": tenant_id
                }
            )
        )
    
    # Upsert points
    qdrant_client.upsert(
        collection_name=collection_name,
        points=points
    )


async def search(
    query: str,
    tenant_id: str,
    project_id: Optional[str] = None,
    limit: int = 10
) -> List[dict]:
    """Perform semantic search"""
    collection_name = get_collection_name(tenant_id)
    
    try:
        # Get query embedding
        query_embedding = await get_embedding(query)
        
        # Search in Qdrant
        search_results = qdrant_client.search(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=limit,
            query_filter={
                "must": [
                    {"key": "tenant_id", "match": {"value": tenant_id}}
                ]
            } if tenant_id else None
        )
        
        # Format results
        results = []
        seen_docs = set()
        for result in search_results:
            doc_id = result.payload.get("document_id")
            if doc_id and doc_id not in seen_docs:
                seen_docs.add(doc_id)
                results.append({
                    "document_id": doc_id,
                    "document_name": result.payload.get("document_name", "Unknown"),
                    "content": result.payload.get("content", ""),
                    "score": result.score
                })
        
        return results
    except Exception as e:
        # Collection might not exist
        return []


async def delete_document(document_id: str, tenant_id: str):
    """Delete document from vector store"""
    collection_name = get_collection_name(tenant_id)
    try:
        # Delete all points for this document
        qdrant_client.delete(
            collection_name=collection_name,
            points_selector={
                "filter": {
                    "must": [
                        {"key": "document_id", "match": {"value": document_id}}
                    ]
                }
            }
        )
    except Exception:
        pass  # Collection or document might not exist

