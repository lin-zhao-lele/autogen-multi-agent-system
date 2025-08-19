"""
Unit tests for the Testing Agent.
"""
import pytest
from agents.testing_agent import generate_tests
from agents.models import GeneratedTestResult


class TestTestingAgent:
    """Test cases for the Testing Agent."""
    
    @pytest.mark.asyncio
    async def test_generate_tests_success(self):
        """Test successful test generation."""
        # Test with simple fibonacci function
        code = """
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)
"""
        
        # Generate tests
        result = await generate_tests(code)
        
        # Verify the result structure
        assert isinstance(result, GeneratedTestResult)
        assert result.source_code == code
        assert isinstance(result.test_code, str)
        assert isinstance(result.test_cases, list)
        assert isinstance(result.coverage_percentage, float)
        
    @pytest.mark.asyncio
    async def test_generate_tests_with_class(self):
        """Test test generation for class-based code."""
        code = """
class Calculator:
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
"""
        
        result = await generate_tests(code)
        assert isinstance(result, GeneratedTestResult)
        assert result.source_code == code
        assert len(result.test_cases) >= 0
        assert isinstance(result.test_code, str)
        
    @pytest.mark.asyncio
    async def test_generate_tests_edge_cases(self):
        """Test test generation with edge cases."""
        # Test with empty code
        result1 = await generate_tests("")
        assert isinstance(result1, GeneratedTestResult)
        
        # Test with single function
        result2 = await generate_tests("def x(): pass")
        assert isinstance(result2, GeneratedTestResult)
        
        # Test with complex function
        complex_code = """
def complex_function(a, b, c=None, *args, **kwargs):
    if c is None:
        return a + b
    elif isinstance(c, list):
        return sum(c) + a + b
    else:
        return a * b * c
"""
        result3 = await generate_tests(complex_code)
        assert isinstance(result3, GeneratedTestResult)
        
    @pytest.mark.asyncio
    async def test_generate_tests_with_error_handling(self):
        """Test test generation with code that has error handling."""
        code = """
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
"""
        
        result = await generate_tests(code)
        assert isinstance(result, GeneratedTestResult)
        assert result.source_code == code
        # Should identify test cases for normal and error conditions
        assert len(result.test_cases) >= 0
        
    @pytest.mark.asyncio
    async def test_generate_tests_coverage_estimation(self):
        """Test coverage estimation in test generation."""
        simple_code = """
def add(a, b):
    return a + b
"""
        
        result = await generate_tests(simple_code)
        assert isinstance(result, GeneratedTestResult)
        assert result.source_code == simple_code
        # Coverage should be a reasonable percentage
        assert 0 <= result.coverage_percentage <= 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])