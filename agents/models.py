"""
Core data models for the AutoGen multi-agent system.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class CodeGenerationRequest(BaseModel):
    """Model for code generation requests."""
    requirements: str = Field(..., description="Programming requirements to implement")
    language: str = Field(default="python", description="Programming language for code generation")
    complexity: str = Field(default="medium", description="Complexity level (simple/medium/complex)")


class CodeReviewResult(BaseModel):
    """Model for code review results."""
    code: str = Field(..., description="Code to review")
    issues: List[str] = Field(default_factory=list, description="List of identified issues")
    suggestions: List[str] = Field(default_factory=list, description="List of improvement suggestions")
    pep8_compliance: bool = Field(default=False, description="Whether code passes PEP8 compliance")
    review_comments: List[str] = Field(default_factory=list, description="Detailed review comments")


class CodeOptimizationResult(BaseModel):
    """Model for code optimization results."""
    original_code: str = Field(..., description="Original code before optimization")
    optimized_code: str = Field(..., description="Optimized code")
    improvements: List[str] = Field(default_factory=list, description="List of improvements made")
    performance_gain: float = Field(default=0.0, description="Estimated performance gain percentage")


class GeneratedTestResult(BaseModel):
    """Model for test generation results."""
    source_code: str = Field(..., description="Source code to generate tests for")
    test_code: str = Field(..., description="Generated test code")
    test_cases: List[str] = Field(default_factory=list, description="List of test cases")
    coverage_percentage: float = Field(default=0.0, description="Estimated code coverage percentage")


class AgentResponse(BaseModel):
    """Generic agent response model."""
    success: bool = Field(..., description="Whether the operation was successful")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    error: Optional[str] = Field(None, description="Error message if failed")
    tools_used: List[str] = Field(default_factory=list, description="List of tools used")
    execution_time: float = Field(default=0.0, description="Execution time in seconds")


class ChatMessage(BaseModel):
    """Model for chat messages."""
    role: str = Field(..., description="Message role (user/assistant)")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.now, description="Message timestamp")
    tools_used: Optional[List[Dict[str, Any]]] = Field(None, description="Tools used in response")


class SessionState(BaseModel):
    """Model for maintaining session state."""
    session_id: str = Field(..., description="Unique session identifier")
    user_id: Optional[str] = Field(None, description="User identifier")
    messages: List[ChatMessage] = Field(default_factory=list, description="Conversation history")
    created_at: datetime = Field(default_factory=datetime.now, description="Session creation time")
    last_activity: datetime = Field(default_factory=datetime.now, description="Last activity timestamp")