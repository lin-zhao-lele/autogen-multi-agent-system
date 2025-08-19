"""
Code Optimization Tool for the AutoGen multi-agent system.
This tool provides code optimization suggestions and refactored code.
"""
import ast
import re
from typing import Dict, List, Any


def analyze_code_patterns(code: str) -> List[str]:
    """
    Analyze code for common optimization patterns.
    
    Args:
        code: Python code to analyze
        
    Returns:
        List of identified optimization patterns
    """
    patterns = []
    
    # Check for inefficient loops
    if "for " in code and "range(len(" in code:
        patterns.append("Inefficient loop - consider using enumerate() or direct iteration")
    
    # Check for string concatenation in loops
    if "for " in code and "+=" in code and "''" in code:
        patterns.append("String concatenation in loop - consider using join()")
    
    # Check for list comprehensions opportunity
    if "for " in code and "append" in code:
        patterns.append("Consider using list comprehension")
    
    # Check for unnecessary imports
    if "import " in code:
        patterns.append("Check for unused imports")
    
    return patterns


def suggest_optimizations(code: str) -> List[str]:
    """
    Suggest specific optimizations for the code.
    
    Args:
        code: Python code to optimize
        
    Returns:
        List of optimization suggestions
    """
    suggestions = []
    
    # Basic pattern matching for common optimizations
    if "fibonacci" in code and "recursive" in code.lower():
        suggestions.append("Consider using memoization or iterative approach for better performance")
    
    if "range(len(" in code:
        suggestions.append("Use direct iteration instead of range(len()) when possible")
    
    if "try:" in code and "except:" in code:
        suggestions.append("Specify specific exception types instead of bare except")
    
    return suggestions


def refactor_code(code: str) -> str:
    """
    Apply basic refactoring to the code.
    
    Args:
        code: Python code to refactor
        
    Returns:
        Refactored code
    """
    # This is a simplified implementation
    # In a real implementation, we would use more sophisticated refactoring techniques
    refactored_code = code
    
    # Simple pattern replacements
    # Replace range(len()) with enumerate where applicable
    refactored_code = re.sub(
        r'for i in range\(len\((\w+)\)\):',
        r'for i, item in enumerate(\1):',
        refactored_code
    )
    
    # Add basic type hints if missing
    if "def " in refactored_code and "->" not in refactored_code:
        # Simple heuristic to add return type hints
        refactored_code = re.sub(
            r'def (\w+)\(([^)]*)\):',
            r'def \1(\2) -> Any:',
            refactored_code
        )
    
    return refactored_code


def optimize_code_with_suggestions(code: str) -> Dict[str, Any]:
    """
    Optimize code and provide detailed suggestions.
    
    Args:
        code: Python code to optimize
        
    Returns:
        Dictionary with optimization results and suggestions
    """
    try:
        # Analyze code patterns
        patterns = analyze_code_patterns(code)
        
        # Suggest optimizations
        suggestions = suggest_optimizations(code)
        
        # Refactor code
        refactored_code = refactor_code(code)
        
        # Check if refactored code is syntactically valid
        try:
            ast.parse(refactored_code)
            refactoring_success = True
        except SyntaxError:
            refactoring_success = False
            refactored_code = code  # Revert to original if refactoring breaks syntax
        
        return {
            "success": True,
            "original_code": code,
            "optimized_code": refactored_code,
            "patterns_identified": patterns,
            "suggestions": suggestions,
            "refactoring_success": refactoring_success,
            "improvements_made": refactored_code != code
        }
        
    except Exception as e:
        return {
            "success": False,
            "original_code": code,
            "optimized_code": code,
            "patterns_identified": [],
            "suggestions": [f"Error during optimization: {str(e)}"],
            "refactoring_success": False,
            "improvements_made": False
        }


# Example usage
if __name__ == "__main__":
    sample_code = """
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def process_list(items):
    result = []
    for i in range(len(items)):
        result.append(items[i] * 2)
    return result

print(fibonacci(10))
"""
    
    optimization_result = optimize_code_with_suggestions(sample_code)
    print(f"Optimization result: {optimization_result}")