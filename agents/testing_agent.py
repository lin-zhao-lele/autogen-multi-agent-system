"""
Testing Agent for the AutoGen multi-agent system.
This agent is responsible for generating test cases and test code for the generated code.
"""
import asyncio
from typing import List
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from agents.provider import get_llm_model
from agents.models import GeneratedTestResult


# System message for the testing agent
TESTING_AGENT_SYSTEM_MESSAGE = """
你是一个专业的Python测试工程师。为Python函数生成全面的测试用例和测试代码。

生成测试时请考虑：
1. 正常情况的单元测试
2. 边界情况测试
3. 错误条件测试
4. 边界值测试
5. 性能测试（如果适用）
6. 代码覆盖率目标
7. pytest最佳实践

请生成干净、可读的测试代码。

请用中文回答。
"""


def identify_test_cases(code: str) -> List[str]:
    """
    Identify test cases needed for the code.
    
    Args:
        code: Python code to analyze
        
    Returns:
        List of identified test cases
    """
    # This is a simplified implementation
    # In a real implementation, we would use more sophisticated analysis
    test_cases = []
    
    if "def " in code:
        test_cases.append("Test normal input cases")
        test_cases.append("Test edge cases")
        test_cases.append("Test error conditions")
        test_cases.append("Test boundary values")
        
    return test_cases


def estimate_coverage(test_cases: List[str]) -> float:
    """
    Estimate code coverage based on test cases.
    
    Args:
        test_cases: List of test cases
        
    Returns:
        Estimated code coverage percentage
    """
    # This is a simplified implementation
    # In a real implementation, we would use actual coverage tools
    return min(len(test_cases) * 25.0, 100.0)  # Assume each test case covers 25%


# Create the testing agent
testing_agent = AssistantAgent(
    name="TestingAgent",
    system_message=TESTING_AGENT_SYSTEM_MESSAGE,
    model_client=get_llm_model()
)


async def generate_tests(code: str) -> GeneratedTestResult:
    """
    Generate test cases and test code for the given code.
    
    Args:
        code: Python code to generate tests for
        
    Returns:
        TestGenerationResult with test generation results
    """
    try:
        # Identify test cases
        test_cases = identify_test_cases(code)
        
        # Create a detailed prompt for the agent
        prompt = f"""
请为以下Python代码生成全面的pytest测试用例和测试代码（请用中文回答）：

待测试代码：
```python
{code}
```

已识别的测试用例：
{', '.join(test_cases) if test_cases else '未识别到测试用例'}

请生成干净、可读的测试代码。
包含正常情况、边界情况和错误条件的测试。
"""
        
        # Create a message for the agent
        message = TextMessage(
            content=prompt,
            source="user"
        )
        
        # Get response from the agent
        response = await testing_agent.on_messages(
            [message], 
            CancellationToken()
        )
        
        # Extract the test code from the response
        test_code = response.chat_message.content
        
        # Estimate coverage
        coverage_percentage = estimate_coverage(test_cases)
        
        return GeneratedTestResult(
            source_code=code,
            test_code=test_code,
            test_cases=test_cases,
            coverage_percentage=coverage_percentage
        )
        
    except Exception as e:
        print(f"Error generating tests: {e}")
        # Return a default test generation result
        return GeneratedTestResult(
            source_code=code,
            test_code=f"# Error occurred during test generation\n# {str(e)}\n\nimport pytest\n\n# TODO: Add test cases",
            test_cases=["Error occurred during test generation"],
            coverage_percentage=0.0
        )


# Example usage
async def main():
    """Example of how to use the testing agent."""
    sample_code = """
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)
"""
    
    test_result = await generate_tests(sample_code)
    print(f"Test result: {test_result}")


if __name__ == "__main__":
    asyncio.run(main())