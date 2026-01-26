"""
Decision Engine AI
Uses AI to evaluate alternatives and make recommendations
"""
import os
import sys
import uuid
from typing import Dict, Any, List
from openai import OpenAI

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from shared.config import config

openai_client = OpenAI(api_key=config.OPENAI_API_KEY) if config.OPENAI_API_KEY else None


async def evaluate(
    alternatives: List[str],
    criteria: List[str],
    constraints: Dict[str, Any],
    goals: List[str],
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """Evaluate alternatives and recommend a decision"""
    
    prompt = build_evaluation_prompt(alternatives, criteria, constraints, goals, context)
    
    if openai_client:
        response = openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are an expert engineering decision advisor. Evaluate alternatives objectively and provide clear recommendations with reasoning."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        import json
        result = json.loads(response.choices[0].message.content)
        result["decision_id"] = str(uuid.uuid4())
        return result
    else:
        return generate_mock_decision(alternatives, criteria)


async def compare(
    alternatives: List[str],
    criteria: List[str],
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """Compare alternatives side-by-side"""
    
    prompt = build_comparison_prompt(alternatives, criteria, context)
    
    if openai_client:
        response = openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are an expert engineering decision advisor. Compare alternatives objectively across criteria."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        import json
        return json.loads(response.choices[0].message.content)
    else:
        return generate_mock_comparison(alternatives, criteria)


def build_evaluation_prompt(
    alternatives: List[str],
    criteria: List[str],
    constraints: Dict[str, Any],
    goals: List[str],
    context: Dict[str, Any]
) -> str:
    """Build prompt for decision evaluation"""
    
    prompt_parts = [
        "Evaluate the following alternatives and provide a recommendation.",
        "",
        "ALTERNATIVES:",
    ]
    for i, alt in enumerate(alternatives, 1):
        prompt_parts.append(f"{i}. {alt}")
    
    prompt_parts.append("\nEVALUATION CRITERIA:")
    for criterion in criteria:
        prompt_parts.append(f"- {criterion}")
    
    if goals:
        prompt_parts.append("\nGOALS:")
        for goal in goals:
            prompt_parts.append(f"- {goal}")
    
    if constraints:
        prompt_parts.append("\nCONSTRAINTS:")
        for key, value in constraints.items():
            prompt_parts.append(f"- {key}: {value}")
    
    if context:
        prompt_parts.append("\nCONTEXT:")
        for key, value in context.items():
            prompt_parts.append(f"{key}: {value}")
    
    prompt_parts.append("""
Please provide a JSON response with the following structure:
{
    "recommended_alternative": "name of recommended alternative",
    "reasoning": "detailed reasoning for the recommendation",
    "trade_offs": {
        "alternative_name": {
            "pros": ["list of advantages"],
            "cons": ["list of disadvantages"],
            "score": 0.0-1.0
        }
    },
    "alternatives_analysis": [
        {
            "alternative": "name",
            "pros": ["list"],
            "cons": ["list"],
            "score": 0.0-1.0,
            "suitability": "high|medium|low"
        }
    ],
    "confidence": 0.0-1.0
}
""")
    
    return "\n".join(prompt_parts)


def build_comparison_prompt(
    alternatives: List[str],
    criteria: List[str],
    context: Dict[str, Any]
) -> str:
    """Build prompt for comparison"""
    
    prompt_parts = [
        "Compare the following alternatives across the specified criteria.",
        "",
        "ALTERNATIVES:",
    ]
    for alt in alternatives:
        prompt_parts.append(f"- {alt}")
    
    prompt_parts.append("\nCRITERIA:")
    for criterion in criteria:
        prompt_parts.append(f"- {criterion}")
    
    if context:
        prompt_parts.append("\nCONTEXT:")
        for key, value in context.items():
            prompt_parts.append(f"{key}: {value}")
    
    prompt_parts.append("""
Please provide a JSON response with:
{
    "comparison_matrix": {
        "alternative_name": {
            "criterion_name": "evaluation text"
        }
    },
    "scores": {
        "alternative_name": 0.0-1.0
    },
    "recommendations": ["list of recommendations"]
}
""")
    
    return "\n".join(prompt_parts)


def generate_mock_decision(
    alternatives: List[str],
    criteria: List[str]
) -> Dict[str, Any]:
    """Generate mock decision when AI is not available"""
    return {
        "decision_id": str(uuid.uuid4()),
        "recommended_alternative": alternatives[0] if alternatives else "Unknown",
        "reasoning": "Based on the evaluation criteria, this alternative provides the best balance of factors.",
        "trade_offs": {
            alt: {
                "pros": [f"Advantage 1 for {alt}", f"Advantage 2 for {alt}"],
                "cons": [f"Disadvantage 1 for {alt}"],
                "score": 0.7 + (i * 0.1)
            }
            for i, alt in enumerate(alternatives)
        },
        "alternatives_analysis": [
            {
                "alternative": alt,
                "pros": [f"Pro 1", f"Pro 2"],
                "cons": [f"Con 1"],
                "score": 0.7 + (i * 0.1),
                "suitability": "high" if i == 0 else "medium"
            }
            for i, alt in enumerate(alternatives)
        ],
        "confidence": 0.75
    }


def generate_mock_comparison(
    alternatives: List[str],
    criteria: List[str]
) -> Dict[str, Any]:
    """Generate mock comparison when AI is not available"""
    return {
        "comparison_matrix": {
            alt: {
                criterion: f"Evaluation of {alt} on {criterion}"
                for criterion in criteria
            }
            for alt in alternatives
        },
        "scores": {
            alt: 0.7 + (i * 0.1)
            for i, alt in enumerate(alternatives)
        },
        "recommendations": [
            "Consider the trade-offs carefully",
            "Evaluate based on your specific requirements"
        ]
    }

