"""
Unit tests for the Requirements Analysis Agent.
"""
import pytest
from agents.requirements_agent import analyze_requirements


class TestRequirementsAgent:
    """Test cases for the Requirements Analysis Agent."""
    
    @pytest.mark.asyncio
    async def test_analyze_requirements_success(self):
        """Test successful requirements analysis."""
        # Test with simple requirements
        requirements = "Create a function that calculates fibonacci numbers"
        
        # Mock the agent's response
        result = await analyze_requirements(requirements)
        
        # Verify the result structure
        assert isinstance(result, dict)
        assert "original_requirements" in result
        assert "language" in result
        assert "complexity" in result
        assert "functional_requirements" in result
        assert "non_functional_requirements" in result
        assert "constraints" in result
        
        # Verify the content
        assert result["original_requirements"] == requirements
        assert result["language"] == "python"
        assert result["complexity"] == "medium"
        
    @pytest.mark.asyncio
    async def test_analyze_requirements_with_complex_input(self):
        """Test requirements analysis with complex input."""
        requirements = """
        Build a web scraper that extracts product information from e-commerce websites.
        The scraper should handle pagination, extract product names, prices, and ratings.
        Store the data in a database and provide a REST API to access it.
        """
        
        result = await analyze_requirements(requirements)
        
        assert isinstance(result, dict)
        assert result["original_requirements"] == requirements
        assert result["language"] == "python"
        
    def test_breakdown_requirements_function(self):
        """Test the breakdown_requirements function directly."""
        from agents.requirements_agent import breakdown_requirements
        
        requirements = "Create a calculator app with basic operations"
        result = breakdown_requirements(requirements)
        
        assert isinstance(result, dict)
        assert result["original_requirements"] == requirements
        assert result["language"] == "python"
        assert result["complexity"] == "medium"
        
    @pytest.mark.asyncio
    async def test_analyze_requirements_edge_cases(self):
        """Test requirements analysis with edge cases."""
        # Test with empty requirements
        result1 = await analyze_requirements("")
        assert isinstance(result1, dict)
        
        # Test with very long requirements
        long_requirements = "Create " + "very long requirements " * 100
        result2 = await analyze_requirements(long_requirements)
        assert isinstance(result2, dict)
        assert result2["original_requirements"] == long_requirements


if __name__ == "__main__":
    pytest.main([__file__, "-v"])