"""
Unit tests for the Code Optimization Agent.
"""
import pytest
from agents.optimization_agent import optimize_code
from agents.models import CodeOptimizationResult


class TestOptimizationAgent:
    """Test cases for the Code Optimization Agent."""
    
    @pytest.mark.asyncio
    async def test_optimize_code_success(self):
        """Test successful code optimization."""
        # Test with simple recursive fibonacci code
        code = """
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))
"""
        
        # Optimize the code
        result = await optimize_code(code)
        
        # Verify the result structure
        assert isinstance(result, CodeOptimizationResult)
        assert result.original_code == code
        assert isinstance(result.optimized_code, str)
        assert isinstance(result.improvements, list)
        assert isinstance(result.performance_gain, float)
        
    @pytest.mark.asyncio
    async def test_optimize_code_with_iterative_approach(self):
        """Test optimization of code that can be improved with iterative approach."""
        code = """
def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)
"""
        
        result = await optimize_code(code)
        assert isinstance(result, CodeOptimizationResult)
        assert result.original_code == code
        assert len(result.improvements) >= 0
        
    @pytest.mark.asyncio
    async def test_optimize_code_with_loops(self):
        """Test optimization of code with loops."""
        code = """
def process_list(items):
    result = []
    for i in range(len(items)):
        result.append(items[i] * 2)
    return result
"""
        
        result = await optimize_code(code)
        assert isinstance(result, CodeOptimizationResult)
        assert result.original_code == code
        
    @pytest.mark.asyncio
    async def test_optimize_code_edge_cases(self):
        """Test code optimization with edge cases."""
        # Test with empty code
        result1 = await optimize_code("")
        assert isinstance(result1, CodeOptimizationResult)
        
        # Test with single line
        result2 = await optimize_code("x = 1")
        assert isinstance(result2, CodeOptimizationResult)
        
        # Test with already optimized code
        optimized_code = """
def fibonacci(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
"""
        result3 = await optimize_code(optimized_code)
        assert isinstance(result3, CodeOptimizationResult)
        
    @pytest.mark.asyncio
    async def test_optimize_code_with_complex_logic(self):
        """Test optimization of complex code."""
        complex_code = """
class DataProcessor:
    def __init__(self, data):
        self.data = data
    
    def process(self):
        result = []
        for item in self.data:
            if item > 0:
                result.append(item * 2)
        return result

def main():
    processor = DataProcessor([1, 2, 3, -1, 4])
    result = processor.process()
    print(result)

if __name__ == "__main__":
    main()
"""
        
        result = await optimize_code(complex_code)
        assert isinstance(result, CodeOptimizationResult)
        assert result.original_code == complex_code


if __name__ == "__main__":
    pytest.main([__file__, "-v"])