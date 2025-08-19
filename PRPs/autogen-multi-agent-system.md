name: "AutoGen 多智能体代码生成系统"
description: |

## 目的
使用AutoGen框架创建一个多智能体系统，能够通过Web界面根据用户需求生成、审查、优化和测试Python代码。

## 核心原则
1. **上下文为王**: 包含所有必要的文档、示例和注意事项
2. **验证循环**: 提供可执行的测试/lint，让AI可以运行和修复
3. **信息密集**: 使用代码库中的关键词和模式
4. **渐进式成功**: 从简单开始，验证，然后增强
5. **全局规则**: 确保遵循CLAUDE.md中的所有规则

---

## 目标
构建一个使用AutoGen框架的多智能体系统，能够：
- 接收用户对Python代码开发的需求
- 根据这些需求生成Python代码
- 审查和检查代码质量，确保符合PEP8标准
- 优化和修复代码以提高性能和可读性
- 提供基于Web的用户交互界面
- 包含五个专门的智能体：
  - 需求分析智能体
  - 代码生成智能体
  - 代码审查智能体
  - 代码优化智能体
  - 测试智能体

## 为什么
- [业务价值和用户影响] 使非程序员能够通过自然语言描述生成高质量的代码
- [与现有功能集成] 利用AutoGen经过验证的多智能体框架进行复杂任务自动化
- [解决的问题和受益对象] 为开发者和非开发者解决手动编写、审查和优化代码的问题

## 功能
[用户可见行为和技术要求]
- 用户输入需求的Web界面
- 处理需求并生成代码的多智能体系统
- 代码质量检查和优化
- 自动化测试生成和执行
- 通过Web界面实时更新进度

### 成功标准
- [ ] 系统能够从自然语言需求生成Python代码
- [ ] 代码通过PEP8合规性检查
- [ ] 代码经过性能和可读性优化
- [ ] 自动生成测试并通过测试
- [ ] Web界面允许用户交互并显示结果
- [ ] 所有智能体协调工作

## 所需上下文

### 文档和参考资料（实现功能所需的所有上下文）
```yaml
# 必须阅读 - 将这些包含在上下文窗口中
- url: https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/index.html
  why: 构建多智能体系统的核心AutoGen AgentChat API文档

- url: https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/agents.html
  why: 理解不同智能体类型及其能力

- url: https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/teams.html
  why: 团队协作模式和群聊实现

- url: https://fastapi.tiangolo.com/
  why: 构建Web界面的FastAPI文档

- file: /Users/lin/Documents/AICoding/autogen-multi-agent-system/use-cases/pydantic-ai/examples/main_agent_reference/cli.py
  why: 构建命令行界面与智能体交互的模式

- file: /Users/lin/Documents/AICoding/autogen-multi-agent-system/use-cases/mcp-server/examples/database-tools.ts
  why: 工具注册和基于权限的访问模式示例

- docfile: /Users/lin/Documents/AICoding/autogen-multi-agent-system/CLAUDE.md
  why: 项目特定的编码标准和指南
```

### 当前代码库结构（在项目根目录运行`tree`获取概览）
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

### 期望的代码库结构（要添加的文件及其职责）
```bash
.
├── agents/                 # 智能体模块
│   ├── __init__.py               # 包初始化
│   ├── requirements_agent.py     # 需求分析智能体
│   ├── codegen_agent.py          # 代码生成智能体
│   ├── review_agent.py           # 代码审查智能体
│   ├── optimization_agent.py     # 代码优化智能体
│   ├── testing_agent.py          # 测试智能体
│   ├── provider.py              # LLM提供商配置
│   └── models.py                # Pydantic数据验证模型
├── tools/                  # 工具模块
│   ├── __init__.py              # 包初始化
│   ├── code_quality_tool.py     # 代码质量检查工具
│   └── code_optimizer_tool.py   # 代码优化工具
├── web/                    # Web界面
│   ├── __init__.py              # 包初始化
│   ├── main.py                  # FastAPI应用入口点
│   ├── api.py                   # API路由
│   └── frontend/                # 前端文件（HTML, CSS, JS）
├── config/                 # 配置管理
│   ├── __init__.py              # 包初始化
│   └── settings.py              # 环境和配置管理
├── tests/                  # 测试套件
│   ├── __init__.py              # 包初始化
│   ├── test_requirements_agent.py
│   ├── test_codegen_agent.py
│   ├── test_review_agent.py
│   ├── test_optimization_agent.py
│   ├── test_testing_agent.py
│   └── test_web_interface.py
├── utils/                  # 工具函数
│   ├── __init__.py              # 包初始化
│   └── code_validator.py        # 代码验证工具
├── .env.example                 # 环境变量模板
├── requirements.txt             # 更新的依赖项
└── README.md                   # 全面的文档
```

## 实现蓝图

### 数据模型和结构

创建核心数据模型，确保类型安全和一致性。
```python
# 智能体通信和数据验证的模型
# - 需求、代码和测试用例的Pydantic模型
# - 智能体消息和响应的数据结构
# - LLM设置的配置模型

class CodeGenerationRequest(BaseModel):
    """代码生成请求模型"""
    requirements: str
    language: str = "python"
    complexity: str = "medium"

class CodeReviewResult(BaseModel):
    """代码审查结果模型"""
    code: str
    issues: List[str]
    suggestions: List[str]
    pep8_compliance: bool

class CodeOptimizationResult(BaseModel):
    """代码优化结果模型"""
    original_code: str
    optimized_code: str
    improvements: List[str]
    performance_gain: float

class TestGenerationResult(BaseModel):
    """测试生成结果模型"""
    test_code: str
    test_cases: List[str]
    coverage_percentage: float
```

### 完成任务列表（按顺序完成PRP）

```yaml
任务1:
创建 config/settings.py:
  - 镜像模式来自: use-cases/pydantic-ai/examples/main_agent_reference/settings.py
  - 使用python-dotenv实现环境变量加载
  - 定义LLM提供商和API密钥的配置

任务2:
创建 agents/provider.py:
  - 镜像模式来自: use-cases/pydantic-ai/examples/main_agent_reference/providers.py
  - 实现OpenAI、Anthropic等的LLM提供商配置
  - 定义模型选择和API密钥管理

任务3:
创建 agents/models.py:
  - 镜像模式来自: use-cases/pydantic-ai/examples/main_agent_reference/models.py
  - 实现Pydantic数据验证模型
  - 定义智能体通信的数据结构

任务4:
创建 agents/requirements_agent.py:
  - 实现需求分析的AssistantAgent
  - 定义理解用户需求的系统提示
  - 创建分解复杂需求的工具

任务5:
创建 agents/codegen_agent.py:
  - 实现代码生成的AssistantAgent
  - 定义Python代码生成的系统提示
  - 创建基于需求生成代码的工具

任务6:
创建 agents/review_agent.py:
  - 实现代码审查的AssistantAgent
  - 定义代码质量评估的系统提示
  - 创建PEP8合规性检查的工具

任务7:
创建 agents/optimization_agent.py:
  - 实现代码优化的AssistantAgent
  - 定义代码性能改进的系统提示
  - 创建代码重构和优化的工具

任务8:
创建 agents/testing_agent.py:
  - 实现测试生成的AssistantAgent
  - 定义测试用例创建的系统提示
  - 创建生成pytest测试用例的工具

任务9:
创建 tools/code_quality_tool.py:
  - 实现代码质量检查工具
  - 集成pycodestyle或flake8进行PEP8合规性检查
  - 返回代码问题的详细反馈

任务10:
创建 tools/code_optimizer_tool.py:
  - 实现代码优化建议工具
  - 分析代码以进行性能改进
  - 提供重构后的代码和解释

任务11:
创建 web/main.py:
  - 镜像模式来自: FastAPI文档
  - 实现FastAPI应用设置
  - 定义主应用入口点

任务12:
创建 web/api.py:
  - 实现用户交互的API路由
  - 定义提交需求和获取结果的端点
  - 与智能体系统集成处理请求

任务13:
创建 utils/code_validator.py:
  - 实现代码验证工具
  - 集成pylint或类似工具
  - 提供详细的错误报告

任务14:
创建 tests/test_requirements_agent.py:
  - 镜像模式来自: use-cases/pydantic-ai/examples/testing_examples/test_agent_patterns.py
  - 实现需求分析智能体的单元测试
  - 测试需求解析和分解

任务15:
创建 tests/test_codegen_agent.py:
  - 实现代码生成智能体的单元测试
  - 测试从需求生成代码
  - 验证生成的代码语法

任务16:
创建 tests/test_review_agent.py:
  - 实现代码审查智能体的单元测试
  - 测试代码质量评估
  - 验证PEP8合规性检查

任务17:
创建 tests/test_optimization_agent.py:
  - 实现代码优化智能体的单元测试
  - 测试代码性能改进
  - 验证优化建议

任务18:
创建 tests/test_testing_agent.py:
  - 实现测试智能体的单元测试
  - 测试测试用例生成
  - 验证测试代码有效性

任务19:
创建 tests/test_web_interface.py:
  - 实现Web界面的集成测试
  - 测试API端点
  - 验证用户交互流程

任务20:
创建 web/frontend/:
  - 实现基本的HTML/CSS/JavaScript前端
  - 创建提交需求的用户界面
  - 显示智能体处理结果
```

### 每项任务的伪代码（根据需要添加）
```python
# 任务1: 设置配置
# 环境变量管理的伪代码
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")
    
    # LLM配置
    llm_provider: str = Field(default="openai")
    llm_api_key: str = Field(...)
    llm_model: str = Field(default="gpt-4")

def load_settings() -> Settings:
    load_dotenv()
    return Settings()

# 任务4: 需求分析智能体
# 需求分析智能体的伪代码
from autogen import AssistantAgent
from agents.provider import get_llm_model

requirements_agent = AssistantAgent(
    name="RequirementsAgent",
    system_message="""你是一个专业的编程需求分析专家。你的任务是理解用户需求并创建详细的代码实现规范。

分析需求时请考虑：
1. 应该使用什么编程语言
2. 需要实现什么功能
3. 预期的输入和输出是什么
4. 任何特定的约束或要求
5. 实现的复杂度级别

请提供清晰、结构化的需求分解，以便其他智能体生成代码。

请用中文回答。""",
    llm_config=get_llm_model()
)

@requirements_agent.tool
async def breakdown_requirements(requirements: str) -> dict:
    """将复杂需求分解为更小的任务"""
    # 实现代码
    pass

# 任务5: 代码生成智能体
# 代码生成智能体的伪代码
codegen_agent = AssistantAgent(
    name="CodegenAgent",
    system_message="""你是一个专业的Python开发专家。根据提供的需求生成干净、高效、文档完善的Python代码。

生成代码时请遵循以下准则：
1. 编写符合PEP8标准的干净、可读代码
2. 不要注释
3. 处理边界情况和错误条件
4. 编写性能良好的高效代码
5. 遵循Python最佳实践和约定

你的回答应该只包含生成的代码，不要包含额外的解释或markdown格式。

请用中文回答。""",
    llm_config=get_llm_model()
)

@codegen_agent.tool
async def generate_code(specification: dict) -> str:
    """根据详细规范生成Python代码"""
    # 实现代码
    pass

# 任务9: 代码质量工具
# 代码质量检查的伪代码
import subprocess

async def check_code_quality(code: str) -> dict:
    """使用pycodestyle检查代码质量"""
    # 将代码写入临时文件
    # 在文件上运行pycodestyle
    # 解析结果并返回结构化反馈
    pass
```

### 集成点
```yaml
数据库:
  - 初始实现不需要数据库
  
配置:
  - 添加到: config/settings.py
  - 模式: "LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'openai')"
  - 模式: "LLM_API_KEY = os.getenv('LLM_API_KEY')"
  
路由:
  - 添加到: web/api.py  
  - 模式: "app.post('/generate-code', generate_code_endpoint)"
  - 模式: "app.get('/code-status/{task_id}', get_code_status)"
```

## 验证循环

### 级别1: 语法和样式
```bash
# 首先运行这些 - 在继续之前修复任何错误
ruff check src/ --fix  # 自动修复可能的问题
mypy src/              # 类型检查

# 期望: 没有错误。如果有错误，阅读错误并修复。
```

### 级别2: 单元测试（每个新功能/文件/函数使用现有测试模式）
```python
# 创建 tests/test_agents.py 包含这些测试用例：
def test_requirements_agent():
    """测试需求分析智能体可以解析和分解需求"""
    # 使用示例需求进行测试
    # 验证结构化输出
    pass

def test_code_generation_agent():
    """测试代码生成智能体产生有效的Python代码"""
    # 使用示例规范进行测试
    # 验证代码语法和结构
    pass

def test_code_review_agent():
    """测试代码审查智能体正确识别问题"""
    # 使用包含已知问题的示例代码进行测试
    # 验证问题检测和建议
    pass

def test_code_optimization_agent():
    """测试代码优化智能体提供有意义的改进"""
    # 使用可以优化的示例代码进行测试
    # 验证优化建议
    pass

def test_testing_agent():
    """测试测试智能体生成有效的测试用例"""
    # 使用示例代码进行测试
    # 验证生成的测试代码语法正确
    pass
```

```bash
# 运行并迭代直到通过：
uv run pytest tests/test_agents.py -v
# 如果失败: 阅读错误，理解根本原因，修复代码，重新运行（不要mock来通过）
```

### 级别3: 集成测试
```bash
# 启动Web服务
uv run python -m web.main --dev

# 测试代码生成端点
curl -X POST http://localhost:8000/generate-code \
  -H "Content-Type: application/json" \
  -d '{"requirements": "创建一个计算斐波那契数的函数", "language": "python"}'

# 期望: {"status": "success", "task_id": "..."}
# 然后检查状态和结果
curl http://localhost:8000/code-status/{task_id}

# 如果错误: 检查日志中的堆栈跟踪
```

### 级别4: 端到端测试
```bash
# 通过Web界面测试完整工作流程
# 1. 通过Web表单提交需求
# 2. 等待智能体处理
# 3. 验证生成的代码
# 4. 检查代码审查结果
# 5. 验证优化后的代码
# 6. 检查生成的测试
```

## 最终验证清单
- [ ] 所有单元测试通过: `uv run pytest tests/ -v`
- [ ] 没有lint错误: `uv run ruff check src/`
- [ ] 没有类型错误: `uv run mypy src/`
- [ ] Web界面工作正常: 通过浏览器手动测试
- [ ] 智能体协调工作: 需求 → 代码 → 审查 → 优化 → 测试
- [ ] 错误情况得到优雅处理
- [ ] 日志信息丰富但不冗长
- [ ] 文档已根据需要更新

---

## 要避免的反模式
- ❌ 不要在有现有模式可用时创建新模式
- ❌ 不要因为"应该能工作"而跳过验证  
- ❌ 不要忽略失败的测试 - 修复它们
- ❌ 不要在异步上下文中使用同步函数
- ❌ 不要硬编码应该配置的值
- ❌ 不要捕获所有异常 - 要具体
- ❌ 不要忽略AutoGen的异步要求
- ❌ 不要忘记验证环境变量
- ❌ 不要在日志或响应中暴露敏感信息