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
你是一个专业的Python开发专家。根据提供的需求生成干净、高效、文档完善的Python代码。

生成代码时请遵循以下准则：
1. 编写符合PEP8标准的干净、可读代码
2. 不要注释
3. 处理边界情况和错误条件
4. 编写性能良好的高效代码
5. 遵循Python最佳实践和约定

你的回答应该只包含生成的代码，不要包含额外的解释或markdown格式。

请用中文回答。
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
请为以下需求生成{language}代码（请用中文回答）：
需求：{requirements}
复杂度：{complexity}

请生成干净、高效、文档完善的代码。
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