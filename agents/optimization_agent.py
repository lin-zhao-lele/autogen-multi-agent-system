"""
Code Optimization Agent for the AutoGen multi-agent system.
This agent is responsible for optimizing generated code for better performance and readability.
"""
import asyncio
from typing import List
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from agents.provider import get_llm_model
from agents.models import CodeOptimizationResult


# System message for the code optimization agent
OPTIMIZATION_AGENT_SYSTEM_MESSAGE = """
You are an expert Python code optimizer. Optimize code for better performance, readability, and maintainability.

When optimizing code, consider:
1. Algorithmic improvements for better performance
2. Code readability and maintainability
3. Memory usage optimization
4. Elimination of redundant operations
5. Better data structure choices
6. Improved error handling
7. Enhanced documentation and comments

Provide detailed explanations of the optimizations made.
"""


def identify_optimization_opportunities(code: str) -> List[str]:
    """
    Identify opportunities for code optimization.
    
    Args:
        code: Python code to analyze
        
    Returns:
        List of optimization opportunities
    """
    # This is a simplified implementation
    # In a real implementation, we would use more sophisticated analysis
    opportunities = []
    
    if "for " in code and "range(" in code:
        opportunities.append("Consider using list comprehensions or generator expressions")
        
    if "import " in code:
        opportunities.append("Check for unused imports")
        
    if len(code.split('\n')) > 50:
        opportunities.append("Consider breaking code into smaller functions")
        
    return opportunities


def estimate_performance_gain(original_code: str, optimized_code: str) -> float:
    """
    Estimate the performance gain from optimization.
    In a real implementation, this would run benchmarks.
    
    Args:
        original_code: Original code
        optimized_code: Optimized code
        
    Returns:
        Estimated performance gain percentage
    """
    # This is a simplified implementation
    # In a real implementation, we would run actual benchmarks
    return 15.0  # Assume 15% improvement


# Create the code optimization agent
optimization_agent = AssistantAgent(
    name="OptimizationAgent",
    system_message=OPTIMIZATION_AGENT_SYSTEM_MESSAGE,
    model_client=get_llm_model()
)


async def optimize_code(code: str) -> CodeOptimizationResult:
    """
    Optimize code for better performance and readability.
    
    Args:
        code: Python code to optimize
        
    Returns:
        CodeOptimizationResult with optimization results
    """
    try:
        # Identify optimization opportunities
        opportunities = identify_optimization_opportunities(code)
        
        # Create a detailed prompt for the agent
        prompt = f"""
Optimize the following Python code for better performance, readability, and maintainability:

Original Code:
```python
{code}
```

Identified Opportunities:
{', '.join(opportunities) if opportunities else 'None identified'}

Provide optimized code with detailed explanations of the improvements made.
"""
        
        # Create a message for the agent
        message = TextMessage(
            content=prompt,
            source="user"
        )
        
        # Get response from the agent
        response = await optimization_agent.on_messages(
            [message], 
            CancellationToken()
        )
        
        # Extract the optimized code from the response
        optimized_code = response.chat_message.content
        
        # Estimate performance gain
        performance_gain = estimate_performance_gain(code, optimized_code)
        
        # Create improvements list
        improvements = []
        if opportunities:
            improvements.extend(opportunities)
        improvements.append("Code optimized by AI assistant")
        
        return CodeOptimizationResult(
            original_code=code,
            optimized_code=optimized_code,
            improvements=improvements,
            performance_gain=performance_gain
        )
        
    except Exception as e:
        print(f"Error optimizing code: {e}")
        # Return a default optimization result
        return CodeOptimizationResult(
            original_code=code,
            optimized_code=code,
            improvements=["Error occurred during code optimization"],
            performance_gain=0.0
        )


# Example usage
async def main():
    """Example of how to use the code optimization agent."""
    sample_code = """
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))
"""
    
    optimization_result = await optimize_code(sample_code)
    print(f"Optimization result: {optimization_result}")


if __name__ == "__main__":
    asyncio.run(main())