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
            # In production, call project-context service
            pass
        
        # Step 2: Retrieve relevant knowledge
        knowledge_results = {}
        if input_data.get("research_required", True):
            # Call knowledge hub for research
            # knowledge_results = await client.post(
            #     f"{config.KNOWLEDGE_HUB_URL}/search",
            #     json={"query": input_data.get("system_description", "")}
            # )
            pass
        
        # Step 3: Run system analysis
        analysis_result = {}
        # analysis_result = await client.post(
        #     f"{config.SYSTEM_ANALYSIS_URL}/analyze",
        #     json={
        #         "system_description": input_data.get("system_description", ""),
        #         "context": project_context,
        #         "knowledge": knowledge_results
        #     }
        # )
        
        # Step 4: Generate insights
        insights = {}
        # insights = await client.post(
        #     f"{config.INSIGHT_SERVICE_URL}/generate",
        #     json={"analysis": analysis_result}
        # )
        
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
        
        # Step 2: Run decision engine
        decision_result = {}
        # decision_result = await client.post(
        #     f"{config.DECISION_ENGINE_URL}/evaluate",
        #     json={
        #         "alternatives": input_data.get("alternatives", []),
        #         "criteria": input_data.get("criteria", []),
        #         "context": input_data.get("context", {})
        #     }
        # )
        
        # Step 3: Generate insights
        insights = {}
        # insights = await client.post(
        #     f"{config.INSIGHT_SERVICE_URL}/generate",
        #     json={"decision": decision_result}
        # )
        
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

