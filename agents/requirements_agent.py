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
你是一个专业的编程需求分析专家。你的任务是理解用户需求并创建详细的代码实现规范。

分析需求时请考虑：
1. 应该使用什么编程语言
2. 需要实现什么功能
3. 预期的输入和输出是什么
4. 任何特定的约束或要求
5. 实现的复杂度级别

请提供清晰、结构化的需求分解，以便其他智能体生成代码。

请用中文回答。
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
            content=f"请分析以下需求并提供详细的规范说明（请用中文回答）：{user_requirements}",
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