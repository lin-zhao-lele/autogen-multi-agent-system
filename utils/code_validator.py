"""
Code Validator utilities for the AutoGen multi-agent system.
This module provides tools for validating Python code syntax and structure.
"""
import ast
import subprocess
import tempfile
import os
from typing import Dict, Any


def validate_python_syntax(code: str) -> Dict[str, Any]:
    """
    Validate Python code syntax.
    
    Args:
        code: Python code to validate
        
    Returns:
        Dictionary with validation results
    """
    try:
        # Parse the code to check syntax
        ast.parse(code)
        return {
            "valid": True,
            "errors": [],
            "warnings": []
        }
    except SyntaxError as e:
        return {
            "valid": False,
            "errors": [f"Syntax error at line {e.lineno}: {e.msg}"],
            "warnings": []
        }
    except Exception as e:
        return {
            "valid": False,
            "errors": [f"Error validating syntax: {str(e)}"],
            "warnings": []
        }


def check_imports(code: str) -> Dict[str, Any]:
    """
    Check for imports in the code and validate them.
    
    Args:
        code: Python code to check
        
    Returns:
        Dictionary with import validation results
    """
    try:
        # Parse the code
        tree = ast.parse(code)
        
        # Find all import statements
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        
        return {
            "imports": imports,
            "count": len(imports),
            "success": True,
            "error": None
        }
    except Exception as e:
        return {
            "imports": [],
            "count": 0,
            "success": False,
            "error": f"Error checking imports: {str(e)}"
        }


def run_pyflakes_check(code: str) -> Dict[str, Any]:
    """
    Run pyflakes check on the code.
    
    Args:
        code: Python code to check
        
    Returns:
        Dictionary with pyflakes results
    """
    try:
        # Create a temporary file to store the code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name
        
        # Run pyflakes on the temporary file
        result = subprocess.run(
            ['pyflakes', temp_file_path],
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
            "error": None
        }
        
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "issues": [],
            "error": "Pyflakes check timed out"
        }
    except FileNotFoundError:
        return {
            "success": False,
            "issues": [],
            "error": "Pyflakes not installed"
        }
    except Exception as e:
        return {
            "success": False,
            "issues": [],
            "error": f"Error running pyflakes: {str(e)}"
        }


def comprehensive_code_validation(code: str) -> Dict[str, Any]:
    """
    Perform comprehensive code validation.
    
    Args:
        code: Python code to validate
        
    Returns:
        Dictionary with comprehensive validation results
    """
    # Validate syntax
    syntax_result = validate_python_syntax(code)
    
    # Check imports
    imports_result = check_imports(code)
    
    # Run pyflakes check
    pyflakes_result = run_pyflakes_check(code)
    
    # Combine results
    validation_result = {
        "syntax": syntax_result,
        "imports": imports_result,
        "pyflakes": pyflakes_result,
        "overall_valid": syntax_result["valid"] and pyflakes_result["success"],
        "timestamp": __import__('datetime').datetime.now().isoformat()
    }
    
    return validation_result


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
    
    validation_result = comprehensive_code_validation(sample_code)
    print(f"Validation result: {validation_result}")