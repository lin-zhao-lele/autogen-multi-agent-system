"""
Requirements Analysis Agent for the AutoGen multi-agent system.
This agent is responsible for understanding user requirements and breaking them down into detailed specifications.
"""
import asyncio
from typing import Dict, Any
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from agents.provider import get_llm_model


# System message for the requirements analysis agent
REQUIREMENTS_AGENT_SYSTEM_MESSAGE = """
You are an expert at analyzing and breaking down programming requirements. 
Your task is to understand user requirements and create a detailed specification for code implementation.

When analyzing requirements, consider:
1. What programming language should be used
2. What functionality needs to be implemented
3. What inputs and outputs are expected
4. Any specific constraints or requirements
5. Complexity level of the implementation

Provide a clear, structured breakdown of the requirements that can be used by other agents to generate code.
"""


def breakdown_requirements(requirements: str) -> Dict[str, Any]:
    """
    Break down complex requirements into structured components.
    
    Args:
        requirements: User requirements description
        
    Returns:
        Dictionary with structured requirements breakdown
    """
    # For now, we'll return a simple breakdown
    # In a more advanced implementation, this could use NLP to analyze requirements
    return {
        "original_requirements": requirements,
        "language": "python",  # Default to Python
        "complexity": "medium",  # Default complexity
        "functional_requirements": [],
        "non_functional_requirements": [],
        "constraints": []
    }


# Create the requirements analysis agent
requirements_agent = AssistantAgent(
    name="RequirementsAgent",
    system_message=REQUIREMENTS_AGENT_SYSTEM_MESSAGE,
    model_client=get_llm_model(),
    tools=[breakdown_requirements]
)


async def analyze_requirements(user_requirements: str) -> Dict[str, Any]:
    """
    Analyze user requirements and generate a detailed specification.
    
    Args:
        user_requirements: User requirements description
        
    Returns:
        Dictionary with detailed requirements specification
    """
    try:
        # Create a message for the agent
        message = TextMessage(
            content=f"Analyze the following requirements and provide a detailed specification: {user_requirements}",
            source="user"
        )
        
        # Get response from the agent
        await requirements_agent.on_messages(
            [message], 
            CancellationToken()
        )
        
        # For now, we'll use a simple breakdown
        # In a more advanced implementation, we could parse the agent's response
        specification = breakdown_requirements(user_requirements)
        return specification
        
    except Exception as e:
        print(f"Error analyzing requirements: {e}")
        # Return a default specification
        return {
            "original_requirements": user_requirements,
            "language": "python",
            "complexity": "medium",
            "functional_requirements": [],
            "non_functional_requirements": [],
            "constraints": []
        }


# Example usage
async def main():
    """Example of how to use the requirements analysis agent."""
    requirements = "Create a function that calculates fibonacci numbers"
    specification = await analyze_requirements(requirements)
    print(f"Specification: {specification}")


if __name__ == "__main__":
    asyncio.run(main())