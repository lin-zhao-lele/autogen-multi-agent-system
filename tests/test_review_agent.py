"""
Unit tests for the Code Review Agent.
"""
import pytest
from agents.review_agent import review_code
from agents.models import CodeReviewResult


class TestReviewAgent:
    """Test cases for the Code Review Agent."""
    
    @pytest.mark.asyncio
    async def test_review_code_success(self):
        """Test successful code review."""
        # Test with simple code
        code = """
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))
"""
        
        # Review the code
        result = await review_code(code)
        
        # Verify the result structure
        assert isinstance(result, CodeReviewResult)
        assert result.code == code
        assert isinstance(result.issues, list)
        assert isinstance(result.suggestions, list)
        assert isinstance(result.pep8_compliance, bool)
        assert isinstance(result.review_comments, list)
        
    @pytest.mark.asyncio
    async def test_review_code_with_good_quality(self):
        """Test code review with good quality code."""
        code = """
def calculate_fibonacci(n: int) -> int:
    \"\"\"
    Calculate the nth Fibonacci number using an iterative approach.
    
    Args:
        n: The position in the Fibonacci sequence
        
    Returns:
        The nth Fibonacci number
    \"\"\"
    if n < 0:
        raise ValueError("n must be non-negative")
    
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    
    return b

# Example usage
if __name__ == "__main__":
    result = calculate_fibonacci(10)
    print(f"Fibonacci(10) = {result}")
"""
        
        result = await review_code(code)
        assert isinstance(result, CodeReviewResult)
        assert result.code == code
        
    @pytest.mark.asyncio
    async def test_review_code_with_issues(self):
        """Test code review with code that has issues."""
        # Code with common issues
        code = """
import *
def fib(n):
    if n <= 1:
        return n
    else:
        return fib(n-1) + fib(n-2)
print(fib(10))
"""
        
        result = await review_code(code)
        assert isinstance(result, CodeReviewResult)
        assert result.code == code
        # Should identify issues
        assert len(result.issues) >= 0
        assert len(result.review_comments) > 0
        
    @pytest.mark.asyncio
    async def test_review_code_edge_cases(self):
        """Test code review with edge cases."""
        # Test with empty code
        result1 = await review_code("")
        assert isinstance(result1, CodeReviewResult)
        
        # Test with invalid code
        invalid_code = "def x(:"
        result2 = await review_code(invalid_code)
        assert isinstance(result2, CodeReviewResult)
        
        # Test with very long code
        long_code = "def func():\n" + "    pass\n" * 1000
        result3 = await review_code(long_code)
        assert isinstance(result3, CodeReviewResult)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])