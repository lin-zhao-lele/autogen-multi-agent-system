"""
Code Quality Tool for the AutoGen multi-agent system.
This tool checks code quality and PEP8 compliance.
"""
import subprocess
import tempfile
import os
from typing import Dict, Any


def check_code_quality(code: str) -> Dict[str, Any]:
    """
    Check code quality using pycodestyle (PEP8 compliance).
    
    Args:
        code: Python code to check
        
    Returns:
        Dictionary with quality check results
    """
    try:
        # Create a temporary file to store the code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name
        
        # Run pycodestyle on the temporary file
        result = subprocess.run(
            ['pycodestyle', temp_file_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Clean up the temporary file
        os.unlink(temp_file_path)
        
        # Parse the results
        issues = []
        if result.stdout:
            issues = result.stdout.strip().split('\n')
        
        return {
            "success": True,
            "issues": issues,
            "pep8_compliance": len(issues) == 0,
            "error": None
        }
        
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "issues": [],
            "pep8_compliance": False,
            "error": "Code quality check timed out"
        }
    except Exception as e:
        return {
            "success": False,
            "issues": [],
            "pep8_compliance": False,
            "error": f"Error checking code quality: {str(e)}"
        }


def check_code_complexity(code: str) -> Dict[str, Any]:
    """
    Check code complexity using radon.
    
    Args:
        code: Python code to check
        
    Returns:
        Dictionary with complexity analysis results
    """
    try:
        # Create a temporary file to store the code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name
        
        # Run radon cc (cyclomatic complexity) on the temporary file
        result = subprocess.run(
            ['radon', 'cc', temp_file_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Clean up the temporary file
        os.unlink(temp_file_path)
        
        # Parse the results
        complexity_info = []
        if result.stdout:
            complexity_info = result.stdout.strip().split('\n')
        
        return {
            "success": True,
            "complexity_info": complexity_info,
            "error": None
        }
        
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "complexity_info": [],
            "error": "Complexity check timed out"
        }
    except Exception as e:
        return {
            "success": False,
            "complexity_info": [],
            "error": f"Error checking code complexity: {str(e)}"
        }


def get_detailed_feedback(code: str) -> Dict[str, Any]:
    """
    Get detailed feedback on code quality.
    
    Args:
        code: Python code to analyze
        
    Returns:
        Dictionary with detailed feedback
    """
    # Check PEP8 compliance
    quality_result = check_code_quality(code)
    
    # Check code complexity
    complexity_result = check_code_complexity(code)
    
    # Combine results
    feedback = {
        "pep8_compliance": quality_result["pep8_compliance"],
        "issues": quality_result["issues"],
        "complexity_info": complexity_result["complexity_info"],
        "overall_quality": "Good" if quality_result["pep8_compliance"] and quality_result["success"] else "Needs improvement"
    }
    
    return feedback


# Example usage
if __name__ == "__main__":
    sample_code = """
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))
"""
    
    feedback = get_detailed_feedback(sample_code)
    print(f"Code quality feedback: {feedback}")