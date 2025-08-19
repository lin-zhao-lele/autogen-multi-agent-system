name: "AutoGen Multi-Agent Code Generation System"
description: |

## Purpose
Create a multi-agent system using the AutoGen framework that can generate, review, optimize, and test Python code based on user requirements through a web interface.

## Core Principles
1. **Context is King**: Include ALL necessary documentation, examples, and caveats
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
3. **Information Dense**: Use keywords and patterns from the codebase
4. **Progressive Success**: Start simple, validate, then enhance
5. **Global rules**: Be sure to follow all rules in CLAUDE.md

---

## Goal
Build a multi-agent system using the AutoGen framework that:
- Takes user requirements for Python code development
- Generates Python code based on those requirements
- Reviews and checks code quality against PEP8 standards
- Optimizes and fixes code for better performance and readability
- Provides a web-based interface for user interaction
- Includes five specialized agents:
  - Requirements Analysis Agent
  - Code Generation Agent
  - Code Review Agent
  - Code Optimization Agent
  - Testing Agent

## Why
- [Business value and user impact] Enable non-programmers to generate quality Python code through natural language descriptions
- [Integration with existing features] Leverages AutoGen's proven multi-agent framework for complex task automation
- [Problems this solves and for whom] Solves the problem of manual code writing, review, and optimization for developers and non-developers alike

## What
[User-visible behavior and technical requirements]
- Web interface for users to input requirements
- Multi-agent system that processes requirements and generates code
- Code quality checking and optimization
- Automated test generation and execution
- Real-time progress updates through the web interface

### Success Criteria
- [ ] System can generate Python code from natural language requirements
- [ ] Code passes PEP8 compliance checks
- [ ] Code is optimized for performance and readability
- [ ] Automated tests are generated and pass
- [ ] Web interface allows user interaction and displays results
- [ ] All agents work together in a coordinated manner

## All Needed Context

### Documentation & References (list all context needed to implement the feature)
```yaml
# MUST READ - Include these in your context window
- url: https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/index.html
  why: Core AutoGen AgentChat API documentation for building multi-agent systems

- url: https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/agents.html
  why: Understanding different agent types and their capabilities

- url: https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/teams.html
  why: Team collaboration patterns and group chat implementations

- url: https://fastapi.tiangolo.com/
  why: FastAPI documentation for building the web interface

- file: /Users/lin/Documents/AICoding/Context-Engineering-Intro/use-cases/pydantic-ai/examples/main_agent_reference/cli.py
  why: Pattern for building command-line interfaces with agent interactions

- file: /Users/lin/Documents/AICoding/Context-Engineering-Intro/use-cases/mcp-server/examples/database-tools.ts
  why: Example of tool registration and permission-based access patterns

- docfile: /Users/lin/Documents/AICoding/Context-Engineering-Intro/CLAUDE.md
  why: Project-specific coding standards and guidelines
```

### Current Codebase tree (run `tree` in the root of the project) to get an overview of the codebase
```bash
.
├── CLAUDE.md
├── INITIAL.md
├── INITIAL_EXAMPLE.md
├── LICENSE
├── PRPs/
│   ├── autogen-multi-agent-system.md
│   ├── templates/
│   │   └── prp_base.md
│   └── ai_docs/
├── README.md
├── claude-code-full-guide/
├── examples/
├── use-cases/
│   ├── mcp-server/
│   └── pydantic-ai/
└── venv_linux
```

### Desired Codebase tree with files to be added and responsibility of file
```bash
.
├── agents/
│   ├── __init__.py               # Package init
│   ├── requirements_agent.py     # Requirements analysis agent
│   ├── codegen_agent.py          # Code generation agent
│   ├── review_agent.py           # Code review agent
│   ├── optimization_agent.py     # Code optimization agent
│   ├── testing_agent.py          # Testing agent
│   ├── provider.py              # LLM provider configuration
│   └── models.py                # Pydantic models for data validation
├── tools/
│   ├── __init__.py              # Package init
│   ├── code_quality_tool.py     # Code quality checking tool
│   └── code_optimizer_tool.py   # Code optimization tool
├── web/
│   ├── __init__.py              # Package init
│   ├── main.py                  # FastAPI application entry point
│   ├── api.py                   # API routes
│   └── frontend/                # Frontend files (HTML, CSS, JS)
├── config/
│   ├── __init__.py              # Package init
│   └── settings.py              # Environment and config management
├── tests/
│   ├── __init__.py              # Package init
│   ├── test_requirements_agent.py
│   ├── test_codegen_agent.py
│   ├── test_review_agent.py
│   ├── test_optimization_agent.py
│   ├── test_testing_agent.py
│   └── test_web_interface.py
├── utils/
│   ├── __init__.py              # Package init
│   └── code_validator.py        # Code validation utilities
├── .env.example                 # Environment variables template
├── requirements.txt             # Updated dependencies
└── README.md                   # Comprehensive documentation
```

## Implementation Blueprint

### Data models and structure

Create the core data models, we ensure type safety and consistency.
```python
# Models for agent communication and data validation
# - Pydantic models for requirements, code, and test cases
# - Data structures for agent messages and responses
# - Configuration models for LLM settings

class CodeGenerationRequest(BaseModel):
    """Model for code generation requests"""
    requirements: str
    language: str = "python"
    complexity: str = "medium"

class CodeReviewResult(BaseModel):
    """Model for code review results"""
    code: str
    issues: List[str]
    suggestions: List[str]
    pep8_compliance: bool

class CodeOptimizationResult(BaseModel):
    """Model for code optimization results"""
    original_code: str
    optimized_code: str
    improvements: List[str]
    performance_gain: float

class TestGenerationResult(BaseModel):
    """Model for test generation results"""
    test_code: str
    test_cases: List[str]
    coverage_percentage: float
```

### list of tasks to be completed to fullfill the PRP in the order they should be completed

```yaml
Task 1:
CREATE config/settings.py:
  - MIRROR pattern from: use-cases/pydantic-ai/examples/main_agent_reference/settings.py
  - IMPLEMENT environment variable loading with python-dotenv
  - DEFINE configuration for LLM providers and API keys

Task 2:
CREATE agents/provider.py:
  - MIRROR pattern from: use-cases/pydantic-ai/examples/main_agent_reference/providers.py
  - IMPLEMENT LLM provider configuration for OpenAI, Anthropic, etc.
  - DEFINE model selection and API key management

Task 3:
CREATE agents/models.py:
  - MIRROR pattern from: use-cases/pydantic-ai/examples/main_agent_reference/models.py
  - IMPLEMENT Pydantic models for data validation
  - DEFINE data structures for agent communication

Task 4:
CREATE agents/requirements_agent.py:
  - IMPLEMENT AssistantAgent for requirements analysis
  - DEFINE system prompt for understanding user requirements
  - CREATE tool for breaking down complex requirements

Task 5:
CREATE agents/codegen_agent.py:
  - IMPLEMENT AssistantAgent for code generation
  - DEFINE system prompt for Python code generation
  - CREATE tool for generating code based on requirements

Task 6:
CREATE agents/review_agent.py:
  - IMPLEMENT AssistantAgent for code review
  - DEFINE system prompt for code quality assessment
  - CREATE tool for PEP8 compliance checking

Task 7:
CREATE agents/optimization_agent.py:
  - IMPLEMENT AssistantAgent for code optimization
  - DEFINE system prompt for code performance improvements
  - CREATE tool for code refactoring and optimization

Task 8:
CREATE agents/testing_agent.py:
  - IMPLEMENT AssistantAgent for test generation
  - DEFINE system prompt for test case creation
  - CREATE tool for generating pytest test cases

Task 9:
CREATE tools/code_quality_tool.py:
  - IMPLEMENT tool for code quality checking
  - INTEGRATE with pycodestyle or flake8 for PEP8 compliance
  - RETURN detailed feedback on code issues

Task 10:
CREATE tools/code_optimizer_tool.py:
  - IMPLEMENT tool for code optimization suggestions
  - ANALYZE code for performance improvements
  - PROVIDE refactored code with explanations

Task 11:
CREATE web/main.py:
  - MIRROR pattern from: FastAPI documentation
  - IMPLEMENT FastAPI application setup
  - DEFINE main application entry point

Task 12:
CREATE web/api.py:
  - IMPLEMENT API routes for user interaction
  - DEFINE endpoints for submitting requirements and getting results
  - INTEGRATE with agent system for processing requests

Task 13:
CREATE utils/code_validator.py:
  - IMPLEMENT code validation utilities
  - INTEGRATE with pylint or similar tools
  - PROVIDE detailed error reporting

Task 14:
CREATE tests/test_requirements_agent.py:
  - MIRROR pattern from: use-cases/pydantic-ai/examples/testing_examples/test_agent_patterns.py
  - IMPLEMENT unit tests for requirements agent
  - TEST requirements parsing and breakdown

Task 15:
CREATE tests/test_codegen_agent.py:
  - IMPLEMENT unit tests for code generation agent
  - TEST code generation from requirements
  - VERIFY generated code syntax

Task 16:
CREATE tests/test_review_agent.py:
  - IMPLEMENT unit tests for code review agent
  - TEST code quality assessment
  - VERIFY PEP8 compliance checking

Task 17:
CREATE tests/test_optimization_agent.py:
  - IMPLEMENT unit tests for code optimization agent
  - TEST code performance improvements
  - VERIFY optimization suggestions

Task 18:
CREATE tests/test_testing_agent.py:
  - IMPLEMENT unit tests for testing agent
  - TEST test case generation
  - VERIFY test code validity

Task 19:
CREATE tests/test_web_interface.py:
  - IMPLEMENT integration tests for web interface
  - TEST API endpoints
  - VERIFY user interaction flow

Task 20:
CREATE web/frontend/:
  - IMPLEMENT basic HTML/CSS/JavaScript frontend
  - CREATE user interface for submitting requirements
  - DISPLAY results from agent processing
```


### Per task pseudocode as needed added to each task
```python
# Task 1: Settings Configuration
# Pseudocode for environment variable management
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")
    
    # LLM Configuration
    llm_provider: str = Field(default="openai")
    llm_api_key: str = Field(...)
    llm_model: str = Field(default="gpt-4")

def load_settings() -> Settings:
    load_dotenv()
    return Settings()

# Task 4: Requirements Analysis Agent
# Pseudocode for requirements agent
from autogen import AssistantAgent
from agents.provider import get_llm_model

requirements_agent = AssistantAgent(
    name="RequirementsAgent",
    system_message="""You are an expert at analyzing and breaking down programming requirements.
    Your task is to understand user requirements and create a detailed specification.""",
    llm_config=get_llm_model()
)

@requirements_agent.tool
async def breakdown_requirements(requirements: str) -> dict:
    """Break down complex requirements into smaller tasks"""
    # Implementation here
    pass

# Task 5: Code Generation Agent
# Pseudocode for code generation agent
codegen_agent = AssistantAgent(
    name="CodegenAgent",
    system_message="""You are an expert Python developer. Generate clean, efficient, 
    and well-documented Python code based on the provided requirements.""",
    llm_config=get_llm_model()
)

@codegen_agent.tool
async def generate_code(specification: dict) -> str:
    """Generate Python code based on detailed specification"""
    # Implementation here
    pass

# Task 9: Code Quality Tool
# Pseudocode for code quality checking
import subprocess

async def check_code_quality(code: str) -> dict:
    """Check code quality using pycodestyle"""
    # Write code to temporary file
    # Run pycodestyle on the file
    # Parse results and return structured feedback
    pass
```

### Integration Points
```yaml
DATABASE:
  - No database required for initial implementation
  
CONFIG:
  - add to: config/settings.py
  - pattern: "LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'openai')"
  - pattern: "LLM_API_KEY = os.getenv('LLM_API_KEY')"
  
ROUTES:
  - add to: web/api.py  
  - pattern: "app.post('/generate-code', generate_code_endpoint)"
  - pattern: "app.get('/code-status/{task_id}', get_code_status)"
```

## Validation Loop

### Level 1: Syntax & Style
```bash
# Run these FIRST - fix any errors before proceeding
ruff check src/ --fix  # Auto-fix what's possible
mypy src/              # Type checking

# Expected: No errors. If errors, READ the error and fix.
```

### Level 2: Unit Tests each new feature/file/function use existing test patterns
```python
# CREATE tests/test_agents.py with these test cases:
def test_requirements_agent():
    """Test requirements agent can parse and breakdown requirements"""
    # Test with sample requirements
    # Verify structured output
    pass

def test_code_generation_agent():
    """Test code generation agent produces valid Python code"""
    # Test with sample specification
    # Verify code syntax and structure
    pass

def test_code_review_agent():
    """Test code review agent identifies issues correctly"""
    # Test with sample code containing known issues
    # Verify issue detection and suggestions
    pass

def test_code_optimization_agent():
    """Test code optimization agent provides meaningful improvements"""
    # Test with sample code that can be optimized
    # Verify optimization suggestions
    pass

def test_testing_agent():
    """Test testing agent generates valid test cases"""
    # Test with sample code
    # Verify generated test code is syntactically correct
    pass
```

```bash
# Run and iterate until passing:
uv run pytest tests/test_agents.py -v
# If failing: Read error, understand root cause, fix code, re-run (never mock to pass)
```

### Level 3: Integration Test
```bash
# Start the web service
uv run python -m web.main --dev

# Test the code generation endpoint
curl -X POST http://localhost:8000/generate-code \
  -H "Content-Type: application/json" \
  -d '{"requirements": "Create a function that calculates fibonacci numbers", "language": "python"}'

# Expected: {"status": "success", "task_id": "..."}
# Then check status and results
curl http://localhost:8000/code-status/{task_id}

# If error: Check logs for stack trace
```

### Level 4: End-to-End Test
```bash
# Test complete workflow through web interface
# 1. Submit requirements via web form
# 2. Wait for agent processing
# 3. Verify generated code
# 4. Check code review results
# 5. Verify optimized code
# 6. Check generated tests
```

## Final validation Checklist
- [ ] All unit tests pass: `uv run pytest tests/ -v`
- [ ] No linting errors: `uv run ruff check src/`
- [ ] No type errors: `uv run mypy src/`
- [ ] Web interface works: Manual test via browser
- [ ] Agent coordination works: Requirements → Code → Review → Optimize → Test
- [ ] Error cases handled gracefully
- [ ] Logs are informative but not verbose
- [ ] Documentation updated if needed

---

## Anti-Patterns to Avoid
- ❌ Don't create new patterns when existing ones work
- ❌ Don't skip validation because "it should work"  
- ❌ Don't ignore failing tests - fix them
- ❌ Don't use sync functions in async context
- ❌ Don't hardcode values that should be config
- ❌ Don't catch all exceptions - be specific
- ❌ Don't ignore AutoGen's async requirements
- ❌ Don't forget to validate environment variables
- ❌ Don't expose sensitive information in logs or responses