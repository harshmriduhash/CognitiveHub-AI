"""
Workflow execution logic
Orchestrates AI services to complete workflows
"""
import httpx
import sys
import os
from typing import Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from shared.config import config
from shared.database import SessionLocal
from shared.models import WorkflowStatus
from app import models


async def execute_workflow(workflow_id: str, tenant_id: str):
    """Execute a workflow by orchestrating AI services"""
    db = SessionLocal()
    try:
        workflow = models.Workflow.get_by_id(db, workflow_id)
        if not workflow:
            return
        
        # Update status to running
        workflow.status = WorkflowStatus.RUNNING
        db.commit()
        
        workflow_type = workflow.workflow_type
        input_data = workflow.input_data
        
        # Route to appropriate workflow handler
        if workflow_type == "architecture_analysis":
            result = await execute_architecture_analysis_workflow(input_data, tenant_id)
        elif workflow_type == "decision_support":
            result = await execute_decision_support_workflow(input_data, tenant_id)
        elif workflow_type == "full_analysis":
            result = await execute_full_analysis_workflow(input_data, tenant_id)
        else:
            raise ValueError(f"Unknown workflow type: {workflow_type}")
        
        # Update workflow with results
        workflow.output_data = result
        workflow.status = WorkflowStatus.COMPLETED
        workflow.completed_at = datetime.utcnow()
        db.commit()
        
    except Exception as e:
        workflow = models.Workflow.get_by_id(db, workflow_id)
        if workflow:
            workflow.status = WorkflowStatus.FAILED
            workflow.error_message = str(e)
            db.commit()
    finally:
        db.close()


async def execute_architecture_analysis_workflow(
    input_data: Dict[str, Any],
    tenant_id: str
) -> Dict[str, Any]:
    """Execute architecture analysis workflow"""
    async with httpx.AsyncClient() as client:
        # Step 1: Get project context
        project_id = input_data.get("project_id")
        project_context = {}
        if project_id:
            try:
                response = await client.get(
                    f"{config.PROJECT_CONTEXT_URL}/projects/{project_id}",
                    params={"tenant_id": tenant_id}
                )
                if response.status_code == 200:
                    project_context = response.json()
            except Exception as e:
                print(f"Error fetching project context: {e}")
        
        # Step 2: Retrieve relevant knowledge
        knowledge_results = []
        if input_data.get("research_required", True):
            try:
                response = await client.post(
                    f"{config.KNOWLEDGE_HUB_URL}/search",
                    json={
                        "query": input_data.get("system_description", {}).get("description", ""),
                        "project_id": project_id,
                        "limit": 5
                    },
                    params={"tenant_id": tenant_id}
                )
                if response.status_code == 200:
                    knowledge_results = response.json().get("results", [])
            except Exception as e:
                print(f"Error searching knowledge hub: {e}")
        
        # Step 3: Run system analysis
        analysis_result = {}
        try:
            response = await client.post(
                f"{config.SYSTEM_ANALYSIS_URL}/analyze",
                json={
                    "system_description": input_data.get("system_description", {}),
                    "analysis_types": input_data.get("analysis_types", []),
                    "context": project_context,
                    "knowledge": knowledge_results
                },
                params={"tenant_id": tenant_id}
            )
            if response.status_code == 200:
                analysis_result = response.json()
        except Exception as e:
            print(f"Error running system analysis: {e}")
        
        # Step 4: Generate insights
        insights = {}
        try:
            response = await client.post(
                f"{config.INSIGHT_SERVICE_URL}/generate",
                json={
                    "source_type": "analysis",
                    "source_data": analysis_result,
                    "project_id": project_id,
                    "context": project_context
                },
                params={"tenant_id": tenant_id}
            )
            if response.status_code == 200:
                insights = response.json()
        except Exception as e:
            print(f"Error generating insights: {e}")
        
        return {
            "knowledge": knowledge_results,
            "analysis": analysis_result,
            "insights": insights,
            "status": "completed"
        }


async def execute_decision_support_workflow(
    input_data: Dict[str, Any],
    tenant_id: str
) -> Dict[str, Any]:
    """Execute decision support workflow"""
    async with httpx.AsyncClient() as client:
        # Step 1: Get project context
        project_id = input_data.get("project_id")
        project_context = {}
        if project_id:
            try:
                response = await client.get(
                    f"{config.PROJECT_CONTEXT_URL}/projects/{project_id}",
                    params={"tenant_id": tenant_id}
                )
                if response.status_code == 200:
                    project_context = response.json()
            except Exception as e:
                print(f"Error fetching project context: {e}")
        
        # Step 2: Run decision engine
        decision_result = {}
        try:
            response = await client.post(
                f"{config.DECISION_ENGINE_URL}/evaluate",
                json={
                    "alternatives": input_data.get("alternatives", []),
                    "criteria": input_data.get("criteria", []),
                    "constraints": input_data.get("constraints", {}),
                    "goals": input_data.get("goals", []),
                    "context": project_context
                },
                params={"tenant_id": tenant_id}
            )
            if response.status_code == 200:
                decision_result = response.json()
        except Exception as e:
            print(f"Error running decision engine: {e}")
        
        # Step 3: Generate insights
        insights = {}
        try:
            response = await client.post(
                f"{config.INSIGHT_SERVICE_URL}/generate",
                json={
                    "source_type": "decision",
                    "source_data": decision_result,
                    "project_id": project_id,
                    "context": project_context
                },
                params={"tenant_id": tenant_id}
            )
            if response.status_code == 200:
                insights = response.json()
        except Exception as e:
            print(f"Error generating insights: {e}")
        
        return {
            "decision": decision_result,
            "insights": insights,
            "status": "completed"
        }


async def execute_full_analysis_workflow(
    input_data: Dict[str, Any],
    tenant_id: str
) -> Dict[str, Any]:
    """Execute full analysis workflow (research + analysis + decision)"""
    # Combine architecture analysis and decision support
    arch_result = await execute_architecture_analysis_workflow(input_data, tenant_id)
    decision_result = await execute_decision_support_workflow(input_data, tenant_id)
    
    return {
        "architecture_analysis": arch_result,
        "decision_support": decision_result,
        "status": "completed"
    }

