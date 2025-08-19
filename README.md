# AutoGen Multi-Agent Code Generation System

基于Microsoft AutoGen构建的多智能体系统，能够通过Web界面根据自然语言需求生成、审查、优化和测试Python代码。

> **本项目展示了上下文工程的强大功能，通过Microsoft AutoGen框架实现了实用的多智能体系统。支持完整的中文交互和代码生成。**

## 🚀 快速开始

```bash
# 1. 克隆代码库
git clone <repository-url>
cd autogen-multi-agent-system

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 设置环境变量
cp .env.example .env
# 编辑.env文件，填入实际的API密钥和配置
# 使用Google Gemini时: cp .env.gemini .env

# 5. 启动Web服务器
python -m web.main

# 6. 打开浏览器
# 访问 http://localhost:8000 使用Web界面
# http://127.0.0.1:8008/api/v1/agents
# http://127.0.0.1:8008/static/index.html

```

## 📚 目录

- [什么是上下文工程？](#什么是上下文工程)
- [项目结构](#项目结构)
- [功能特性](#功能特性)
- [LLM提供商配置](#llm提供商配置)
- [API端点](#api端点)
- [运行测试](#运行测试)
- [开发指南](#开发指南)
- [贡献指南](#贡献指南)
- [许可证](#许可证)
- [致谢](#致谢)

## 什么是上下文工程？

上下文工程代表了从传统提示工程向全面上下文提供的范式转变：

### 提示工程 vs 上下文工程

**提示工程:**
- 侧重于巧妙的措辞和特定的表达方式
- 仅限于如何表述任务
- 就像给人一张便利贴

**上下文工程:**
- 提供全面上下文的完整系统
- 包括文档、示例、规则、模式和验证
- 就像编写包含所有细节的完整剧本

### 为什么上下文工程很重要

1. **减少AI失败**: 大多数智能体失败不是模型失败，而是上下文失败
2. **确保一致性**: AI遵循您的项目模式和约定
3. **支持复杂功能**: 通过适当的上下文，AI可以处理多步骤实现
4. **自我纠正**: 验证循环允许AI修复自己的错误

## 项目结构

```
autogen-multi-agent-system/
├── agents/                 # AutoGen智能体实现
│   ├── requirements_agent.py    # 需求分析智能体
│   ├── codegen_agent.py         # 代码生成智能体
│   ├── review_agent.py          # 代码审查智能体
│   ├── optimization_agent.py    # 代码优化智能体
│   ├── testing_agent.py         # 测试智能体
│   ├── provider.py              # LLM提供商配置
│   └── models.py                # 数据模型
├── tools/                  # 代码分析工具
│   ├── code_quality_tool.py     # 代码质量检查工具
│   └── code_optimizer_tool.py   # 代码优化工具
├── web/                    # Web应用程序
│   ├── main.py                  # FastAPI主应用
│   ├── api.py                   # API路由
│   └── frontend/           # 前端文件
│       ├── index.html           # 主页面
│       ├── style.css            # 样式表
│       └── script.js            # JavaScript逻辑
├── config/                 # 配置管理
│   └── settings.py              # 应用设置
├── tests/                  # 单元测试
│   ├── test_requirements_agent.py
│   ├── test_codegen_agent.py
│   ├── test_review_agent.py
│   ├── test_optimization_agent.py
│   ├── test_testing_agent.py
│   └── test_web_interface.py
├── utils/                  # 工具函数
│   └── code_validator.py        # 代码验证工具
├── requirements.txt        # Python依赖
├── .env.example           # 环境变量模板
└── README.md              # 本文档
```

## Features

- **Multi-Agent Architecture**: Five specialized agents working together:
  - Requirements Analysis Agent - 分析用户需求并制定开发计划
  - Code Generation Agent - 根据规范生成Python代码
  - Code Review Agent - 审查代码质量和PEP8合规性
  - Code Optimization Agent - 优化代码性能和可读性
  - Testing Agent - 生成测试用例和测试代码
- **Web Interface**: 用户友好的Web界面，支持中文交互和结果展示
- **Code Quality Assurance**: 自动代码审查和PEP8合规性检查
- **Performance Optimization**: 代码性能优化和可读性改进
- **Automated Testing**: 自动生成测试用例和测试代码
- **Chinese Language Support**: 完整的中文支持，所有智能体使用中文交互

## LLM Provider Configuration

The system supports multiple LLM providers through a flexible configuration system. All agents are configured to use Chinese language responses.

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

Note: The system uses the OpenAI-compatible API endpoint for Google Gemini, which allows seamless integration with the existing AutoGen framework. All agents are configured to request Chinese responses from the LLM.

## API Endpoints

- `GET /` - 根端点，提供API信息
- `POST /api/v1/generate-code` - 根据需求生成代码
- `GET /api/v1/code-status/{task_id}` - 获取代码生成任务状态
- `GET /api/v1/agents` - 列出所有可用智能体
- `GET /api/v1/config` - 获取应用程序配置
- `GET /docs` - 交互式API文档 (Swagger UI)
- `GET /redoc` - 替代API文档 (ReDoc)

## Running Tests

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试文件
pytest tests/test_requirements_agent.py -v

# 运行带覆盖率的测试
pytest tests/ --cov=agents --cov=tools --cov=web --cov=utils -v
```

## Development

### Adding New Agents

1. 在 `agents/` 目录中创建新的智能体文件
2. 使用AutoGen的AssistantAgent实现智能体
3. 在 `tests/` 目录中添加单元测试
4. 如果需要，更新Web API

### Adding New Tools

1. 在 `tools/` 目录中创建新的工具文件
2. 实现工具函数
3. 向相应的智能体注册工具

## Contributing

1. Fork 代码库
2. 创建功能分支
3. 提交您的更改
4. 推送到分支
5. 创建拉取请求

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Microsoft AutoGen团队提供出色的多智能体框架
- FastAPI提供Web框架支持
- 所有为本项目使用的开源库做出贡献的开发者

