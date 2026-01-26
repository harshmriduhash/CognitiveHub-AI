"""
Insight Generator
Converts AI output into structured insights
"""
from typing import Dict, Any, List
from datetime import datetime


def generate(
    source_type: str,
    source_data: Dict[str, Any],
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """Generate insight from source data"""
    
    if source_type == "analysis":
        return generate_analysis_insight(source_data, context)
    elif source_type == "decision":
        return generate_decision_insight(source_data, context)
    elif source_type == "workflow":
        return generate_workflow_insight(source_data, context)
    else:
        return generate_generic_insight(source_data, context)


def generate_analysis_insight(
    analysis_data: Dict[str, Any],
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """Generate insight from analysis results"""
    
    system_name = analysis_data.get("system_name", "System")
    results = analysis_data.get("results", {})
    
    strengths = results.get("strengths", [])
    weaknesses = results.get("weaknesses", [])
    risks = results.get("risks", [])
    recommendations = results.get("recommendations", [])
    
    # Build insight content
    content_parts = [
        f"## Analysis Summary for {system_name}",
        "",
        "### Strengths",
    ]
    for strength in strengths[:5]:
        content_parts.append(f"- {strength}")
    
    if weaknesses:
        content_parts.append("\n### Areas for Improvement")
        for weakness in weaknesses[:5]:
            content_parts.append(f"- {weakness}")
    
    if risks:
        content_parts.append("\n### Identified Risks")
        for risk in risks[:5]:
            content_parts.append(f"- {risk}")
    
    if recommendations:
        content_parts.append("\n### Recommendations")
        for rec in recommendations[:5]:
            content_parts.append(f"- {rec}")
    
    return {
        "type": "analysis",
        "title": f"Architecture Analysis: {system_name}",
        "content": "\n".join(content_parts),
        "confidence": results.get("confidence", 0.8),
        "metadata": {
            "system_name": system_name,
            "metrics": results.get("metrics", {})
        }
    }


def generate_decision_insight(
    decision_data: Dict[str, Any],
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """Generate insight from decision results"""
    
    recommended = decision_data.get("recommended_alternative", "Unknown")
    reasoning = decision_data.get("reasoning", "")
    trade_offs = decision_data.get("trade_offs", {})
    
    content_parts = [
        "## Decision Recommendation",
        "",
        f"**Recommended Alternative:** {recommended}",
        "",
        "### Reasoning",
        reasoning,
    ]
    
    if trade_offs:
        content_parts.append("\n### Trade-off Analysis")
        for alt, analysis in trade_offs.items():
            content_parts.append(f"\n#### {alt}")
            if "pros" in analysis:
                content_parts.append("**Pros:**")
                for pro in analysis["pros"][:3]:
                    content_parts.append(f"- {pro}")
            if "cons" in analysis:
                content_parts.append("**Cons:**")
                for con in analysis["cons"][:3]:
                    content_parts.append(f"- {con}")
    
    return {
        "type": "decision",
        "title": f"Decision Recommendation: {recommended}",
        "content": "\n".join(content_parts),
        "confidence": decision_data.get("confidence", 0.8),
        "metadata": {
            "recommended_alternative": recommended,
            "alternatives": list(trade_offs.keys())
        }
    }


def generate_workflow_insight(
    workflow_data: Dict[str, Any],
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """Generate insight from workflow results"""
    
    workflow_type = workflow_data.get("workflow_type", "workflow")
    output = workflow_data.get("output_data", {})
    
    return {
        "type": "workflow",
        "title": f"Workflow Results: {workflow_type}",
        "content": f"Workflow completed successfully. See details in output data.",
        "confidence": 0.9,
        "metadata": {
            "workflow_type": workflow_type,
            "output": output
        }
    }


def generate_generic_insight(
    source_data: Dict[str, Any],
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """Generate generic insight"""
    
    return {
        "type": "generic",
        "title": "Insight Generated",
        "content": "Analysis completed. Review the results for details.",
        "confidence": 0.7,
        "metadata": source_data
    }


def generate_report(
    insights: List[Dict[str, Any]],
    report_type: str,
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """Generate comprehensive report from insights"""
    
    content_parts = [
        "# Engineering Intelligence Report",
        f"**Report Type:** {report_type}",
        f"**Generated:** {datetime.utcnow().isoformat()}",
        "",
        "## Summary",
        f"This report contains {len(insights)} insights generated from analysis and decision-making processes.",
        "",
        "## Insights",
    ]
    
    for i, insight in enumerate(insights[:20], 1):  # Limit to 20 insights
        content_parts.append(f"\n### {i}. {insight.get('title', 'Insight')}")
        content_parts.append(insight.get('content', '')[:500] + "...")
    
    return {
        "title": f"{report_type.replace('_', ' ').title()} Report",
        "content": "\n".join(content_parts),
        "report_type": report_type
    }

