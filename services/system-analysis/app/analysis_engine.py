"""
System Analysis AI Engine
Uses AI to evaluate architectures and systems
"""
import os
import sys
from typing import Dict, Any, List
from openai import OpenAI

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from shared.config import config
from shared.models import AnalysisType

openai_client = OpenAI(api_key=config.OPENAI_API_KEY) if config.OPENAI_API_KEY else None


async def analyze(
    system_description: Dict[str, Any],
    analysis_types: List[AnalysisType],
    context: Dict[str, Any],
    knowledge: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Analyze a system using AI"""
    
    # Build analysis prompt
    prompt = build_analysis_prompt(system_description, analysis_types, context, knowledge)
    
    if openai_client:
        # Use OpenAI for analysis
        response = openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are an expert software architect and systems engineer. Analyze systems objectively and provide detailed insights."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        import json
        result = json.loads(response.choices[0].message.content)
        return result
    else:
        # Fallback: return structured mock analysis
        return generate_mock_analysis(system_description, analysis_types)


def build_analysis_prompt(
    system_description: Dict[str, Any],
    analysis_types: List[AnalysisType],
    context: Dict[str, Any],
    knowledge: List[Dict[str, Any]]
) -> str:
    """Build prompt for AI analysis"""
    
    prompt_parts = [
        "Analyze the following system architecture and provide a comprehensive evaluation.",
        "",
        "SYSTEM DESCRIPTION:",
        f"Name: {system_description.get('name', 'Unknown')}",
        f"Description: {system_description.get('description', 'N/A')}",
        f"Tech Stack: {', '.join(system_description.get('tech_stack', []))}",
        f"Architecture Type: {system_description.get('architecture_type', 'N/A')}",
    ]
    
    if context:
        prompt_parts.append("\nCONTEXT:")
        for key, value in context.items():
            prompt_parts.append(f"{key}: {value}")
    
    if knowledge:
        prompt_parts.append("\nRELEVANT KNOWLEDGE:")
        for item in knowledge[:5]:  # Limit to 5 knowledge items
            prompt_parts.append(f"- {item.get('content', '')[:200]}...")
    
    prompt_parts.append("\nANALYSIS TYPES REQUESTED:")
    for analysis_type in analysis_types:
        prompt_parts.append(f"- {analysis_type.value}")
    
    prompt_parts.append("""
Please provide a JSON response with the following structure:
{
    "strengths": ["list of strengths"],
    "weaknesses": ["list of weaknesses"],
    "risks": ["list of identified risks"],
    "recommendations": ["list of recommendations"],
    "metrics": {
        "scalability_score": 0.0-1.0,
        "reliability_score": 0.0-1.0,
        "cost_efficiency_score": 0.0-1.0,
        "security_score": 0.0-1.0,
        "performance_score": 0.0-1.0
    },
    "confidence": 0.0-1.0
}
""")
    
    return "\n".join(prompt_parts)


def generate_mock_analysis(
    system_description: Dict[str, Any],
    analysis_types: List[AnalysisType]
) -> Dict[str, Any]:
    """Generate mock analysis when AI is not available"""
    return {
        "strengths": [
            "Well-defined architecture",
            "Modern tech stack",
            "Clear separation of concerns"
        ],
        "weaknesses": [
            "Potential scalability bottlenecks",
            "Limited redundancy mechanisms"
        ],
        "risks": [
            "Single point of failure in critical components",
            "Potential cost overruns at scale"
        ],
        "recommendations": [
            "Implement caching layer",
            "Add monitoring and observability",
            "Consider horizontal scaling strategy"
        ],
        "metrics": {
            "scalability_score": 0.7,
            "reliability_score": 0.75,
            "cost_efficiency_score": 0.8,
            "security_score": 0.7,
            "performance_score": 0.75
        },
        "confidence": 0.75
    }

