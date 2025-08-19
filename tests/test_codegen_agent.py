"""
Unit tests for the Code Generation Agent.
"""
import pytest
from agents.codegen_agent import generate_code


class TestCodegenAgent:
    """Test cases for the Code Generation Agent."""
    
    @pytest.mark.asyncio
    async def test_generate_code_success(self):
        """Test successful code generation."""
        # Test with simple specification
        specification = {
            "original_requirements": "Create a function that calculates fibonacci numbers",
            "language": "python",
            "complexity": "medium"
        }
        
        # Generate code
        result = await generate_code(specification)
        
        # Verify the result
        assert isinstance(result, str)
        assert len(result) > 0
        # Check that it contains Python code elements
        assert "def " in result or "class " in result
        
    @pytest.mark.asyncio
    async def test_generate_code_with_different_languages(self):
        """Test code generation with different language specifications."""
        # Test with Python specification
        python_spec = {
            "original_requirements": "Create a simple calculator",
            "language": "python",
            "complexity": "simple"
        }
        
        result = await generate_code(python_spec)
        assert isinstance(result, str)
        assert len(result) > 0
        
    @pytest.mark.asyncio
    async def test_generate_code_edge_cases(self):
        """Test code generation with edge cases."""
        # Test with empty specification
        empty_spec = {}
        result1 = await generate_code(empty_spec)
        assert isinstance(result1, str)
        
        # Test with minimal specification
        minimal_spec = {
            "original_requirements": "Hello world"
        }
        result2 = await generate_code(minimal_spec)
        assert isinstance(result2, str)
        assert len(result2) > 0
        
    @pytest.mark.asyncio
    async def test_generate_code_complex_requirements(self):
        """Test code generation with complex requirements."""
        complex_spec = {
            "original_requirements": """
            Build a web scraper that extracts product information from e-commerce websites.
            The scraper should handle pagination, extract product names, prices, and ratings.
            Store the data in a database and provide a REST API to access it.
            """,
            "language": "python",
            "complexity": "complex"
        }
        
        result = await generate_code(complex_spec)
        assert isinstance(result, str)
        assert len(result) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])