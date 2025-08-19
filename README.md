# AutoGen Multi-Agent Code Generation System

A multi-agent system built with Microsoft AutoGen that can generate, review, optimize, and test Python code based on natural language requirements through a web interface.

> **This project demonstrates the power of Context Engineering with a practical implementation using Microsoft AutoGen framework.**

## 🚀 Quick Start

```bash
# 1. Clone this repository
git clone <repository-url>
cd autogen-multi-agent-system

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env file with your actual API keys and configuration
# For Google Gemini, use: cp .env.gemini .env

# 5. Start the web server
python -m web.main

# 6. Open your browser
# Navigate to http://localhost:8000 to access the web interface
# http://127.0.0.1:8008/api/v1/agents
# http://127.0.0.1:8008/static/index.html

```

## 📚 Table of Contents

- [What is Context Engineering?](#what-is-context-engineering)
- [Template Structure](#template-structure)
- [Step-by-Step Guide](#step-by-step-guide)
- [Writing Effective INITIAL.md Files](#writing-effective-initialmd-files)
- [The PRP Workflow](#the-prp-workflow)
- [Using Examples Effectively](#using-examples-effectively)
- [Best Practices](#best-practices)

## What is Context Engineering?

Context Engineering represents a paradigm shift from traditional prompt engineering:

### Prompt Engineering vs Context Engineering

**Prompt Engineering:**
- Focuses on clever wording and specific phrasing
- Limited to how you phrase a task
- Like giving someone a sticky note

**Context Engineering:**
- A complete system for providing comprehensive context
- Includes documentation, examples, rules, patterns, and validation
- Like writing a full screenplay with all the details

### Why Context Engineering Matters

1. **Reduces AI Failures**: Most agent failures aren't model failures - they're context failures
2. **Ensures Consistency**: AI follows your project patterns and conventions
3. **Enables Complex Features**: AI can handle multi-step implementations with proper context
4. **Self-Correcting**: Validation loops allow AI to fix its own mistakes

## Project Structure

```
autogen-multi-agent-system/
├── agents/                 # AutoGen agents implementation
│   ├── requirements_agent.py
│   ├── codegen_agent.py
│   ├── review_agent.py
│   ├── optimization_agent.py
│   ├── testing_agent.py
│   ├── provider.py
│   └── models.py
├── tools/                  # Utility tools for code analysis
│   ├── code_quality_tool.py
│   └── code_optimizer_tool.py
├── web/                    # Web application
│   ├── main.py
│   ├── api.py
│   └── frontend/           # Frontend files
│       ├── index.html
│       ├── style.css
│       └── script.js
├── config/                 # Configuration management
│   └── settings.py
├── tests/                  # Unit tests
│   ├── test_requirements_agent.py
│   ├── test_codegen_agent.py
│   ├── test_review_agent.py
│   ├── test_optimization_agent.py
│   ├── test_testing_agent.py
│   └── test_web_interface.py
├── utils/                  # Utility functions
│   └── code_validator.py
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## Features

- **Multi-Agent Architecture**: Five specialized agents working together:
  - Requirements Analysis Agent
  - Code Generation Agent
  - Code Review Agent
  - Code Optimization Agent
  - Testing Agent
- **Web Interface**: User-friendly web interface for submitting requirements and viewing results
- **Code Quality Assurance**: Automatic code review and PEP8 compliance checking
- **Performance Optimization**: Code optimization for better performance and readability
- **Automated Testing**: Automatic generation of test cases and test code

## LLM Provider Configuration

The system supports multiple LLM providers through a flexible configuration system.

### OpenAI Configuration

To use OpenAI models:
```bash
cp .env.example .env
```

Then edit the `.env` file:
```
LLM_PROVIDER=openai
LLM_API_KEY=your_openai_api_key_here
LLM_MODEL=gpt-4o
LLM_BASE_URL=https://api.openai.com/v1
```

### Google Gemini Configuration

To use Google Gemini models:
```bash
cp .env.gemini .env
```

Then edit the `.env` file:
```
LLM_PROVIDER=gemini
LLM_API_KEY=your_gemini_api_key_here
LLM_MODEL=gemini-1.5-pro
LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta
```

Note: The system uses the OpenAI-compatible API endpoint for Google Gemini, which allows seamless integration with the existing AutoGen framework.

## API Endpoints

- `GET /` - Root endpoint with API information
- `POST /api/v1/generate-code` - Generate code based on requirements
- `GET /api/v1/code-status/{task_id}` - Get status of a code generation task
- `GET /api/v1/agents` - List all available agents
- `GET /api/v1/config` - Get application configuration
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_requirements_agent.py -v

# Run tests with coverage
pytest tests/ --cov=agents --cov=tools --cov=web --cov=utils -v
```

## Development

### Adding New Agents

1. Create a new agent file in the `agents/` directory
2. Implement the agent using AutoGen's AssistantAgent
3. Add unit tests in the `tests/` directory
4. Update the web API if needed

### Adding New Tools

1. Create a new tool file in the `tools/` directory
2. Implement the tool functions
3. Register the tools with the appropriate agents

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Microsoft AutoGen team for the excellent multi-agent framework
- FastAPI for the web framework
- All contributors to the open-source libraries used in this project

