"""
Code Generation Agent for the AutoGen multi-agent system.
This agent is responsible for generating Python code based on detailed specifications.
"""
import asyncio
from typing import Dict, Any
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from agents.provider import get_llm_model


# System message for the code generation agent
CODEGEN_AGENT_SYSTEM_MESSAGE = """
You are an expert Python developer. Generate clean, efficient, and well-documented Python code based on the provided requirements.

When generating code, follow these guidelines:
1. Write clean, readable code that follows PEP8 standards
2. Include appropriate comments and docstrings
3. Handle edge cases and error conditions
4. Write efficient code with good performance
5. Include type hints where appropriate
6. Follow Python best practices and conventions

Your response should be ONLY the generated Python code, with no additional explanation or markdown formatting.
"""


# Create the code generation agent
codegen_agent = AssistantAgent(
    name="CodegenAgent",
    system_message=CODEGEN_AGENT_SYSTEM_MESSAGE,
    model_client=get_llm_model()
)


async def generate_code(specification: Dict[str, Any]) -> str:
    """
    Generate Python code based on detailed specification.
    
    Args:
        specification: Detailed requirements specification
        
    Returns:
        Generated Python code as string
    """
    try:
        # Create a detailed prompt for code generation
        requirements = specification.get("original_requirements", "")
        language = specification.get("language", "python")
        complexity = specification.get("complexity", "medium")
        
        prompt = f"""
Generate {language} code for the following requirements:
Requirements: {requirements}
Complexity: {complexity}

Please generate clean, efficient, and well-documented code.
Include appropriate comments and follow best practices.
"""
        
        # Create a message for the agent
        message = TextMessage(
            content=prompt,
            source="user"
        )
        
        # Get response from the agent
        response = await codegen_agent.on_messages(
            [message], 
            CancellationToken()
        )
        
        # Extract the code from the response
        generated_code = response.chat_message.content
        return generated_code
        
    except Exception as e:
        print(f"Error generating code: {e}")
        # Return a simple error handling function
        return """
def error_handler():
    \"\"\"
    Error handler function.
    \"\"\"
    print("Error occurred during code generation")
    return None
"""


# Example usage
async def main():
    """Example of how to use the code generation agent."""
    specification = {
        "original_requirements": "Create a function that calculates fibonacci numbers",
        "language": "python",
        "complexity": "medium"
    }
    code = await generate_code(specification)
    print(f"Generated code:\n{code}")


if __name__ == "__main__":
    asyncio.run(main())