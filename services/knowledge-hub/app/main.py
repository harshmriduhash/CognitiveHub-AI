"""
Knowledge Hub Service
RAG (Retrieval-Augmented Generation) and semantic search for engineering knowledge
"""
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from shared.database import get_db, Base, engine
from app import models, schemas, rag_service

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Knowledge Hub Service",
    description="RAG and semantic search for engineering knowledge",
    version="1.0.0"
)


@app.post("/documents", response_model=schemas.DocumentResponse)
async def ingest_document(
    file: UploadFile = File(...),
    tenant_id: str = None,  # In production, get from auth token
    project_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Ingest a document into the knowledge base"""
    # Read file content
    content = await file.read()
    text_content = content.decode('utf-8')
    
    # Create document record
    db_document = models.Document(
        name=file.filename,
        content=text_content,
        tenant_id=tenant_id,
        project_id=project_id
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    
    # Process and index document
    await rag_service.index_document(str(db_document.id), text_content, tenant_id)
    
    return schemas.DocumentResponse.from_orm(db_document)


@app.post("/documents/text", response_model=schemas.DocumentResponse)
async def ingest_text(
    document: schemas.DocumentCreate,
    tenant_id: str = None,  # In production, get from auth token
    db: Session = Depends(get_db)
):
    """Ingest text content into the knowledge base"""
    db_document = models.Document(
        name=document.name,
        content=document.content,
        tenant_id=tenant_id,
        project_id=document.project_id
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    
    # Process and index document
    await rag_service.index_document(str(db_document.id), document.content, tenant_id)
    
    return schemas.DocumentResponse.from_orm(db_document)


@app.post("/search", response_model=schemas.SearchResponse)
async def semantic_search(
    query: schemas.SearchQuery,
    tenant_id: str = None,  # In production, get from auth token
    db: Session = Depends(get_db)
):
    """Perform semantic search on the knowledge base"""
    results = await rag_service.search(
        query.query,
        tenant_id=tenant_id,
        project_id=query.project_id,
        limit=query.limit or 10
    )
    
    return schemas.SearchResponse(
        query=query.query,
        results=results,
        count=len(results)
    )


@app.get("/documents", response_model=List[schemas.DocumentResponse])
async def list_documents(
    tenant_id: str,  # In production, get from auth token
    project_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List documents for a tenant"""
    documents = models.Document.get_by_tenant(db, tenant_id, project_id)
    return [schemas.DocumentResponse.from_orm(d) for d in documents]


@app.delete("/documents/{document_id}")
async def delete_document(
    document_id: str,
    tenant_id: str,  # In production, get from auth token
    db: Session = Depends(get_db)
):
    """Delete a document"""
    document = models.Document.get_by_id(db, document_id)
    if not document or str(document.tenant_id) != tenant_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Remove from vector store
    await rag_service.delete_document(str(document.id), tenant_id)
    
    db.delete(document)
    db.commit()
    return {"message": "Document deleted"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "knowledge-hub"}

