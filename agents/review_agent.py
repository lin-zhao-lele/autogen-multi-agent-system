"""
Code Review Agent for the AutoGen multi-agent system.
This agent is responsible for reviewing generated code for quality, PEP8 compliance, and best practices.
"""
import asyncio
from typing import List
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from agents.provider import get_llm_model
from agents.models import CodeReviewResult


# System message for the code review agent
REVIEW_AGENT_SYSTEM_MESSAGE = """
你是一个专业的Python代码审查专家。审查代码的质量、PEP8合规性和最佳实践。

审查代码时请考虑：
1. PEP8合规性和代码风格
2. 代码可读性和可维护性
3. 错误处理和边界情况
4. 性能和效率
5. 安全考虑
6. 最佳实践和设计模式

请提供详细的反馈和具体的改进建议。

请用中文回答。
"""


def check_pep8_compliance(code: str) -> bool:
    """
    Check if code complies with PEP8 standards.
    In a real implementation, this would use tools like pycodestyle or flake8.
    
    Args:
        code: Python code to check
        
    Returns:
        True if code complies with PEP8, False otherwise
    """
    # This is a simplified implementation
    # In a real implementation, we would use actual PEP8 checking tools
    return True


def identify_issues(code: str) -> List[str]:
    """
    Identify issues in the code.
    In a real implementation, this would use various code analysis tools.
    
    Args:
        code: Python code to analyze
        
    Returns:
        List of identified issues
    """
    # This is a simplified implementation
    # In a real implementation, we would use actual code analysis tools
    issues = []
    
    # Simple checks
    if "import *" in code:
        issues.append("Avoid 'import *' statements")
    
    if len(code.split('\n')) > 100:
        issues.append("Consider breaking long functions into smaller ones")
        
    return issues


def suggest_improvements(code: str) -> List[str]:
    """
    Suggest improvements for the code.
    
    Args:
        code: Python code to improve
        
    Returns:
        List of suggested improvements
    """
    # This is a simplified implementation
    # In a real implementation, we would provide more detailed suggestions
    suggestions = []
    
    if "TODO" in code:
        suggestions.append("Replace TODO comments with actual implementation")
        
    if "print(" in code:
        suggestions.append("Consider using logging instead of print statements")
        
    return suggestions


# Create the code review agent
review_agent = AssistantAgent(
    name="ReviewAgent",
    system_message=REVIEW_AGENT_SYSTEM_MESSAGE,
    model_client=get_llm_model()
)


async def review_code(code: str) -> CodeReviewResult:
    """
    Review code for quality, PEP8 compliance, and best practices.
    
    Args:
        code: Python code to review
        
    Returns:
        CodeReviewResult with review results
    """
    try:
        # Check PEP8 compliance
        pep8_compliance = check_pep8_compliance(code)
        
        # Identify issues
        issues = identify_issues(code)
        
        # Suggest improvements
        suggestions = suggest_improvements(code)
        
        # Create review comments
        review_comments = []
        if not pep8_compliance:
            review_comments.append("Code does not fully comply with PEP8 standards")
            
        for issue in issues:
            review_comments.append(f"Issue: {issue}")
            
        for suggestion in suggestions:
            review_comments.append(f"Suggestion: {suggestion}")
        
        # Create a detailed prompt for the agent
        prompt = f"""
请审查以下代码的质量、PEP8合规性和最佳实践（请用中文回答）：

代码：
```
{code}
```

请提供详细的反馈和具体的改进建议。
"""
        
        # Create a message for the agent
        message = TextMessage(
            content=prompt,
            source="user"
        )
        
        # Get response from the agent
        response = await review_agent.on_messages(
            [message], 
            CancellationToken()
        )
        
        # Extract the review feedback from the response
        agent_feedback = response.chat_message.content
        
        # Combine automated checks with agent feedback
        review_comments.append(f"Agent feedback: {agent_feedback}")
        
        return CodeReviewResult(
            code=code,
            issues=issues,
            suggestions=suggestions,
            pep8_compliance=pep8_compliance,
            review_comments=review_comments
        )
        
    except Exception as e:
        print(f"Error reviewing code: {e}")
        # Return a default review result
        return CodeReviewResult(
            code=code,
            issues=["Error occurred during code review"],
            suggestions=["Please review the code manually"],
            pep8_compliance=False,
            review_comments=[f"Error: {str(e)}"]
        )


# Example usage
async def main():
    """Example of how to use the code review agent."""
    sample_code = """
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))
"""
    
    review_result = await review_code(sample_code)
    print(f"Review result: {review_result}")


if __name__ == "__main__":
    asyncio.run(main())