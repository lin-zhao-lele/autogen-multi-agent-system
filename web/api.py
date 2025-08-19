"""
API routes for the AutoGen multi-agent code generation web application.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import asyncio
import uuid
from datetime import datetime

from config.settings import settings
from agents.models import CodeGenerationRequest

# Create API router
api_router = APIRouter(prefix="/api/v1")

# Pydantic models for API requests and responses


class CodeGenerationResponse(BaseModel):
    """Response model for code generation."""
    task_id: str
    message: str


class TaskStatusResponse(BaseModel):
    """Response model for task status."""
    task_id: str
    status: str  # pending, processing, completed, failed
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class AgentResponse(BaseModel):
    """Response model for agent information."""
    name: str
    description: str
    status: str


# In-memory storage for tasks (in production, use a database)
tasks_storage = {}


async def process_code_generation(task_id: str, request: CodeGenerationRequest):
    """Process code generation in the background."""
    try:
        # Update task status
        tasks_storage[task_id]["status"] = "processing"
        tasks_storage[task_id]["updated_at"] = datetime.now()
        
        # Import agents here to avoid circular imports
        from agents.requirements_agent import analyze_requirements
        from agents.codegen_agent import generate_code
        from agents.review_agent import review_code
        from agents.optimization_agent import optimize_code
        from agents.testing_agent import generate_tests
        
        # Step 1: Analyze requirements
        specification = await analyze_requirements(request.requirements)
        
        # Step 2: Generate code
        generated_code = await generate_code(specification)
        
        # Step 3: Review code
        review_result = await review_code(generated_code)
        
        # Step 4: Optimize code
        optimization_result = await optimize_code(generated_code)
        
        # Step 5: Generate tests
        test_result = await generate_tests(generated_code)
        
        # Store final result
        tasks_storage[task_id]["status"] = "completed"
        tasks_storage[task_id]["result"] = {
            "specification": specification,
            "generated_code": generated_code,
            "review_result": review_result.dict(),
            "optimization_result": optimization_result.dict(),
            "test_result": test_result.dict()
        }
        tasks_storage[task_id]["updated_at"] = datetime.now()
        
    except Exception as e:
        # Store error
        tasks_storage[task_id]["status"] = "failed"
        tasks_storage[task_id]["error"] = str(e)
        tasks_storage[task_id]["updated_at"] = datetime.now()


# API routes


@api_router.get("/")
async def get_api_info():
    """Get API information."""
    return {
        "name": "AutoGen Multi-Agent Code Generation API",
        "version": "1.0.0",
        "description": "API for generating, reviewing, and optimizing Python code using AutoGen agents"
    }


@api_router.post("/generate-code", response_model=CodeGenerationResponse)
async def generate_code(request: CodeGenerationRequest):
    """Generate code based on requirements."""
    # Create a task ID
    task_id = str(uuid.uuid4())
    
    # Store initial task status
    tasks_storage[task_id] = {
        "status": "pending",
        "result": None,
        "error": None,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    
    # Start processing in background
    asyncio.create_task(process_code_generation(task_id, request))
    
    return CodeGenerationResponse(
        task_id=task_id,
        message="Code generation task started"
    )


@api_router.get("/code-status/{task_id}", response_model=TaskStatusResponse)
async def get_code_status(task_id: str):
    """Get the status of a code generation task."""
    if task_id not in tasks_storage:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = tasks_storage[task_id]
    return TaskStatusResponse(
        task_id=task_id,
        status=task["status"],
        result=task["result"],
        error=task["error"],
        created_at=task["created_at"],
        updated_at=task["updated_at"]
    )


@api_router.get("/agents", response_model=List[AgentResponse])
async def list_agents():
    """List all available agents."""
    agents = [
        {
            "name": "RequirementsAgent",
            "description": "Analyzes and breaks down programming requirements",
            "status": "active"
        },
        {
            "name": "CodegenAgent",
            "description": "Generates Python code based on specifications",
            "status": "active"
        },
        {
            "name": "ReviewAgent",
            "description": "Reviews code for quality and PEP8 compliance",
            "status": "active"
        },
        {
            "name": "OptimizationAgent",
            "description": "Optimizes code for performance and readability",
            "status": "active"
        },
        {
            "name": "TestingAgent",
            "description": "Generates test cases and test code",
            "status": "active"
        }
    ]
    
    return [AgentResponse(**agent) for agent in agents]


@api_router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now()}


@api_router.get("/config")
async def get_config():
    """Get application configuration."""
    return {
        "llm_provider": settings.llm_provider,
        "llm_model": settings.llm_model,
        "app_env": settings.app_env,
        "debug": settings.debug
    }